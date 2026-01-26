import argparse
from llm import LLMClient, history_to_xml

STEP1_PROMPT = """
### Step 1: Source-Reference Alignment & Semantic Analysis

Perform a word-by-word alignment between the Source Text and the Reference Translation.

Goal: Identify the specific English meaning and precise semantic definition for each Source token in this context.

Instructions:
1. Use Reference for Context: Use the Reference Translation to disambiguate polysemous words.
2. Define Semantics: For the [Contextual Definition] column, write the specific dictionary definition that applies to this context.
   - Example: For "trattar", do not just write "treat". Write "to discuss; to deal with a subject".
   - Example: For "ben", write "the good; virtue".
3. Analyze Grammar: Identify the grammatical role (Subject, Direct Object, etc.).

Table Columns:
- [Source Word]
- [Morphology] (Lemma, POS)
- [English Equivalent] (Literal word aligned with Source)
- [Contextual Definition] (Specific dictionary sense used here)
- [Grammatical Role] (Syntactic function)

Source Text:
{source_text}

Reference Translation (English):
{reference}
""".strip()

STEP2_PROMPT = """
### Step 2: Morphosyntactic Requirement Definition

Based on the alignment and roles from Step 1, define the grammatical requirements for {target_lang}.

Tasks:
1. Map Case/Suffix: Define the Target Language requirement based on the [Grammatical Role] identified in Step 1.
   - If Role is Direct Object -> Assign Accusative Case.
   - If Role is Prepositional Phrase -> Determine the Suffix (e.g., Locative).
2. Tense/Mood Mapping: Map the Source Tense to the appropriate Target Tense.

Output Format (Table):
- [Source Word]
- [Contextual Definition] (from Step 1)
- [Target Requirement] (e.g., "Accusative case (-e)", "Suffix (-il) on next noun")
""".strip()

STEP3_PROMPT = """
### Step 3: Pre-assembled Lexical Inventory

Create a list of {target_lang} components ready for assembly.

STRICT RULES:
1. Agglutination: If Step 2 identified a word as a Suffix (e.g., "of", "in"), do NOT list it separately. Fuse it immediately with the head noun.
   - Bad: [forest] [in]
   - Good: [forest-in] (e.g., kattil)
2. Case Verification: Ensure the grammatical role from Step 2 is respected.
   - Direct Object: Must use Accusative form.
3. Lexical Sanity: Ensure words are standard and natural. Verify that the chosen {target_lang} word matches the Contextual Definition.

Table Columns:
- [Source Word]
- [Contextual Definition] (English dictionary definition/description of the meaning in this context. Do not just translate the word; explain it.)
- [Target Lemma]
- [Final Agglutinated Form] (The fully inflected word to be used in the sentence)
""".strip()

STEP4_PROMPT = """
### Step 4: Slot-Based Syntactic Assembly

Arrange the components from Step 3 into a strictly literal {target_lang} sentence.

Universal Rules:
1. Line Integrity: Do not merge the text into a single paragraph. Translate exactly one Source line at a time. The output must have the same number of lines as the Source.
2. Punctuation Transfer: Strictly copy punctuation marks (commas, periods, exclamation marks) from the end of the Source Line to the end of the Target Line. Do not add artificial periods if the source does not have them.
3. Transparency: Explicitly show which components are used for each line to allow debugging.

Target Language Specific Rules (for SOV/Agglutinative languages like {target_lang}):
4. Slot Filling: Inside each line, arrange components into the following order: [Subject] + [Time/Place/Manner Adverbials] + [Object] + [Verb]
5. Head-Final Modifiers: Ensure adjectives and genitives are placed before the noun they modify. ([Adjective/Genitive] + [Noun])
6. No New Agglutination: Use the Final Agglutinated Forms from Step 3 exactly as they are. Do not separate suffixes again.

Final Output Format:
For each line, provide:
- Source Line: [Original Text]
- Component Mapping: [List of components used from Step 3 in their new order]
- Assembly Logic: [Brief explanation of word order changes or connections]
- Target Text: [Final translation for this line]
""".strip()

STEP5_PROMPT = """
### Step 5: Self-Correction via Back-Translation & Grammatical Check

Perform the verification and display the results for each step:

Table Columns:
- [Line #]
- [Target Text] (Copy the final text from Step 4)
- [Back-Translation] (Literal English)
- [Source Context] (Original Source text)
- [Verification Result] (OK / Correction Needed)

Rules:
1. Verify Meaning: Compare Back-Translation with the "Locked Meaning" from Step 1.
2. Verify Structure: Check against [Source Context] to ensure no structural elements are ignored.
3. Correction: If there is a mismatch or grammatical error, output a corrected version.
   - Constraint: Do NOT reorder words across lines. Corrections must happen strictly within each line.
4. Final Output: Present the final, verified {target_lang} text in a code block, separated line by line.
""".strip()

FINAL_PROMPT = """
Based on the verification in Step 5, output ONLY the final {target_lang} translation.
No explanations, no tables, just the translated text line by line.
""".strip()

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

def extract_final(llm_client, target_lang):
    """Extract final translation from verified results."""
    prompt = FINAL_PROMPT.format(target_lang=target_lang)
    return llm_client.call(prompt)

def print_header(prompt):
    """Print header for each step."""
    first_line = prompt.strip().splitlines()[0]
    print()
    print(first_line)
    print()

def translate(client, target_lang):
    """Run the complete 5-stage structured translation process."""
    llm_client = LLMClient(client.model, client.think)
    llm_client.history = client.history.copy()

    print_header(STEP2_PROMPT)
    step2(llm_client, target_lang)

    print_header(STEP3_PROMPT)
    step3(llm_client, target_lang)

    print_header(STEP4_PROMPT)
    step4(llm_client, target_lang)

    print_header(STEP5_PROMPT)
    step5(llm_client, target_lang)

    print()
    print("### FINAL TRANSLATION")
    print()
    extract_final(llm_client, target_lang)

    return llm_client.history

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='5-Stage Structured Translation for Low-Resource Languages')
    parser.add_argument('source_text', type=str,
                        help='Source text to translate (or @filename to read from file)')
    parser.add_argument('-r', '--reference', type=str, required=True,
                        help='Reference translation in English (or @filename to read from file)')
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

    llm_client = LLMClient(args.model, not args.no_think)
    final_translation = translate(llm_client, source_lang, target_lang, source_text, reference)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(history_to_xml(llm_client.history))
        print(f"Final translation saved to {output_file}")
