"""Test for quick debugging."""
import os
from translate import *

# model = "ollama:gpt-oss:120b"
model = "groq:openai/gpt-oss-120b"
think = False

# Read test data
with open("tokenize/inferno/01.txt", 'r', encoding='utf-8') as f:
    it = [l.split("|")[0] for line in f if (l := line.strip())]
with open("en-norton/inferno-01.txt", 'r', encoding='utf-8') as f:
    en = [l for line in f if (l := line.strip())]

# Create output directory
os.makedirs("test", exist_ok=True)

# Process 3-line chunks
for i in range(3):
    # Print source text and reference
    if i:
        print()
    print("=" * 60)
    i3 = i * 3
    lines = it[i3:i3+3]
    source_text = ""
    for j in range(3):
        line = f"{i3+j+1} {lines[j]}"
        print(line)
        source_text += line + "\n"
    reference = en[i]
    print(reference)
    print("=" * 60)
    result = f"# Italian\n\n{source_text}\n# English\n\n{reference}\n"

    # Step 1
    client = LLMClient(model, think)
    xml_file = f"test/{i+1}-1.xml"
    if os.path.exists(xml_file):
        with open(xml_file, 'r', encoding='utf-8') as f:
            client.history = xml_to_history(f.read())
    else:
        print_header(STEP1_PROMPT)
        step1(client, source_text, reference)
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(history_to_xml(client.history))

    # Steps 2-5 and final translation for each target language
    for j, lang in enumerate(["Telugu", "Tamil", "Kannada", "Malayalam"]):
        result += f"\n# {lang}\n\n"
        xml_file = f"test/{i+1}-{lang}.xml"
        if os.path.exists(xml_file):
            with open(xml_file, 'r', encoding='utf-8') as f:
                history = xml_to_history(f.read())
        else:
            print()
            print("-" * 60)
            print(f"Testing translation to {lang}...")
            print("-" * 60)
            history = translate(client, lang)[2:]
            with open(f"test/{i+1}-{lang}.xml", 'w', encoding='utf-8') as f:
                f.write(history_to_xml(history))
        translated_text = history[-1]['content'].rstrip()
        for k, line in enumerate(translated_text.splitlines()):
            result += f"{i3+k+1} {line}\n"

    # Save combined result
    output_file = f"test/{i+1}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
