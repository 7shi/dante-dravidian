"""Test for quick debugging."""

from pathlib import Path
from llm import LLMClient, history_to_xml, xml_to_history
from translate import step1, translate, get_result

# MODEL = "ollama:gpt-oss:120b"
# MODEL = "groq:openai/gpt-oss-120b"
MODEL = "openrouter:openai/gpt-oss-120b:free"
THINK = False
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
testdir = Path("test")

# Read test data
with open("tokenize/inferno/01.txt", "r", encoding="utf-8") as f:
    it = [l.split("|")[0] for line in f if (l := line.strip())]
with open("en-norton/inferno-01.txt", "r", encoding="utf-8") as f:
    en = [l for line in f if (l := line.strip())]

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
    output_file = testdir / f"{i+1:02d}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (lang, text) in enumerate(result.items()):
            if i:
                f.write("\n")
            f.write(f"# {lang}\n\n{text}\n")
            result_all.setdefault(lang, []).append(text)

# Save results by language
alldir = testdir / "all"
alldir.mkdir(parents=True, exist_ok=True)
for lang, texts in result_all.items():
    if lang in ["Italian", "English"]:
        continue
    output_file = alldir / f"{lang}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(texts))
