import argparse
import os
import re
import sys
from tts import generate

def read_lines(file_path: str) -> list[str]:
    """Read text file and extract text lines (without line numbers)."""
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            # Remove line number prefix (e.g., "1 ", "123 ")
            line = re.sub(r'^\d+\s+', '', line)
            if line:
                lines.append(line)
    return lines

def read_sections(file_path: str) -> list[tuple[str, list[str]]]:
    """Read text file and split into sections by headers (lines starting with #).
    
    Returns a list of tuples: (section_name, lines)
    """
    sections = []
    current_name = ""
    current_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Check for section header (lines starting with #)
            if line.startswith('#'):
                # Save previous section if exists
                if current_lines:
                    sections.append((current_name, current_lines))
                # Start new section
                current_name = line.lstrip('#').strip()
                current_lines = []
            elif re.match(r'^\d+\s+', line):
                # Remove line number prefix and add to current section
                line = re.sub(r'^\d+\s+', '', line)
                if line:
                    current_lines.append(line)
            # Ignore lines that don't start with # or a number
        
        # Add the last section
        if current_lines:
            sections.append((current_name, current_lines))
    
    return sections

def process_file(input_file: str, language: str | None, model: str, outdir: str | None = None) -> list[str]:
    """Process a text file and generate audio files."""
    # Determine language name
    if language:
        lang = language
    else:
        lang = os.path.splitext(os.path.basename(input_file))[0]
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Create output directory if specified
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    
    # Read sections
    sections = read_sections(input_file)
    print(f"Total sections: {len(sections)}")
    
    if not sections:
        print("No sections to process")
        return []
    
    # Process each section
    all_generated = []
    for i, (section_name, lines) in enumerate(sections, 1):
        # Generate filename with section number
        section_base = f"{base_name}-{i}"
        output_file = section_base + '.wav'
        
        # Full output path
        if outdir:
            output_path = os.path.join(outdir, output_file)
            section_path = os.path.join(outdir, section_base)
        else:
            output_path = output_file
            section_path = section_base
        
        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"Skipping section {i}/{len(sections)}: {output_path} already exists")
            continue
        
        # Combine lines for this section
        section_text = '\n'.join(lines)
        
        # Add instruction prefix
        text = f"Poetry reading in {lang}:\n{section_text}"
        
        print(f"\nProcessing section {i}/{len(sections)}: {section_name or 'Untitled'}")
        print(f"Lines: {len(lines)}")
        print(f"Generating: {output_path}")
        
        # Generate audio for this section
        generated_files = generate(section_path, text, model)
        all_generated.extend(generated_files)
    
    print(f"\n=== Complete: {len(all_generated)} files generated ===")
    for f in all_generated:
        print(f"  {f}")
    
    return all_generated


def parse_voice_mapping(voice_str: str) -> tuple[str, str]:
    """Parse voice mapping string 'speaker:voice_name' into tuple."""
    parts = voice_str.split(':')
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Invalid voice format '{voice_str}'. Expected 'speaker:voice_name'")
    return (parts[0].strip(), parts[1].strip())


