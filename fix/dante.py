import argparse
import json
import sys
import re
from pathlib import Path
import dante_corpus as dc
from llm7shi.compat import generate_with_schema

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PATH_TITLES = SCRIPT_DIR / "titles.json"

def read_canto_text(canticle, canto_no):
    canto = dc.canto(canticle, canto_no)
    result = ""
    for line in canto.lines():
        if line.no > 1 and line.no % 3 == 1:
            result += "\n"
        result += f"{line.no} {line.text}\n"
    return result

def load_titles():
    """Load section titles from titles.json."""
    if not PATH_TITLES.exists():
        print(f"Error: {PATH_TITLES} not found. Run extract_titles.py first.", file=sys.stderr)
        sys.exit(1)
    with open(PATH_TITLES, 'r', encoding='utf-8') as f:
        # Keys are strings in JSON, convert to integers
        return {int(k): v for k, v in json.load(f).items()}

def read_file(path):
    path = Path(path)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")

def write_file(path, content):
    Path(path).write_text(content, encoding="utf-8")

def extract_code_block(text):
    # Matches triple backtick blocks, optionally with a language identifier
    match = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1)
    return text.rstrip()

def run_llm(messages, model):
    # Passing the list of messages to the library
    response = generate_with_schema(messages, model=model, show_params=False)
    return extract_code_block(response.text) + "\n"

def cmd_review(input_path, output_path, model):
    print(f"Reviewing {input_path}...")
    target_text = read_file(input_path)
    original_text = read_canto_text("inferno", 1)
    
    prompt = """You are an expert translator and reviewer specializing in Dante's Inferno.
Your task is to review the following translation against the original Italian text.

## Protocols
1. **Analysis**: Compare the target translation against the source text (`inferno-01.txt`) tercet by tercet.
2. **Identify Errors**: Look for mistranslations, awkward literalisms, grammatical errors, and stylistic mismatches.
3. **Execution**:
    - **Do NOT** correct the translation text itself. Keep it exactly as is.
    - Insert comments into the **blank lines** between tercets.
    - Format: `- Note: {Points of criticism}`.
    - Explicitly state why it is wrong and suggest corrections.
    - Do NOT list errors separately; embed them in the text.

Output the full text with embedded review notes.
IMPORTANT: Wrap the entire output in a single code block using triple backticks (```)."""
    
    result = run_llm([
        f"Original Text (Italian):\n```\n{original_text.rstrip()}\n```",
        f"Target Text (to review):\n```\n{target_text.rstrip()}\n```",
        prompt
    ], model)
    write_file(output_path, result)
    print(f"Reviewed text written to {output_path}")

def cmd_fix(input_path, output_path, model):
    print(f"Fixing {input_path}...")
    reviewed_text = read_file(input_path)
    
    prompt = """You are an expert translator.
Your task is to correct the following translation based on the embedded review notes.

## Protocols
1. **Execution**:
    - Address each `- Note:` comment by modifying the corresponding lines.
    - **Remove the `- Note:` lines** completely after applying the fix.
    - Maintain the literal translation style unless noted otherwise.
2. **Formatting**:
    - Ensure line numbers and structure remain consistent.

Output the corrected, clean text without notes.
IMPORTANT: Wrap the entire output in a single code block using triple backticks (```)."""
    
    result = run_llm([
        f"Reviewed Text (with notes):\n```\n{reviewed_text.rstrip()}\n```",
        prompt
    ], model)
    write_file(output_path, result)
    print(f"Fixed text written to {output_path}")

def cmd_quote(input_path, output_path, model):
    print(f"Fixing quotes in {input_path}...")
    target_text = read_file(input_path)
    original_text = read_canto_text("inferno", 1)
    target_lines = target_text.splitlines()
    
    prompt = """You are an expert translator and editor specializing in Dante's Inferno.
Your task is to identify and list lines that need quotation mark fixes by comparing the translation with the original Italian text.

## Protocols
1. **Analysis**: Compare the target translation against the source text (`inferno-01.txt`) tercet by tercet.
2. **Identify Missing Quotes**: Look for dialogue lines where the original Italian uses quotation marks (« ») but the translation is missing opening or closing quotes.
   - Missing closing quotes are the most common issue.
   - Pay special attention to dialogue that continues across multiple lines or tercets.
3. **Quote Style**: Use the SAME quotation mark style already present in the translation. Do NOT change the quote style.
   - Examples: " " (English), 「 」(Japanese), « » (French), etc.
4. **Output Format**:
   - Output ONLY the corrected lines, one per line.
   - The translation already contains line numbers at the beginning of each line. Keep the line numbers as they are.
   - Example: `115 kie vi aŭdos la malesperajn kriojn,"`
   - If no fixes are needed, output "NO_FIXES_NEEDED"
   - Do NOT output any other text, explanations, or the full text.

IMPORTANT: 
   - Keep the existing line numbers in the output. Do NOT add extra line numbers.
   - **ONLY add missing quotation marks**. Do NOT modify anything else - no punctuation changes, no word changes, no spacing changes."""
    
    response = run_llm([
        f"Original Text (Italian):\n```\n{original_text.rstrip()}\n```",
        f"Target Text (to fix quotes):\n```\n{target_text.rstrip()}\n```",
        prompt
    ], model)
    
    # Parse response and apply fixes
    if response.strip() == "NO_FIXES_NEEDED":
        write_file(output_path, target_text)
        print(f"No quote fixes needed. Copied to {output_path}")
        return
    
    # Build a dictionary of fixes: line number -> new content
    fixes = {}
    for line in response.strip().splitlines():
        if not line.strip():
            continue
        # Extract line number from beginning of the line
        match = re.match(r'^(\d+)\s+(.*)', line)
        if match:
            line_num = int(match.group(1))
            fixes[line_num] = line.strip()
    
    # Apply fixes by matching line numbers at the beginning of each line
    result_lines = []
    for line in target_lines:
        # Match lines starting with a number
        match = re.match(r'^(\d+)\s+(.*)', line)
        if match:
            line_num = int(match.group(1))
            if line_num in fixes:
                result_lines.append(fixes[line_num])
            else:
                result_lines.append(line)
        else:
            # Headers and empty lines are preserved
            result_lines.append(line)
    
    write_file(output_path, '\n'.join(result_lines) + '\n')
    print(f"Fixed quotes written to {output_path}")

