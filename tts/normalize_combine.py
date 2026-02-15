"""
Script to normalize volume and combine multiple WAV files

Usage:
    uv run normalize_combine.py input1.wav input2.wav ... -o output.wav
    uv run normalize_combine.py *.wav -o output.wav
"""

import argparse
import sys
from pathlib import Path
from pydub import AudioSegment

def normalize_audio(audio, target_db=-14.0):
    """
    Normalize audio to the specified dB level
    
    Args:
        audio: AudioSegment object
        target_db: Target dB (default: -14.0 dBFS)
    
    Returns:
        Normalized AudioSegment
    """
    # Get current dB
    current_db = audio.dBFS
    
    # Calculate gain
    gain = target_db - current_db
    
    # Apply
    return audio.apply_gain(gain)

def combine_wav_files(input_files, output_file, target_db=-14.0, crossfade_ms=0, outdir=None):
    """
    Normalize and combine multiple WAV files
    
    Args:
        input_files: List of input WAV files
        output_file: Output file path
        target_db: Target dB (default: -14.0 dBFS)
        crossfade_ms: Crossfade time in milliseconds
        outdir: Output directory for individual normalized files (if None, no output)
    """
    if not input_files:
        print("Error: No input files specified")
        sys.exit(1)
    
    # Create directory if outdir is specified
    if outdir:
        Path(outdir).mkdir(parents=True, exist_ok=True)
    
    print(f"Number of files to process: {len(input_files)}")
    print(f"Target dB: {target_db} dBFS")
    
    # Load first file
    print(f"\n1. {input_files[0]}")
    combined = AudioSegment.from_wav(input_files[0])
    print(f"   Length: {len(combined)/1000:.2f} seconds, dBFS: {combined.dBFS:.2f}")
    
    # Normalize
    combined = normalize_audio(combined, target_db)
    print(f"   Normalized dBFS: {combined.dBFS:.2f}")
    
    # Output normalized file if outdir is specified
    if outdir:
        norm_file = Path(outdir) / Path(input_files[0]).name
        combined.export(norm_file, format="wav")
        print(f"   Individual output: {norm_file}")
    
    # Combine remaining files
    for i, file_path in enumerate(input_files[1:], 2):
        print(f"\n{i}. {file_path}")
        audio = AudioSegment.from_wav(file_path)
        print(f"   Length: {len(audio)/1000:.2f} seconds, dBFS: {audio.dBFS:.2f}")
        
        # Normalize
        audio = normalize_audio(audio, target_db)
        print(f"   Normalized dBFS: {audio.dBFS:.2f}")
        
        # Output normalized file if outdir is specified
        if outdir:
            norm_file = Path(outdir) / Path(file_path).name
            audio.export(norm_file, format="wav")
            print(f"   Individual output: {norm_file}")
        
        # Combine (with crossfade support)
        if crossfade_ms > 0:
            combined = combined.append(audio, crossfade=crossfade_ms)
        else:
            combined += audio
    
    # Combined output (only if output_file is specified)
    if output_file:
        print(f"\nCombined output: {output_file}")
        print(f"Total length: {len(combined)/1000:.2f} seconds")
        
        # Match format to first file
        combined.export(output_file, format="wav")
    
    print("Complete!")

def main():
    parser = argparse.ArgumentParser(
        description='Normalize volume and combine multiple WAV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  uv run normalize_combine.py file1.wav file2.wav file3.wav -o output.wav
  uv run normalize_combine.py *.wav -o combined.wav
  uv run normalize_combine.py *.wav -o output.wav -t -16.0
        """
    )
    
    parser.add_argument('input_files', nargs='+', help='Input WAV files')
    parser.add_argument('-o', '--output', help='Output filename (skips combining if omitted)')
    parser.add_argument('-t', '--target-db', type=float, default=-14.0,
                       help='Target dBFS value (default: -14.0)')
    parser.add_argument('-c', '--crossfade', type=int, default=0,
                       help='Crossfade time in milliseconds (default: 0)')
    parser.add_argument('-s', '--sort', action='store_true',
                       help='Sort files by name before processing')
    parser.add_argument('--outdir', help='Output directory for individual normalized files (does not affect combined file)')
    
    args = parser.parse_args()
    
    # Validation: Either -o or --outdir is required
    if not args.output and not args.outdir:
        print("Error: Please specify either -o (--output) or --outdir")
        sys.exit(1)
    
    # Sort files
    input_files = args.input_files
    if args.sort:
        input_files = sorted(input_files)
    
    # Verify existence
    for f in input_files:
        if not Path(f).exists():
            print(f"Error: File not found: {f}")
            sys.exit(1)
    
    combine_wav_files(input_files, args.output, args.target_db, args.crossfade, args.outdir)

if __name__ == "__main__":
    main()
