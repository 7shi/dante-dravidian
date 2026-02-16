# TTS (Text-to-Speech) Pipeline

This directory contains a TTS pipeline that generates audio readings of Dante's *Inferno* Canto 1 translations using Google's Gemini TTS model.

## Overview

The pipeline converts translation text files into WAV audio files:

1. **`txt2wav.py`** — Splits a text file into individual lines and generates per-line WAV files via the Gemini TTS API.
2. **`normalize_combine.py`** — Normalizes audio levels and concatenates per-line WAVs into a single output file.
3. **`Makefile`** — Orchestrates the full pipeline for all 20 languages plus Italian and English.

## Text Format

Each text file uses numbered lines with section headers:

```
# Section Title

1 First line of the translation
2 Second line of the translation
...
```

Line numbers are stripped before TTS processing. Section headers (lines starting with `#`) serve as structural markers.

## Handling Relative Clauses in Agglutinative Languages

When adapting translations for TTS in agglutinative languages (Japanese, Korean, Dravidian languages, Turkish, etc.), relative clauses pose a structural challenge. Indo-European languages use relative pronouns (`che`, `which`, `who`) to introduce subordinate clauses on separate lines, but agglutinative languages lack relative pronouns entirely — they use prenominal modifiers or participial constructions instead.

### The Problem

In Dante's Italian, a relative clause often occupies its own line:

```
una lonza leggera e presta molto,    (a leopard, light and very swift,)
che di pel macolato era coverta;     (which was covered with spotted fur;)
```

A naive translation into Japanese might force the relative clause into a subject-predicate structure:

```
32 軽くてとてもすばやい豹が、        (a light and very swift leopard [SUBJ],)
33 斑点のある毛皮に覆われていた；    (was covered with spotted fur;)
```

This misrepresents the original: the leopard is not the subject of "was covered" — it is the object of "behold" (line 31). The relative clause is merely a parenthetical description.

### The Dash Technique

Use em dashes (――) to mark appositive insertions, preserving line-by-line correspondence with the source while signaling that the clause is a parenthetical modifier, not a main predicate:

```
31 すると見よ、登りの始まりあたり、   (And behold, almost at the start of the climb,)
32 軽くてとてもすばやい豹――          (a leopard, light and very swift —)
33 斑点のある毛皮に覆われたものを；  (the one covered with spotted fur;)
```

The dash after the noun (line 32) signals that what follows is a parenthetical description, not a new clause. This eliminates the false subject-predicate reading.

### Another Example: Disambiguating Repeated Pronouns

When a relative clause modifies a noun embedded within a line, a literal translation may require repeating a pronoun with a different referent:

```
Italian:
  vestite già de' raggi del pianeta       (already clothed with the rays of the planet)
  che mena dritto altrui per ogne calle.  (which leads everyone straight along every path.)

Problematic:
  17 それはすでに惑星（太陽）の光線に覆われていた、  (It was already covered...)
  18 それはあらゆる道に沿って人をまっすぐ導くもの。  (It leads people straight...)
```

The pronoun それは (it) appears twice with different referents (line 17 = the hill's shoulders, line 18 = the planet/sun), creating ambiguity. The dash technique resolves this:

```
  17 それはすでに惑星（太陽）の光線に覆われていた――  (It was already covered... —)
  18 あらゆる道に沿って人をまっすぐ導くものの。      (the one that leads people straight...)
```

The dash makes line 18 an appositive to 惑星（太陽） (the planet/sun), eliminating the ambiguous pronoun.

### Applicability

This technique is broadly applicable to any agglutinative or SOV language that lacks relative pronouns, including:

- **Japanese** (日本語)
- **Korean** (한국어)
- **Dravidian languages** (Tamil, Telugu, Kannada, Malayalam)
- **Turkic languages** (Turkish, etc.)
- **Uralic languages** (Estonian, Finnish, Hungarian)

The key insight is that em dashes function as a language-neutral bracketing device: they signal "this is a modifier of what came before" without requiring the syntactic machinery of relative pronouns. This allows line-for-line correspondence with Indo-European source texts while producing natural target-language phrasing.
