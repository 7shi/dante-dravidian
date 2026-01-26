# dante-dravidian

This project aims to translate Dante Alighieri's *Divine Comedy* from Italian into Dravidian languages (Telugu, Tamil, Kannada, and Malayalam) using a structured 5-stage translation process powered by Large Language Models (LLMs).

This project uses the following Italian text source:

- [La Divina Commedia di Dante: Complete by Dante Alighieri | Project Gutenberg](https://www.gutenberg.org/ebooks/1000)

## Methodology

**Note**: See [PROMPT.md](PROMPT.md) for the full methodology.

The project is based on a structured prompting methodology designed to overcome the limitations of LLMs when dealing with high-difficulty translations (classical texts, low-resource languages, and languages with significantly different word orders like SOV).

The core philosophy is the "Serialization" and "Fixation" of thought processes:
- **Context Lock**: Using an English reference to fix the meaning and disambiguate polysemous words.
- **Requirement Definition**: Explicitly defining grammatical requirements (cases, suffixes) for the target language.
- **Inventory & Assembly**: Separating vocabulary selection from sentence construction to prevent grammatical collapse.

### 5-Stage Structured Translation

The translation employs a rigorous 5-stage process designed for high-quality translation into low-resource languages:

1.  **Source-Reference Alignment & Semantic Analysis**: Aligns the Italian source with an English reference translation to identify precise contextual definitions for each token.
2.  **Morphosyntactic Requirement Definition**: Maps grammatical roles (Subject, Object, etc.) to the target language's case and suffix requirements.
3.  **Pre-assembled Lexical Inventory**: Selects target language lemmas and applies necessary agglutination (e.g., fusing case suffixes with nouns).
4.  **Slot-Based Syntactic Assembly**: Arranges the pre-assembled components into the target language's syntax (typically SOV for Dravidian languages).
5.  **Self-Correction via Back-Translation & Grammatical Check**: Back-translates the result to English to verify semantic integrity and performs final grammatical checks.

## Project Structure

### Directories

- [it/](it/): Italian source text management.
- [tokenize/](tokenize/): Italian tokenizer specialized for Dante's text.
- [en-norton/](en-norton/): Norton's English translation of *Inferno* Canto 1, used as the reference translation.
- [test/](test/): Contains translation logs and evaluation results for the first few lines of *Inferno*.

### Scripts

- [llm.py](llm.py): Wrapper for LLM interactions, including history management and XML serialization.
- [translate.py](translate.py): Implements the 5-stage translation process.
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

**Results and Evaluation**:

- `test/*.xml`: Detailed 5-stage translation logs for each chunk and language.
- `test/*.txt`: Combined final translations for comparison.
- `test/README.md`: A summary of the translations with critiques and rankings of the LLM's performance in each language (evaluated by GPT-5.2).

## Related Previous Projects

- [dante-llm](https://github.com/7shi/dante-llm) - A comparative study of Divine Comedy translation using multiple LLMs (Gemini 1.0 Pro, Gemma 3 27B, GPT-OSS 120B), verifying that locally-runnable models can match Gemini 1.0 Pro quality, with side-by-side comparisons of translations, word tables, and etymology analysis.
- [dante-gemini-25](https://github.com/7shi/dante-gemini-25) - A complete translation of Dante's Divine Comedy using Gemini 2.5 Pro, focusing specifically on English and Japanese translations across the three canticles. This project also includes illustrations generated using Nano Banana (Gemini 2.5 Flash Image Preview) in a classical Renaissance art style inspired by Gustave Doré.
- [dante-gemini](https://github.com/7shi/dante-gemini) - A multilingual exploration of Dante's Divine Comedy using Gemini 1.0 Pro, featuring detailed linguistic analysis of the opening lines in Italian, English, Hindi, Chinese, Ancient Greek, Arabic, Bengali and other languages with word-by-word breakdowns, grammatical details, and etymologies. 
- [dante-la-el](https://github.com/7shi/dante-la-el) - Originally started as a project to transcribe historical Latin and Ancient Greek translations of Dante's Divine Comedy, but evolved into an early LLM experimentation project when AI became the primary focus, exploring computational linguistic analysis methods.