def process_multiple_files(input_files: list[str], voices: list[tuple[str, str]], model: str, outdir: str | None = None) -> list[str]:
    """Process multiple files with interleaved lines and speaker labels, section by section."""
    # Create output directory if specified
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    
    # Read sections from all files
    file_sections = []
    for input_file in input_files:
        sections = read_sections(input_file)
        if not sections:
            print(f"Warning: No sections found in {input_file}")
            continue
        file_sections.append(sections)
        print(f"Read {len(sections)} sections from {input_file}")
    
    if not file_sections:
        print("No sections to process from any file")
        return []
    
    # Check for exactly 2 files
    if len(file_sections) != 2:
        print(f"Error: Exactly 2 files required for multiple speaker mode, but got {len(file_sections)}")
        return []
    
    # Check that both files have the same number of sections
    if len(file_sections[0]) != len(file_sections[1]):
        print(f"Error: Section count mismatch. File 1 has {len(file_sections[0])} sections, File 2 has {len(file_sections[1])} sections")
        return []
    
    # Determine speaker names
    if voices:
        speakers = [v[0] for v in voices]
    else:
        # Use filename without extension as speaker name
        speakers = [os.path.splitext(os.path.basename(f))[0] for f in input_files]
    
    # Build voice mapping
    voice_mapping = {}
    if voices:
        voice_mapping = dict(voices)
    else:
        # Default voice mapping for bilingual reading
        voice_mapping = {"Italian": "Algieba", "English": "Aoede"}
    
    # Generate output filename base
    base_names = [os.path.splitext(os.path.basename(f))[0] for f in input_files]
    output_base = '-'.join(base_names)
    
    # Process each section pair
    all_generated = []
    num_sections = len(file_sections[0])
    
    for section_idx in range(num_sections):
        section_name_1, lines_1 = file_sections[0][section_idx]
        section_name_2, lines_2 = file_sections[1][section_idx]
        
        # Check that both sections have the same number of lines
        if len(lines_1) != len(lines_2):
            print(f"Error: Line count mismatch in section {section_idx + 1}. File 1 has {len(lines_1)} lines, File 2 has {len(lines_2)} lines")
            return []
        
        # Generate section output filename
        section_base = f"{output_base}-{section_idx + 1}"
        output_file = section_base + '.wav'
        
        # Full output path
        if outdir:
            output_path = os.path.join(outdir, output_file)
            section_path = os.path.join(outdir, section_base)
        else:
            output_path = output_file
            section_path = section_base
        
        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"Skipping section {section_idx + 1}/{num_sections}: {output_path} already exists")
            continue
        
        # Interleave lines from both sections
        interleaved_text = []
        for line_idx in range(len(lines_1)):
            for file_idx, lines in enumerate([lines_1, lines_2]):
                speaker = speakers[file_idx]
                text_line = lines[line_idx]
                interleaved_text.append(f"{speaker}: {text_line}")
        
        # Join all lines
        combined_text = '\n'.join(interleaved_text)
        
        # Add instruction prefix with speaker names
        speaker_list = " and ".join(speakers)
        text = f"Poetry reading in {speaker_list}:\n{combined_text}"
        
        print(f"\nProcessing section {section_idx + 1}/{num_sections}: {section_name_1 or 'Untitled'}")
        print(f"Lines per section: {len(lines_1)}")
        print(f"Total interleaved lines: {len(interleaved_text)}")
        print(f"Generating: {output_path}")
        
        # Generate audio with speakers mapping
        generated_files = generate(section_path, text, model, voice_mapping)
        all_generated.extend(generated_files)
    
    print(f"\n=== Complete: {len(all_generated)} files generated ===")
    for f in all_generated:
        print(f"  {f}")
    
    return all_generated


def main():
    model = "gemini-2.5-flash-preview-tts"
    parser = argparse.ArgumentParser(description='Generate audio from text file')
    parser.add_argument('input_files', nargs='+', help='Input text file(s)')
    parser.add_argument('-l', '--language', help='Language name (defaults to input filename without extension)')
    parser.add_argument('-m', '--model', default=model, help='TTS model to use (default: gemini-2.5-flash-preview-tts)')
    parser.add_argument('--multiple', action='store_true', help='Interleave lines from multiple files with speaker labels')
    parser.add_argument('-v', '--voice', action='append', type=parse_voice_mapping, 
                        help='Voice mapping in format speaker:voice_name (e.g., -v Italian:Algieba). Can be used multiple times.')
    parser.add_argument('-o', '--outdir', help='Output directory for generated audio files')
    args = parser.parse_args()
    model = args.model
    
    # Validate --multiple requires exactly 2 files
    if args.multiple and len(args.input_files) != 2:
        print(f"Error: --multiple option requires exactly 2 input files, but got {len(args.input_files)}")
        sys.exit(1)
    
    total_generated = []
    
    if args.multiple:
        # Multiple files with --multiple: interleave lines with speaker labels
        print(f"\n{'='*60}")
        print(f"Processing {len(args.input_files)} files with interleaved lines")
        print(f"{'='*60}")
        generated = process_multiple_files(args.input_files, args.voice, model, args.outdir)
        total_generated.extend(generated)
    else:
        # Default: process each file individually (single or multiple files)
        for input_file in args.input_files:
            print(f"\n{'='*60}")
            print(f"Processing file: {input_file}")
            print(f"{'='*60}")
            generated = process_file(input_file, args.language, model, args.outdir)
            total_generated.extend(generated)
    
    print(f"\n{'='*60}")
    print(f"=== All files complete: {len(total_generated)} total files generated ===")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
