# dante-dravidian

This project aims to translate Dante Alighieri's *Divine Comedy* from Italian into Dravidian languages (Telugu, Tamil, Kannada, and Malayalam) using a structured 4-stage translation process powered by Large Language Models (LLMs).

**Note**: This project originally began with a focus on SOV agglutinative languages, particularly Dravidian languages. However, the current prompt framework contains no language-specific instructions and is designed as a general-purpose methodology applicable to any source-target language pair.

This project uses the following Italian text source:

- [La Divina Commedia di Dante: Complete by Dante Alighieri | Project Gutenberg](https://www.gutenberg.org/ebooks/1000)

## Methodology

This project targets **local LLMs** (e.g., GPT-OSS 120B) with limited instruction-following capability. Complex multi-step instructions often cause smaller models to lose track of requirements or produce malformed output.

The original approach used a bottom-up method: build a word table first, then assemble words into sentences. However, this led to grammatical collapse, especially for complex syntactic structures like nested relative clauses and purpose clauses. The problem is that assembling words into proper word order is not part of normal LLM training. LLMs are trained on natural text generation and translation, not on puzzle-like word rearrangement tasks.

The current top-down approach (translate first → verify coverage → fix errors) aligns with what LLMs actually learned during training:

1. **Translation**: Abundantly present in training data
2. **Coverage checking**: A comparison/verification task
3. **Correction**: An editing task LLMs handle well

This leverages the model's natural translation ability while using structured checks to catch omissions.

### 4-Stage Structured Translation

1.  **Source-Reference Alignment & Semantic Analysis**: Aligns the Italian source with an English reference translation to establish a **Context Lock** that fixes meaning and disambiguates polysemous words. Produces an "Interpretation Lock" (truth-conditions per line) and a token-by-token alignment table with contextual definitions.
2.  **Direct Translation**: Translates each source line into the target language, guided by the reference translation and Step 1 analysis. This **translate-first approach** lets the model produce natural word order rather than constructing it from individual words. Preserves line count and end punctuation.
3.  **Word Table & Coverage Check**: Builds a word table *after* translation to verify completeness, mapping each source word to its target equivalent with back-translation and status (OK/MISSING/WRONG). Lists any items requiring correction.
4.  **Correction & Final Output**: Fixes MISSING or WRONG items from Step 3. Outputs the corrected translation in a single code block.

**Note**: See [PROMPT.md](PROMPT.md) for the full prompts and [test/README.md](test/README.md) for translation results and analysis.

## Project Structure

### Directories

- [it/](it/): Italian source text management.
- [tokenize/](tokenize/): Italian tokenizer specialized for Dante's text.
- [en-norton/](en-norton/): Norton's English translation of *Inferno* Canto 1, used as the reference translation.
- [test/](test/): Contains translation logs and evaluation results for the first few lines of *Inferno*.
- [fix/](fix/): Post-translation fix pipeline that reviews, corrects, and adds section headers to translations using LLMs (e.g., Gemini 3.0 Pro, GPT-5.2).
- [tts/](tts/): Text-to-Speech pipeline that generates audio readings of *Inferno* Canto 1 translations using Google's Gemini TTS model.

### Scripts

- [llm.py](llm.py): Wrapper for LLM interactions, including history management and XML serialization.
- [translate.py](translate.py): Implements the 4-stage translation process.
- [test.py](test.py): Script for testing and debugging the translation pipeline.

## Usage

### Preparation

Ensure you have `uv` installed. First, prepare the Italian source text:

```bash
uv sync
cd it
make
make split
```

Then, tokenize the text:

```bash
cd ../tokenize
make
```

### Test

A script for quick debugging and verification of the translation pipeline. It processes the source text in 3-line chunks and generates translations for all four target Dravidian languages.

```bash
uv run test.py
```

**Results**:

- `test/*.xml`: Detailed 4-stage translation logs for each chunk and language.
- `test/*.txt`: Combined final translations for comparison.

## Related Previous Projects

- [dante-llm](https://github.com/7shi/dante-llm) - A comparative study of Divine Comedy translation using multiple LLMs (Gemini 1.0 Pro, Gemma 3 27B, GPT-OSS 120B), verifying that locally-runnable models can match Gemini 1.0 Pro quality, with side-by-side comparisons of translations, word tables, and etymology analysis.
- [dante-gemini-25](https://github.com/7shi/dante-gemini-25) - A complete translation of Dante's Divine Comedy using Gemini 2.5 Pro, focusing specifically on English and Japanese translations across the three canticles. This project also includes illustrations generated using Nano Banana (Gemini 2.5 Flash Image Preview) in a classical Renaissance art style inspired by Gustave Doré.
- [dante-gemini](https://github.com/7shi/dante-gemini) - A multilingual exploration of Dante's Divine Comedy using Gemini 1.0 Pro, featuring detailed linguistic analysis of the opening lines in Italian, English, Hindi, Chinese, Ancient Greek, Arabic, Bengali and other languages with word-by-word breakdowns, grammatical details, and etymologies. 
- [dante-la-el](https://github.com/7shi/dante-la-el) - Originally started as a project to transcribe historical Latin and Ancient Greek translations of Dante's Divine Comedy, but evolved into an early LLM experimentation project when AI became the primary focus, exploring computational linguistic analysis methods.
