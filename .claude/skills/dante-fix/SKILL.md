---
name: dante-fix
description: Fix a Dante translation based on embedded review notes
disable-model-invocation: true
argument-hint: <input_file> <output_file>
---

# Fix Dante translation based on review notes

Fix a reviewed Dante translation by applying the embedded `- Note:` comments.

## Arguments
- `$ARGUMENTS`: `<input_file> <output_file>`

## Instructions

1. Read the reviewed translation file (`<input_file>`). This file contains translation lines with embedded `- Note:` comments between tercets.

2. Address each `- Note:` comment by modifying the corresponding lines:
   - Apply the suggested corrections from each note.
   - Remove the `- Note:` lines completely after applying the fix.
   - Maintain the literal translation style unless noted otherwise.

3. Ensure line numbers and structure remain consistent. The output should be clean text without any notes.

4. Write the corrected text to the output file (`<output_file>`).
