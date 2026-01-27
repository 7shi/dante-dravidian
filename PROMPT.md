# 5-Stage Translation Prompt (Local LLM)

This repo translates high-difficulty source text into target languages using a **five-step** prompt pipeline. The goal is to make the process:

- Meaning-stable (anchored to a reference translation)
- Hard to omit components (anti-omission)
- Debuggable (transparent inventories and checks)

## Quick principles

1. **Anchor meaning to a reference translation**: use it to resolve polysemy and idioms.
2. **Separate concerns**: meaning/roles → morphosyntax → inventory → assembly → verification.
3. **No content invention**: do not add new content words to “fix” missing parts.
4. **Line fidelity** (for verse): keep line boundaries; copy end punctuation exactly.

## Policy (Non-Negotiable)

These rules apply to ALL steps.

### Do NOT write / do NOT assume

- Do NOT hardcode any specific target language, script, orthography, or typographic conventions.
   - No language-specific examples (no example sentences, particles, or punctuation from any particular language).
   - No rules that rely on a specific language’s word order or morphology.
- Do NOT hardcode any specific source text, work, author, or test case.
- Do NOT assume a particular reference language; treat the Reference Translation as “the provided reference translation” in its own language.
- Do NOT invent new content words to repair meaning, coverage, or fluency.
- Do NOT introduce new punctuation inside a line; only transfer end punctuation from the source line.

### Must do

- Keep line boundaries and the number of lines identical to the source.
- Keep end punctuation identical to the source line; do not normalize or “fix” punctuation.
- Make every intermediate artifact debuggable:
   - Step 3 must be a clean, deduplicated, placeable inventory.
   - Step 4 must include an explicit coverage check.
   - Step 5 must explicitly check meaning drift and report failures.

### Output discipline

- Follow the output formats exactly; do not add prose outside the specified formats.
- When a required format says “table only” or “no extra prose”, comply literally.

## Prompt templates

The following code blocks are the canonical prompts. `translate.py` extracts each block by the first line (`### Step N:`). Keep that first line unchanged.

```
### Step 1: Source-Reference Alignment & Semantic Analysis
Task: Align source tokens to the provided Reference Translation; pick the correct in-context sense and grammatical role.
Rules: be specific (no vague glosses); use the reference to resolve idioms/polysemy.
Output:
1) ONE Markdown table columns:
- [Source Word] | [Morphology] | [Reference Equivalent] | [Contextual Definition] | [Grammatical Role]
2) Interpretation Lock (bullets; one per source line):
- Line <ID> (copy exact source line): Locked Meaning: <truth-conditions>
- If comparative/degree: state subject, comparator, relation (>, <, ≈) and DO NOT flip.
Where <ID> is the leading integer at the start of that source line.
Source Text:
{source_text}
Reference Translation (provided):
{reference}
```

```
### Step 2: Morphosyntactic Requirement Definition
Goal: For {target_lang}, specify per-token morphosyntax needed to realize the Step 1 Interpretation Lock.
Requirements (ONE Markdown table):
- Columns: [Source Word] | [Contextual Definition] | [Target Requirement]
- In [Target Requirement], make comparative direction unambiguous and add a 1-line literal back-translation check.
Output: ONLY the table; no extra prose.
```

```
### Step 3: Pre-assembled Lexical Inventory
Create placeable {target_lang} components for Step 4.
Output ONLY bullet list; ONE LINE per bullet.
- Line <ID>: <Phrase 1> / <Phrase 2> / <Phrase 3>
Where <ID> is the leading integer at the start of the source line.
Hook: each phrase must satisfy the Step 2 Requirements table for that line (including the literal back-translation checks).
Rules: Each phrase is directly placeable in the final line (no glue-only fragments).
Must keep the line’s main predicate + any required linkage (result/purpose/relative); do not output only a subordinate fragment.
Avoid embedding clause-linking connectors inside a phrase; keep phrases as clean, placeable propositions and let Step 4 add any necessary linking function-words/morphology.
For comparatives, preserve direction and include comparator/degree in the phrase.
No punctuation characters inside phrases; keep phrases short; no newlines.
```

```
### Step 4: Slot-Based Syntactic Assembly
Assemble Step3 components into {target_lang} lines; keep the same number of lines.
Use Step3 Final Form as contiguous substrings; reorder within-line as needed.
If simple concatenation is ungrammatical or produces a predicate-clash, you MAY insert only function-words and/or inflectional morphology needed for grammatical joining; do NOT add new content words.
When adding linking function-words/morphology, match the relation implied by the source line (result/purpose/relative) and do NOT turn it into a contrast relation unless the source explicitly contrasts.
Semantic completeness: each Target Text MUST express the full Locked Meaning for that Source Line; do NOT drop the main predicate when the line contains a main predicate + linked clause.
Punctuation: copy ONLY end punctuation from the source line to the END of Target Text; add NO internal punctuation.
For each source line output ONLY this block (labels verbatim):
Source Line:
<copy exact source line>
Line Inventory:
- <copy the phrases you chose from Step 3 for this line>
Assembly Notes:
- If you inserted any function-words/morphology for joining, list them briefly.
Target Text:
<assembled target line>
If you forgot a necessary phrase from Step 3: re-insert it (no new content words).
```

```
### Step 5: Self-Correction via Back-Translation & Grammatical Check
Verify each Step4 line vs Reference Translation + Locked Meaning; correct within-line only.
Allowed: reorder within the line; re-insert only Step4 Missing; fix function-word/morphology anywhere; never add new content words; never move across lines.
Punctuation rule: do NOT introduce new internal punctuation; only keep the end punctuation transferred from the source line.
Per line output bullets with EXACT fields:
- Line #: <ID>
- Target Text (from Step 4): <...>
- Back-Translation (literal into the reference translation's language): <...>
- Reference Translation (line-aligned): <...>
- Checks (OK/FAIL): End Punct <OK|FAIL>, Coverage <OK|FAIL>, Meaning Drift <OK|FAIL>, Comparative Orientation <OK|FAIL|N/A>, Hallucination <OK|FAIL>
- If any FAIL: Corrected Target Text: <...>
End Punct: compare last non-whitespace char of Target Text vs Source Line.
Line # rule: <ID> is the leading integer at the start of that Source Line.
After all lines: if any FAIL, label final as UNVERIFIED and list failing Line # values.
Output final {target_lang} text in ONE code block, line by line.
```
