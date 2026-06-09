# Architecture: three-repository structure

This project is part of a three-repository set. The split was made because the formalization
work (`scenes → markup → reading → bullets → tags → knowledge graph`) diverged from the translation
goal, and the shared source text became a real, queryable corpus rather than a directory of
files coupled by relative paths.

## Repository layout

```
             dante-corpus  (shared, queryable "DB": library + CLI)
               ▲                         ▲
      depends  │                         │  depends
               │                         │
    dante-dravidian (this repo)     dante-analyze
    translation                     formalization / knowledge graph
```

- **dante-corpus** — the shared corpus as a **library + thin CLI**. Serves source text and
  tokens as an externally accessible "DB". Runtime deps: none (pure Python).
- **dante-dravidian** (this repo) — the translation project. Depends on dante-corpus via an
  editable path dep; `test.py` reads canto text through the `dante_corpus` API.
- **dante-analyze** — the formalization / KG layer. Depends on **dante-corpus + `llm7shi`**
  (both runtime — all LLM calls go through the shared `scenelib.call_llm` gateway).

## The boundary

The split line falls **right after scene segmentation**:

- **dante-corpus = deterministic / mechanical views**: normalized source text, tokens, and
  the quote-span tree. No LLM at query time.
- **dante-analyze = the LLM / semantic layer**: markup, reading, bullets, tags, and the
  downstream speaker / edge / knowledge-graph work.

Coupling: analysis scripts import `dante_corpus` (inputs) + `llm7shi` (model), never the
translation `llm.py`; translation imports nothing from the analysis layer. The only forward
link is conceptual and future: the KG's speaker / edge data feeds the translation **context
lock** (see [PLAN.md](PLAN.md) §3).

## Integration rule

Consumers **read corpus data through the `dante_corpus` API** (`dc.canto(...)`,
`.lines()/.quotes()`, `dc.ref(...)`), never by reading copied corpus files by
relative path, and **write their own outputs locally**.

## End goal

Ultimately the translation will be **re-architected to leverage the knowledge graph** produced
by dante-analyze (beyond just the context lock). That redesign is explicitly out of scope for
the current state — recorded only to fix direction so the repository structure does not block
that future.

## Deferred TODOs

- **Translation should consume dante-analyze's referent tagging instead of re-deriving it.**
  [PROMPT.md](PROMPT.md) Step 1 currently does its own per-word analysis. The analysis layer
  already produces pronoun/person markup and per-tag name resolution. Rework the translation
  prompt to **reuse that referent tagging**. Part of the KG-driven redesign above; later,
  separate work.
