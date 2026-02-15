import argparse
import base64
import mimetypes
import os
import re
import struct
import sys
import time
from collections import deque
from google import genai
from google.genai import types

# Track timestamps of the last 10 TTS calls for rate limiting (10 RPM)
_call_timestamps = deque(maxlen=10)

def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()

def _wait_for_rate_limit():
    """Wait if necessary to respect the 10 RPM rate limit."""
    global _call_timestamps
    if len(_call_timestamps) == 10:
        # Check if 60 seconds have passed since the 10th most recent call
        time_since_10th_call = time.time() - _call_timestamps[0]
        if time_since_10th_call < 60:
            sleep_time = 60 - time_since_10th_call
            print(f"Rate limit: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time + 1)

def generate(file_name: str, text: str, model: str, speakers: dict[str, str] | None = None):
    global _call_timestamps
    
    # Wait for rate limit before making the call
    _wait_for_rate_limit()
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),
            ],
        ),
    ]
    
    # Set default speakers if None
    if speakers is None:
        speakers = {"speaker": "Zephyr"}
    
    # Build speech config based on number of speakers
    if len(speakers) == 1:
        # Single speaker: use simple voice config without speaker label
        voice_name = list(speakers.values())[0]
        speech_config = types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        )
    else:
        # Multiple speakers: use multi-speaker voice config
        speaker_voice_configs = [
            types.SpeakerVoiceConfig(
                speaker=speaker,
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name
                    )
                ),
            )
            for speaker, voice_name in speakers.items()
        ]
        speech_config = types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=speaker_voice_configs
            )
        )
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=speech_config,
    )

    # Cache audio chunks
    chunks = []
    # Note: The genai library's generate_content_stream expects ContentListUnionDict
    # but we're passing list[Content] which is compatible at runtime. The type
    # definition shows ContentListUnion = Union[ContentUnion, list[ContentUnion]]
    # where ContentUnion includes Content, so list[Content] is valid.
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,  # type: ignore[arg-type]
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            print(f"Warning: Skipping invalid chunk (missing candidates/content/parts)")
            continue
        part = chunk.candidates[0].content.parts[0]
        if part.inline_data and part.inline_data.data:
            chunks.append(part.inline_data)
        elif part.text:
            print(f"Warning: Received text instead of audio: {part.text[:100]}...")
        else:
            print(f"Warning: Chunk has no inline_data or text")
    
    # Record the timestamp after the call completes
    _call_timestamps.append(time.time())

    # Check if any chunks were collected
    if not chunks:
        print(f"Error: No audio data received from API")
        return []

    # Save cached chunks
    file_extension = None
    output_files = []
    for i, inline_data in enumerate(chunks):
        data_buffer = inline_data.data
        if file_extension is None:
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
        # Single chunk: no suffix, Multiple chunks: add suffix
        if len(chunks) == 1:
            output_path = f"{file_name}{file_extension}"
        else:
            output_path = f"{file_name}_{i}{file_extension}"
        save_binary_file(output_path, data_buffer)
        output_files.append(output_path)
        # Verify file was created
        if not os.path.exists(output_path):
            print(f"Error: Failed to create file: {output_path}")
        else:
            file_size = os.path.getsize(output_path)
            print(f"  Created: {output_path} ({file_size} bytes)")
    
    return output_files

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"] or 16
    sample_rate = parameters["rate"] or 24000
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}
