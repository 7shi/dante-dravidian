import argparse
import re
from pathlib import Path

from llm import LLMClient, history_to_xml

PROMPT_MD_PATH = Path(__file__).with_name("PROMPT.md")
_CACHED_STEP_BLOCKS: list[str] | None = None

def _extract_fenced_code_blocks(markdown_text: str) -> list[str]:
    """Return the contents of all triple-backtick fenced code blocks."""
    # Supports ``` and ```lang
    pattern = re.compile(r"```[^\n]*\n(.*?)\n```", re.DOTALL)
    return [match.group(1) for match in pattern.finditer(markdown_text)]

def _first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line
    return ""

def read_prompt(step_heading_prefix: str) -> str:
    """Load a Step prompt from PROMPT.md.

    Finds a fenced code block whose first non-empty line starts with `step_heading_prefix`
    (e.g., "### Step 4").
    """
    global _CACHED_STEP_BLOCKS
    if _CACHED_STEP_BLOCKS is None:
        markdown_text = PROMPT_MD_PATH.read_text(encoding="utf-8")
        _CACHED_STEP_BLOCKS = _extract_fenced_code_blocks(markdown_text)

    for block in _CACHED_STEP_BLOCKS:
        if _first_non_empty_line(block).startswith(step_heading_prefix):
            return block.strip()

    available = []
    for block in _CACHED_STEP_BLOCKS:
        head = _first_non_empty_line(block).strip()
        if head.startswith("### Step "):
            available.append(head)
    available_msg = "\n".join(f"- {h}" for h in available) if available else "(no '### Step' blocks found)"
    raise ValueError(
        f"Prompt block not found for prefix: {step_heading_prefix}\n"
        f"Looked in: {PROMPT_MD_PATH}\n"
        f"Available Step blocks:\n{available_msg}"
    )

STEP1_PROMPT = read_prompt("### Step 1:")
STEP2_PROMPT = read_prompt("### Step 2:")
STEP3_PROMPT = read_prompt("### Step 3:")
STEP4_PROMPT = read_prompt("### Step 4:")
STEP5_PROMPT = read_prompt("### Step 5:")
def read_text_input(text):
    """Read text from file if prefixed with @, otherwise return as-is."""
    if text.startswith('@'):
        with open(text[1:], 'r', encoding='utf-8') as f:
            return f.read().strip()
    return text

def step1(llm_client, source_text, reference):
    """Step 1: Source-Reference Alignment & Semantic Analysis."""
    prompt = STEP1_PROMPT.format(source_text=source_text.rstrip(), reference=reference.rstrip())
    return llm_client.call(prompt)

def step2(llm_client, target_lang):
    """Step 2: Morphosyntactic Requirement Definition."""
    prompt = STEP2_PROMPT.format(target_lang=target_lang)
    return llm_client.call(prompt)

def step3(llm_client, target_lang):
    """Step 3: Pre-assembled Lexical Inventory."""
    prompt = STEP3_PROMPT.format(target_lang=target_lang)
    return llm_client.call(prompt)

def step4(llm_client, target_lang):
    """Step 4: Slot-Based Syntactic Assembly."""
    prompt = STEP4_PROMPT.format(target_lang=target_lang)
    return llm_client.call(prompt)

def step5(llm_client, target_lang):
    """Step 5: Self-Correction via Back-Translation."""
    prompt = STEP5_PROMPT.format(target_lang=target_lang)
    return llm_client.call(prompt)

def print_header(prompt):
    """Print header for each step."""
    first_line = prompt.strip().splitlines()[0]
    print()
    print(first_line)
    print()

def get_result(history):
    """Extract final translation result from LLMClient history."""
    return _extract_fenced_code_blocks(history[-1]["content"])[-1]

def translate(client, target_lang):
    """Run the complete 5-stage structured translation process."""
    llm_client = client.copy()

    print_header(STEP2_PROMPT)
    step2(llm_client, target_lang)

    print_header(STEP3_PROMPT)
    step3(llm_client, target_lang)

    print_header(STEP4_PROMPT)
    step4(llm_client, target_lang)

    print_header(STEP5_PROMPT)
    step5(llm_client, target_lang)

    return llm_client.history

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='5-Stage Structured Translation for Low-Resource Languages')
    parser.add_argument('source_text', type=str,
                        help='Source text to translate (or @filename to read from file)')
    parser.add_argument('-r', '--reference', type=str, required=True,
                        help='Reference translation (or @filename to read from file)')
    parser.add_argument('-s', '--source-lang', type=str, required=True,
                        help='Source language name (e.g., Italian)')
    parser.add_argument('-t', '--target-lang', type=str, required=True,
                        help='Target language name (e.g., Malayalam)')
    parser.add_argument('-m', '--model', type=str, default='ollama:gpt-oss:120b',
                        help='Model to use for translation (default: ollama:gpt-oss:120b)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='XML file for translation log')
    parser.add_argument('--no-think', action='store_true',
                        help='Disable thinking mode')
    parser.add_argument('--temperature', type=float, default=0.1,
                        help='Sampling temperature for the model (default: 0.1)')
    args = parser.parse_args()

    source_text = read_text_input(args.source_text)
    reference = read_text_input(args.reference)
    source_lang = args.source_lang
    target_lang = args.target_lang
    output_file = args.output

    print("=" * 60)
    print("5-Stage Structured Translation")
    print("=" * 60)
    print(f"Source Language: {source_lang}")
    print(f"Target Language: {target_lang}")
    print(f"Model: {args.model}")
    print("=" * 60)
    print()

    llm_client = LLMClient(args.model, not args.no_think, temperature=args.temperature)
    print_header(STEP1_PROMPT)
    step1(llm_client, source_text, reference)
    translate(llm_client, target_lang)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(history_to_xml(llm_client.history))
        print(f"Final translation saved to {output_file}")
