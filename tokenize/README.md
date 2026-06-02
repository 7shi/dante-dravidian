# Tokenize - Italian Tokenizer

This directory is sourced from the following URL. Please refer there for details:

- https://github.com/7shi/dante-llm/tree/main/tokenize

## Purpose

This tool provides an Italian tokenizer designed for accurate validation of word tables. It specifically addresses issues with simple string splitting, such as ambiguous apostrophe handling and word boundaries.

## Features

- **Advanced Apostrophe Handling**: Correctly handles apostrophes in various positions:
  - End of word (e.g., `Tant’`)
  - Middle of word (e.g., `ch’i’`)
  - Beginning of word (e.g., `l’altre`, `’l`)
- **Punctuation Separation**: Treats punctuation marks as separate tokens.
- **Space Preservation**: Keeps whitespace as tokens to allow for exact text reconstruction.
- **Quote Disambiguation**: Distinguishes between apostrophes (elision) and closing quotation marks (U+2019) using context.

## Usage

To generate the tokenized files:

```bash
make
```

This runs `tokenizer.py` and populates the `inferno/`, `purgatorio/`, and `paradiso/` directories.

## File Structure

- `tokenizer.py`: The main tokenization script.
- `quote_cases.txt`: Input examples used for determining apostrophe vs. closing quote context.
- `quote_cases_converted.txt`: Normalized data used by the tokenizer for apostrophe handling.
- `inferno/`, `purgatorio/`, `paradiso/`: Directories containing the generated token lists.
- `Makefile`: Automation for running the tokenizer.
- `quotes.py`: Quote-span extractor (see below).
- `quotes/`: Generated XML files (`*.xml`, not committed; see `.gitignore`),
  alongside committed `*.tsv` speaker maps and a `ref/` sample.

## Quote extraction

The Italian source uses three nested quote levels:

| Delimiter | Unicode | Role |
|---|---|---|
| `«»` | U+00AB / U+00BB | Outer speech (dialogue in narrative) |
| `''` | U+2018 / U+2019 | Inner quote (within `«»` or standalone) |
| `""` | U+201C / U+201D | Innermost quote |

`U+2019` (`'`) is ambiguous: it is used both as a closing inner-quote and as an
elision apostrophe (e.g. `l'altra`, `ch'i'`). `tokenizer.py:convert_apostrophe`
resolves the ambiguity per line using pre-analyzed cases in `quote_cases.txt` /
`quote_cases_converted.txt`. After disambiguation, all three delimiter pairs are
balanced across the corpus (verified: zero mismatches, max nesting depth 2).

`quotes.py` reads the disambiguated source and extracts the full nesting tree
into one XML file per canticle (`quotes/inferno.xml`, etc.), where nesting is
expressed by element nesting. Quotes frequently span multiple lines (~67% of
spans) and can be nested, which is why per-line handling is insufficient.

Each `<q>` element carries:

- `id`: stable line-anchored identifier, e.g. `10:77` (canto:start-line).
  When multiple quotes open on the same line, an open-order suffix is appended:
  `10:77A`, `10:77B`, …
- `line`: the line range of the span (e.g. `45-126` or `12`).
- `marker`: the delimiter pair (e.g. `«»`, `''`, `""`).
- `head`: leading tokens after the opener — only present when the `id` carries
  a suffix and a hint is needed to identify the quote in the source.

The `speaker` of each quote is not produced here; it is filled in a separate
step that consumes this XML and writes to a committed file keyed by `id`.

To regenerate:

```bash
uv run python quotes.py inferno purgatorio paradiso
```
