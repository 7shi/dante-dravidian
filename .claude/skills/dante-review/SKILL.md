---
name: dante-review
description: Review a Dante translation against the original Italian text
disable-model-invocation: true
argument-hint: <input_file> <output_file>
---

# Review Dante translation

Review a translation of Dante's Inferno Canto I against the original Italian text.

## Arguments
- `$ARGUMENTS`: `<input_file> <output_file>`

## Instructions

1. Read the original Italian text from `tokenize/inferno/01.txt`. This file is tokenized with `|` separators. Extract only the first field (the original text before the first `|`) from each line, and number them. Insert a blank line every 3 lines (after lines 3, 6, 9, ...) to separate tercets.

2. Read the target translation file specified by the user (`<input_file>`).

3. Compare the target translation against the original Italian text tercet by tercet. You are an expert translator and reviewer specializing in Dante's Inferno. Identify:
   - Mistranslations
   - Awkward literalisms
   - Grammatical errors
   - Stylistic mismatches

4. Output the full translation text with embedded review notes:
   - Do NOT correct the translation text itself. Keep it exactly as is.
   - Insert comments into the blank lines between tercets.
   - Format: `- Note: {Points of criticism}`.
   - Explicitly state why it is wrong and suggest corrections.
   - Do NOT list errors separately; embed them in the text.

5. Write the result to the output file (`<output_file>`).
