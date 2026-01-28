# 4-Stage Translation Prompt (Local LLM)

This repo translates high-difficulty source text into target languages using a **four-step** prompt pipeline.

## Design assumptions

- **Target runtime**: Local LLMs with limited instruction-following capability (e.g., 120B-parameter open-source models).
- **Goal**: Word-by-word literal translation to assist readers in understanding the original text (not publication-quality prose).
- **Simplicity over perfection**: Complex instructions confuse smaller models. We accept imperfect output and keep prompts minimal.

The goal is to make the process:

- Meaning-stable (anchored to a reference translation)
- Hard to omit components (anti-omission)
- Debuggable (transparent inventories and checks)

## Core rules

1. **Anchor to reference**: Use the reference translation to resolve polysemy and idioms.
2. **No content invention**: Never add new content words to fix meaning or fluency.
3. **Line fidelity**: Keep line count and end punctuation identical to source; no internal punctuation.
4. **Language-agnostic**: No hardcoded languages, scripts, or language-specific examples.
5. **Output discipline**: Follow formats exactly; no extra prose.

## Prompt templates

The following code blocks are the canonical prompts. `translate.py` extracts each block by the first line (`### Step N:`). Keep that first line unchanged.

```
### Step 1: Source-Reference Alignment & Semantic Analysis
Task: Align source tokens to the provided Reference Translation; pick in-context sense + grammatical role.
Output: (a) Interpretation Lock FIRST (one bullet per source line):
- Line <ID> <copy exact source line> => Locked Meaning (truth-conditions)
- If comparative/degree: define entities A,B, relation (>,<,≈), and degree (e.g., "slightly").
- Note: A>B is equivalent to B<A; do not reverse the ordering.
(b) THEN ONE Markdown table consistent with the Lock:
- [Source Word] | [Morphology] | [Reference Equivalent] | [Contextual Definition] | [Grammatical Role]
Source Text:
{source_text}
Reference Translation (provided):
{reference}
```

```
### Step 2: Direct Translation
Translate each source line into {target_lang}, guided by the Reference Translation and Step 1 analysis.
Output: ONE {target_lang} line per source line (preserve line count and end punctuation).
Rules:
- Follow the meaning from Reference Translation.
- For "so X that Y": keep resultative structure, do NOT convert to "because".
- No internal punctuation; copy only end punctuation from source.
```

```
### Step 3: Word Table & Coverage Check
Build a word table from Step 2 translation, mapping each source word to its target equivalent.
Output: ONE Markdown table (all lines combined).
Columns: [Source Word] | [Contextual Definition] | [Target Word/Phrase] | [Back-Translation] | [Status: OK/MISSING/WRONG]
After the table, list any MISSING or WRONG items.
```

```
### Step 4: Correction & Final Output
Fix any MISSING or WRONG items from Step 3. Reorder within line if needed; do not add new content words.
Output per line: Line #, Original Translation, Issues, Corrected Translation (if any).
Output final {target_lang} text in ONE code block, line by line (no extra prose).
```
