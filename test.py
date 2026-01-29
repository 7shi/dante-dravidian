"""Test for quick debugging."""
MODEL = "ollama:gpt-oss:120b"
TEMPERATURE = 0.1
LANGUAGES = [
    # Dravidian languages
    "Telugu", "Tamil", "Kannada", "Malayalam",

    # Agglutinative non-Dravidian language
    "Japanese",

    # Romance languages
    "French", "Spanish", "Portuguese",

    # Constructed language
    "Esperanto",
]

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(description='Test translation system')
parser.add_argument('-m', '--model', default=MODEL,
                    help=f'Model to use (default: {MODEL})')
parser.add_argument('--start', type=int, default=1,
                    help='Start index for processing chunks (default: 1, 1-origin)')
parser.add_argument('--end', type=int, default=None,
                    help='End index for processing chunks (default: all)')
parser.add_argument('--step1', action='store_true',
                    help='Run step1 only (skip translation steps)')
parser.add_argument('--no-think', action='store_true',
                    help='Disable thinking mode')
parser.add_argument('-t', '--temperature', type=float, default=TEMPERATURE,
                    help=f'Temperature for LLM (default: {TEMPERATURE})')
parser.add_argument('-l', '--languages', default=None,
                    help='Comma-separated list of languages to translate to')
args = parser.parse_args()

MODEL = args.model
THINK = not args.no_think
TEMPERATURE = args.temperature
if args.languages is not None:
    LANGUAGES = [lang.strip() for lang in args.languages.split(',')]

import math
from pathlib import Path
from llm import LLMClient, history_to_xml, xml_to_history
from translate import step1, translate, get_result

# Read test data
with open("tokenize/inferno/01.txt", "r", encoding="utf-8") as f:
    it = [l.split("|")[0] for line in f if (l := line.strip())]
with open("en-norton/inferno-01.txt", "r", encoding="utf-8") as f:
    en = [l for line in f if (l := line.strip())]

# Determine range of chunks to process
source_count = math.ceil(len(it) / 3)
start = args.start - 1
end = args.end or source_count
if not (0 <= start < end <= source_count):
    raise ValueError(f"Invalid start/end range: {args.start} to {args.end}")

# Process 3-line chunks
testdir = Path("test")
result_all = {}
for i in range(start, end):
    # Print source text and reference
    if i:
        print()
    print("=" * 60)
    i3 = i * 3
    lines = it[i3:i3+3]
    source_text = ""
    for j in range(len(lines)):
        line = f"{i3+j+1} {lines[j]}"
        print(line)
        if j:
            source_text += "\n"
        source_text += line
    reference = en[i]
    print(reference)
    print("=" * 60)
    result = {"Italian": source_text, "English": reference}

    # Create output directory
    outdir = testdir / f"{i+1:02d}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Step 1
    client = LLMClient(MODEL, THINK, temperature=TEMPERATURE)
    xml_file = outdir / "_step1.xml"
    if xml_file.exists():
        client.history = xml_to_history(xml_file.read_text(encoding="utf-8"))
    else:
        step1(client, source_text, reference)
        xml_file.write_text(history_to_xml(client.history), encoding="utf-8")

    # Skip translation steps if --step1 is specified
    if args.step1:
        continue

    # Steps 2-5 and final translation for each target language
    for j, lang in enumerate(LANGUAGES):
        xml_file = outdir / f"{lang}.xml"
        if xml_file.exists():
            history = xml_to_history(xml_file.read_text(encoding="utf-8"))
            text = get_result(history).rstrip()
        else:
            print()
            print("-" * 60)
            print(f"Testing translation to {lang}...")
            print("-" * 60)
            history, text = translate(client, lang)
            xml_file.write_text(history_to_xml(history[2:]), encoding="utf-8")
        lines = [f"{i3+k+1} {line}" for k, line in enumerate(text.splitlines())]
        result[lang] = "\n".join(lines)

    # Save combined result
    output_file = outdir / f"_all.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (lang, text) in enumerate(result.items()):
            if i:
                f.write("\n")
            f.write(f"# {lang}\n\n{text}\n")
            result_all.setdefault(lang, []).append(text)

# Save results by language
if not args.step1:
    alldir = testdir / "all"
    alldir.mkdir(parents=True, exist_ok=True)
    for lang, texts in result_all.items():
        if lang in ["Italian", "English"]:
            continue
        output_file = alldir / f"{lang}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(texts))
