# Post-Translation Fix Pipeline

This directory contains a multi-stage pipeline that reviews, corrects, and structures the translations in `test/` using LLMs. The final output (with section headers) is used by `tts/` for audio generation.

## Pipeline Overview

The pipeline runs in two passes, each using a different model:

### Pass 1: Gemini 3.0 Pro (`gemini3pro/`)

Takes raw translations from `test/*.txt` and applies two stages:

1. **Review** (`1review/`) — Compares each translation against the original Italian, embedding `- Note:` comments between tercets to flag mistranslations, awkward literalisms, and grammatical errors.
2. **Fix** (`2fix/`) — Applies the review notes to produce corrected translations with the notes removed.

### Pass 2: GPT-5.2 (`gpt-5.2/`)

Takes the Gemini-corrected translations from `gemini3pro/2fix/` and applies four stages:

1. **Review** (`1review/`) — Second round of review against the Italian original.
2. **Fix** (`2fix/`) — Applies the second-round review notes.
3. **Quote** (`3quote/`) — Compares against the Italian to detect and fix missing quotation marks (especially closing quotes in dialogue passages).
4. **Split** (`4split/`) — Inserts section headers (e.g., `# The Dark Wood`, `# The Three Beasts`) translated into each target language, using the structure defined in `titles.json`.

## Files

- **`dante.py`** — Main script with subcommands: `review`, `fix`, `quote`, `split`. Uses `llm7shi.compat` for LLM calls.
- **`titles.json`** — Maps line numbers to English section titles for Canto 1 (used by the `split` subcommand to insert translated headers).
- **`Makefile`** — Top-level Makefile that runs both passes sequentially.

## Languages

All 20 target languages from `test/` are processed: Bengali, Bulgarian, Dutch, Esperanto, Estonian, French, German, Hindi, Interlingua, Japanese, Kannada, Malayalam, Polish, Portuguese, Serbian, Spanish, Tamil, Telugu, Turkish. English is additionally generated in some stages.

## Usage

```bash
# Run the full pipeline (both passes)
make

# Run a single language
make -C gpt-5.2 Japanese
```

Individual subcommands can also be run directly:

```bash
# Review a translation
uv run dante.py -m google:gemini-3-pro-preview --outdir out/ review input.txt

# Fix based on review notes
uv run dante.py -m openai:gpt-5.2 --outdir out/ fix reviewed.txt

# Fix missing quotation marks
uv run dante.py -m openai:gpt-5.2 --outdir out/ quote fixed.txt

# Add section headers
uv run dante.py -m openai:gpt-5.2 --outdir out/ split quoted.txt
```