def cmd_split(input_path, output_path, model, language=None):
    print(f"Splitting {input_path} using section structure from {PATH_TITLES}...")
    target_text = read_file(input_path)
    
    # Use provided language or detect from filename
    if language:
        target_language = language
    else:
        target_language = Path(input_path).stem
    
    # Load section titles from titles.json
    titles = load_titles()
    sections = sorted(titles.items())  # List of (line_number, english_title) tuples
    
    if not sections:
        print(f"Warning: No section headers found in {PATH_TITLES}")
        write_file(output_path, target_text)
        return
    
    # Translate section titles using LLM
    english_titles = [title for _, title in sections]
    section_titles = "Section titles to translate:\n```\n" + "\n".join(english_titles) + "\n```"
    titles_prompt = f"""Translate the above section titles from English into {target_language}.

## Protocols
1. Translate each title accurately and naturally into {target_language}.
2. Output ONLY the translated titles in {target_language}, one per line, in the same order.
3. Do NOT add numbers, explanations, or any other text.
4. Do NOT output markdown formatting or code blocks.

IMPORTANT: Output exactly {len(english_titles)} lines, one translation per line."""
    
    translated_response = run_llm([section_titles, titles_prompt], model)
    translated_titles = translated_response.strip().splitlines()
    
    # Handle case where LLM returns fewer lines than expected
    if len(translated_titles) < len(english_titles):
        print(f"Warning: Expected {len(english_titles)} translations, got {len(translated_titles)}. Using original titles where missing.")
        # Pad with original English titles
        translated_titles.extend(english_titles[len(translated_titles):])
    
    # Build a dictionary: line_number -> translated title
    section_headers = {}
    for i, (line_num, _) in enumerate(sections):
        if i < len(translated_titles):
            section_headers[line_num] = translated_titles[i].strip()
    
    # Insert headers into the target text
    target_lines = target_text.splitlines()
    result_lines = []
    inserted_headers = set()
    
    for line in target_lines:
        # Check if this line starts with a number
        match = re.match(r'^(\d+)\s+', line)
        if match:
            line_num = int(match.group(1))
            # If we haven't inserted a header for this position yet and one exists
            if line_num in section_headers and line_num not in inserted_headers:
                # Insert the header with blank lines before and after
                result_lines.append(f"# {section_headers[line_num]}")
                result_lines.append("")  # blank line after header
                inserted_headers.add(line_num)
        
        result_lines.append(line)
    
    write_file(output_path, '\n'.join(result_lines) + '\n')
    print(f"Sectioned text written to {output_path}")

def main():
    model = "google:gemini-3-pro-preview"
    parser = argparse.ArgumentParser(description="Dante Translation Workflow Automation")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Main output options (common to all subcommands)
    out_group = parser.add_mutually_exclusive_group(required=True)
    out_group.add_argument("-o", "--output", help="Output text file (for single file only)")
    out_group.add_argument("--outdir", help="Output directory (uses input filename)")
    
    # Model option
    parser.add_argument("-m", "--model", default=model, help="LLM model to use (default: google:gemini-3-pro-preview)")
    
    # Review
    p_rev = subparsers.add_parser("review", help="Review translation")
    p_rev.add_argument("inputs", nargs="+", help="Input text file(s)")
    
    # Fix
    p_fix = subparsers.add_parser("fix", help="Fix translation based on notes")
    p_fix.add_argument("inputs", nargs="+", help="Input text file(s) (with notes)")
    
    # Quote
    p_quote = subparsers.add_parser("quote", help="Check and mark missing quotes")
    p_quote.add_argument("inputs", nargs="+", help="Input text file(s)")
    
    # Split
    p_split = subparsers.add_parser("split", help="Add section headers")
    p_split.add_argument("inputs", nargs="+", help="Input text file(s)")
    p_split.add_argument("-l", "--language", help="Target language name (auto-detected from filename if not specified)")
    
    args = parser.parse_args()
    model = args.model
    
    # Validate -o is only used with single file
    if args.output and len(args.inputs) > 1:
        print("Error: -o/--output can only be used with a single input file. Use --outdir for multiple files.", file=sys.stderr)
        sys.exit(1)
    
    # Process each input file
    for input_path in args.inputs:
        # Determine output path
        if args.outdir:
            output_path = Path(args.outdir) / Path(input_path).name
        else:
            output_path = args.output
        
        if args.command == "review":
            cmd_review(input_path, output_path, model)
        elif args.command == "fix":
            cmd_fix(input_path, output_path, model)
        elif args.command == "split":
            cmd_split(input_path, output_path, model, getattr(args, 'language', None))
        elif args.command == "quote":
            cmd_quote(input_path, output_path, model)

if __name__ == "__main__":
    main()
