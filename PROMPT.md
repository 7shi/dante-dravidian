# 4-Stage Translation Prompt (Local LLM)

This repo translates high-difficulty source text into target languages using a **four-step** prompt pipeline. The goal is to make the process:

- Meaning-stable (anchored to a reference translation)
- Hard to omit components (anti-omission)
- Debuggable (transparent inventories and checks)

## Quick principles

1. **Anchor meaning to a reference translation**: use it to resolve polysemy and idioms.
2. **Separate concerns**: meaning/roles → morphosyntax → inventory+assembly → verification.
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
   - Step 3 must list a clean inventory and assemble it; coverage failures indicate missing elements.
   - Step 4 must explicitly check meaning drift and report failures.

### Output discipline

- Follow the output formats exactly; do not add prose outside the specified formats.
- When a required format says “table only” or “no extra prose”, comply literally.

## Prompt templates

The following code blocks are the canonical prompts. `translate.py` extracts each block by the first line (`### Step N:`). Keep that first line unchanged.

```
### Step 1: Source-Reference Alignment & Semantic Analysis
Task: Align source tokens to the provided Reference Translation; pick in-context sense + grammatical role.
Output: (a) Interpretation Lock FIRST (one bullet per source line):
- Line <ID> <copy exact source line> => Locked Meaning (truth-conditions)
- If comparative/degree: define entities A,B, relation (>,<,≈), and degree (e.g., “slightly”).
- Include key predicate-argument structure and modifier attachment/scope (what modifies what) when it affects meaning.
- Note: A>B is equivalent to B<A; do not reverse the ordering.
(b) THEN ONE Markdown table consistent with the Lock:
- [Source Word] | [Morphology] | [Reference Equivalent] | [Contextual Definition] | [Grammatical Role]
Source Text:
{source_text}
Reference Translation (provided):
{reference}
```

```
### Step 2: Morphosyntactic Requirement Definition
Goal: For {target_lang}, specify per-token morphosyntax needed to realize the Step 1 Interpretation Lock.
Output: ONE Markdown table only (no prose).
Columns: [Source Word] | [Contextual Definition] | [Target Requirement]
In [Target Requirement]: make comparative ordering+degree explicit and add a 1-line literal back-translation check.
Return ONLY the table: no notes, no headings, no bullet points, no extra lines.
Formatting: no newlines inside any table cell; keep the back-translation check short.
```

```
### Step 3: Lexical Inventory & Syntactic Assembly
Task: For each source line, list ALL required lexical items from Step 2, then assemble into {target_lang}.
Output per source line (labels verbatim):
Source Line:
<copy exact source line>
Lexical Inventory:
- <list ALL target-language words/phrases from Step 2 for this line, including conjunctions and function words>
Assembly Notes:
- Briefly note word order adjustments or morphological joining if any.
Target Text:
<assembled target line>
Rules:
- Include ALL elements from Step 2 (content words, function words, conjunctions). Missing elements cause coverage failures.
- No new content words beyond Step 2 inventory.
- Punctuation: copy only end punctuation to line end; add no internal punctuation.
- Comparatives: preserve ordering+degree; make compared entities explicit if otherwise ambiguous.
```

```
### Step 4: Self-Correction via Back-Translation & Grammatical Check
For each line: verify Step3 Target Text vs Reference Translation + Step1 Locked Meaning; correct within-line only.
Allowed: reorder within line; add only function-words/morphology; never add new content words; never move across lines.
Punctuation: keep only end punctuation from source; no internal punctuation.
Meaning Drift includes wrong modifier attachment/scope.
Output per line bullets with EXACT fields (no extras): Line #, Target Text, Back-Translation, Reference Translation, Checks, Corrected Target Text (if any).
Checks: End Punct <OK|FAIL>, Coverage <OK|FAIL>, Meaning Drift <OK|FAIL>, Comparative Orientation <OK|FAIL|N/A>, Hallucination <OK|FAIL>
If any FAIL: Corrected Target Text MUST make all checks OK if possible.
Comparative Orientation: preserve ordering+degree; treat (A>B) ≡ (B<A) and (A<B) ≡ (B>A); FAIL only if ordering reversed or degree lost.
After all lines: if any line still FAILs, output UNVERIFIED with failing Line #s; otherwise do not output UNVERIFIED.
Output final {target_lang} text in ONE code block, line by line (no extra prose).
```
