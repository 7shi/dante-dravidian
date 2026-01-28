"""Test for quick debugging."""
import os
from llm import LLMClient, history_to_xml, xml_to_history
from translate import step1, translate, get_result

# model = "ollama:gpt-oss:120b"
# model = "groq:openai/gpt-oss-120b"
model = "openrouter:openai/gpt-oss-120b:free"
think = False
temperature = 0.1

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

# Read test data
with open("tokenize/inferno/01.txt", "r", encoding="utf-8") as f:
    it = [l.split("|")[0] for line in f if (l := line.strip())]
with open("en-norton/inferno-01.txt", "r", encoding="utf-8") as f:
    en = [l for line in f if (l := line.strip())]

# Create output directory
os.makedirs("test", exist_ok=True)

# Process 3-line chunks
result_all = {}
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
        if j:
            source_text += "\n"
        source_text += line
    reference = en[i]
    print(reference)
    print("=" * 60)
    result = {"Italian": source_text, "English": reference}

    # Step 1
    client = LLMClient(model, think, temperature=temperature)
    xml_file = f"test/{i+1}-1.xml"
    if os.path.exists(xml_file):
        with open(xml_file, 'r', encoding='utf-8') as f:
            client.history = xml_to_history(f.read())
    else:
        step1(client, source_text, reference)
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(history_to_xml(client.history))

    # Steps 2-5 and final translation for each target language
    for j, lang in enumerate(LANGUAGES):
        xml_file = f"test/{i+1}-{lang}.xml"
        if os.path.exists(xml_file):
            with open(xml_file, 'r', encoding='utf-8') as f:
                history = xml_to_history(f.read())
            text = get_result(history).rstrip()
        else:
            print()
            print("-" * 60)
            print(f"Testing translation to {lang}...")
            print("-" * 60)
            history, text = translate(client, lang)
            with open(f"test/{i+1}-{lang}.xml", 'w', encoding='utf-8') as f:
                f.write(history_to_xml(history[2:]))
        lines = [f"{i3+k+1} {line}" for k, line in enumerate(text.splitlines())]
        result[lang] = "\n".join(lines)

    # Save combined result
    output_file = f"test/{i+1}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (lang, text) in enumerate(result.items()):
            if i:
                f.write("\n")
            f.write(f"# {lang}\n\n{text}\n")
            result_all.setdefault(lang, []).append(text)

# Save all results
with open("test/all.txt", 'w', encoding='utf-8') as f:
    for i, (lang, texts) in enumerate(result_all.items()):
        sep = " " if lang == "English" else "\n\n"
        if i:
            f.write("\n")
        f.write(f"# {lang}\n\n{sep.join(texts)}\n")
