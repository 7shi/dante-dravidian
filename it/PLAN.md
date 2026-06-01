# Plan: Scene breakdowns as translation units, a context lock, and a digest

## Background and intent

`scene.py` splits each canticle into scenes (see [README.md](README.md)). The
real product of the split is the set of **translation units**: stable,
source-aligned line ranges that are large enough to give the translator context
but small enough to keep a local LLM on track.

The per-scene **summaries are incidental and, in practice, unnecessary** — a
by-product of asking the model to reason about boundaries. Translation re-fixes
the context anyway (now via the **context lock**, §3), so the split-time summary
is not reused and can be dropped. Proofreading the generated summaries was
therefore **not strictly required**; it was done proactively, to surface the
model's error tendencies *before* translation, so those traps can be guarded
against (see §2).

Two downstream products are planned:

1. **Translation** driven by the scene split, one unit at a time, defended by a
   per-scene context lock (§3) that runs as pre-processing before the existing
   4-stage pipeline (§5).
2. A **digest edition** built on the same scene split — coarser than a full
   translation but finer than a line-by-line read, readable as a continuous
   story (§4).

## 1. Scene splits as translation units

- Translate scene by scene rather than canto by canto. Each scene is a
  self-contained dramatic beat (one place / speaker / action / topic), so the
  model has just enough context without drowning in a 140-line canto.
- The line ranges are contiguous and validated (no gaps/overlaps; full coverage
  against the source), so they can drive the 4-stage pipeline (`translate.py`)
  unit by unit while guaranteeing nothing is skipped.
- The context that each scene needs (who speaks, which realm, who "this light"
  is) is fixed up front in the **context lock** (§3) rather than left to the
  translator to re-derive implicitly. The split-time summaries are **not
  authoritative** and are not an input — proofreading found real factual errors
  in them (catalogued in the correction tables in [README.md](README.md)); the
  source text is always the final arbiter.

## 2. What to watch for during translation

These are drawn from the error tendencies seen while proofreading the generated
summaries (Inferno, Purgatorio, Paradiso). The local model failed in consistent,
predictable ways; the same traps apply to translation, so guard against them
explicitly. **Every correction in the README tables maps to one of these traps**,
and they are exactly what the context lock (§3) is designed to pin down.

| Trap | What goes wrong | Guard |
|---|---|---|
| **Speaker / referent misidentification** (most common, most serious) | The model assigns lines to the wrong person, or confuses who is being referred to: Justinian→"Farinata", Beatrice↔Matelda, Beatrice↔"the Sphinx", Charon↔the heaven-sent messenger, Chiron↔Nessus, Nicholas III↔Boniface. | Lock the speaker/addressee for each scene before translating; carry an explicit "who speaks, who is addressed, who is described" note through the unit. |
| **Simile read as literal identity** | "X, *like* the shade of Anchises, …" was collapsed into "the shade of Anchises". The vehicle of a comparison gets mistaken for the actual character. | Watch the comparison markers (`come`, `sì … come`, `qual`, `tale`, `non altrimenti`); the compared figure is imagery, not a character entering the scene. |
| **A referent self-identifying vs. pointing to another** | Folco, speaking, was made to "identify itself as Rahab" when he was pointing to a *neighboring* soul. | Track deixis carefully: who is "I", who is "this light / that one". A speaker naming someone is usually naming a third party. |
| **Reference point misread as subject** | "whence thy lady sent Virgil" (= Limbo, a *place* marker) became "a history of Virgil"; Adam's own 4,302-year wait was lost. | A proper name used to fix a location/time is not the topic. Identify the grammatical subject of the passage, not the most famous noun in it. |
| **Mistranslated domain nouns** | `aguglia` ("eagle") rendered as "needle" — repeatedly, in different cantos. | Keep a domain glossary (§3) and translate recurring technical/poetic terms consistently. |
| **Realm / topography slips** | "circle" vs "terrace" vs "heaven/sphere"; Inferno / Purgatory / Limbo confused. Each canticle has its own geography. | Anchor every scene to the correct realm: Inferno = **circles**; Purgatorio = **terraces** (Ante-Purgatory, the Earthly Paradise); Paradiso = **heavens / spheres** (Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn, Fixed Stars, Primum Mobile, Empyrean). |
| **Theological / scriptural over-reading** | "chosen *from* the cross for the great office" (John entrusted with Mary) became "died on the cross" — collapsing John into Christ. | Do not "complete" allusions from prior knowledge; translate what the line says. Be especially careful around Christ, the apostles, and scripture quotations. |
| **Garbled or invented proper names** | "Rinvieri", "Forese Giunchi", "Anchimates" — names mangled or given spurious surnames. | Copy proper names exactly from the source; never invent a surname. Verify any name against the source line before committing it. |
| **Latin / scripture tags** | Embedded Latin (`Diligite iustitiam`, `Sperent in te`, `Ave Maria`) is easy to drop or paraphrase. | Preserve embedded Latin/scripture verbatim; do not silently translate or omit it. |

## 3. The context lock (a per-scene TOML skeleton)

The single mechanism that defends against the §2 traps is a **context lock**: a
per-scene record, produced as **pre-processing before translation**, that fixes
**identity only** — who speaks, where we are, who "this light" is — and nothing
else. It deliberately **does not contain the source's meaning or a paraphrase**;
it is a skeleton to prevent misinterpretation, not a translation. Each entry
carries a `basis` quote so it is verifiable against the source, exactly like the
README correction tables.

### Fields (per scene)

| Field | Required | Defends against (§2) |
|---|---|---|
| `lines` | ✓ | anchor |
| `location` | ✓ | realm / topography slips |
| `cohort` | optional | wrong class of souls |
| `cast` | ✓ | character roster, creature/agent identity, garbled names, first-appearance / cross-canticle bleed |
| `speaker`, `addressee` | when spoken | speaker misidentification |
| `flags` (e.g. `misnames-addressee`) | optional | dramatic irony (a speaker mis-naming the addressee) |
| `refer` (`phrase` → `resolves`, with `note`) | optional | deixis / periphrasis; self vs. third party; reference-point-as-subject |
| `relations` (`who`/`role`/`of`) | optional | kinship / role errors |
| `simile` (`vehicle`, with `note`) | optional | simile vehicle mistaken for a character |
| `basis` | ✓ | verification |

Recurring items that are not scene-specific live in a **single shared glossary**
(e.g. `it/gloss.toml`): fixed renderings of domain terms (`aguglia` = eagle),
the canticle-specific realm vocabulary, and the standard spelling of recurring
proper names (e.g. Cassio → Cassius). Scenes only reference it; they do not
repeat it.

### Format and layout

- **TOML**, one file per canto, placed next to the source (e.g.
  `it/inferno/01.toml` beside `it/inferno/01.txt`), so source + breakdown + lock
  form a consistent per-canto bundle. (A future cleanup may also distribute the
  scene breakdown per canto as JSON; noted, not yet decided.)
- Scenes are an array of tables (`[[scene]]`); `refer` and `simile` are arrays of
  inline tables, which stay readable and hand-editable.

### Production: LLM extraction + manual verification

1. For each scene range, a focused extraction prompt asks only for the lock
   fields ("identify the speaker, addressee, location, cast, referents, and
   similes for these lines") — a narrow task the model handles far more reliably
   than doing it implicitly while translating.
2. The draft is checked against the source and hand-corrected, mirroring the
   README correction workflow; the `basis` quotes make this fast.
3. The verified lock feeds translation as the pipeline's "Step 0" (§5).

### Reference sample

[`ref/inferno-01.toml`](ref/inferno-01.toml) is a hand-written sample of the full
lock for Inferno Canto 1 (20 scenes, validated as contiguous over lines 1–136).
It is kept in `ref/` to compare against a model-generated (e.g. Gemma 4) version
later. It shows the skeleton catching real traps — e.g. resolving "figliuol
d'Anchise" → **Aeneas** (the very Anchises-confusion that hit Paradiso 15), and
marking the swimmer and miser similes as imagery rather than characters.

## 4. Digest edition

Goal: a retelling of each canticle that is **more detailed than a bare plot
summary but lighter than a full line-by-line translation**, at a granularity
where the plot can actually be read as a story.

- **Density**: **one to two sentences per scene** — enough to convey who acts
  and what happens, while skipping the dense doctrinal and prosodic detail of the
  full text.
- **Unit**: scenes are **grouped into paragraphs**, several scenes per paragraph,
  roughly **3–5 paragraphs per canto**. A scene is *not* its own paragraph (that
  would be too long); the per-scene sentences flow together into a paragraph that
  reads as continuous narrative prose, not a table of disconnected blurbs.
- **Source of truth**: build the digest from the **(corrected) translation**, not
  from the raw summaries, so it inherits accurate names, speakers, and
  terminology. The context lock (§3) further guards its identities.
- **Form**: prose paragraphs under the existing `## Canto N` headings (drop the
  table format used for breakdowns).
- **Output**: producible per canticle, and (like the translation) in the target
  languages — a digest is a gentler entry point for readers than the full
  translation, and a useful cross-check on narrative coherence.

## 5. Fit with the 4-stage translation pipeline ([PROMPT.md](../PROMPT.md))

The translation use (§1) runs through the existing four-step pipeline (Step 1
alignment → Step 2 direct translation → Step 3 word-table coverage check →
Step 4 correction). Checking that fit surfaces what is already compatible, what
is merely a prerequisite, and what new machinery is needed.

### Already compatible

- **Chunk size is not hardcoded.** The prompts operate on an opaque
  `{source_text}`; a scene is just a differently-sized chunk than the current
  3-line unit in `test.py`. The line-fidelity rules (preserve line count and end
  punctuation) hold unchanged for a scene.
- **More context, by design.** A scene is a coherent dramatic beat, so it gives
  the model exactly the discourse context the §2 traps need — context a 3-line
  window cannot supply.

### Prerequisites / blockers (required first, but not new mechanisms)

- **Reference-translation coverage.** Steps 1–2 consume a `{reference}`
  translation. Today only `en-norton/` (Inferno Canto 1) exists. Translating any
  other scene needs a reference for those lines first; this gates the whole
  translation use.
- **Table size vs. local-LLM stability.** A 30-line scene yields a large Step 1
  alignment table and Step 3 word table — the kind of long, repetitive output
  that made local models degenerate (the failure `scene.py` was built around). A
  scene should therefore be the **context unit**, while Steps 1–4 may still run
  on **sub-chunks within the scene's locked context** (or scenes may be capped in
  size). A tuning decision for implementation.

### New mechanisms to add

1. **Scene-level context lock ("Step 0").** This is the context lock of §3, and
   it is **not** redundant with Step 1: Step 1 locks meaning *per token/line*,
   whereas the §2 errors are *discourse-level* (speaker, addressee, simile
   vehicle vs. tenor, deixis, realm). The lock is established once per scene and
   carried into Steps 1–4.
2. **Glossary injection.** The shared glossary (§3) needs a delivery slot the
   current prompts lack — a small term list passed into Step 1/Step 2 so
   recurring terms are translated uniformly instead of re-guessed.
3. **Scene-driven driver.** `test.py` chunks by a fixed line count; a new driver
   must read scene ranges from the breakdowns and feed scene (or sub-chunk) units
   through the pipeline. Mechanical, but new.

### The digest is a separate pipeline, not an extension of the four steps

The digest (§4) is **narrative prose**, which deliberately breaks the pipeline's
core rules — line fidelity, no content invention, word-by-word literalness. It
cannot reuse Steps 1–4. It is a distinct prose-generation pass with its own
prompt, taking the **completed literal translation** (or, lacking that, the
source) as input, and its own check: **narrative coherence + factual accuracy
against the source**, not the word-table coverage check. Keep it cleanly
separate from the 4-stage flow.

## Relationship to existing files

- `inferno.md` / `purgatorio.md` / `paradiso.md` — the scene breakdowns (units +
  summaries) this plan builds on; `*.jsonl` hold the raw model output (manual
  corrections live only in the `.md` files).
- `it/<canticle>/NN.txt` — the per-canto source; the per-canto context lock
  (§3) is written alongside as `NN.toml`.
- [`ref/inferno-01.toml`](ref/inferno-01.toml) — the hand-written context-lock
  sample (§3), for comparison against a model-generated version.
- [README.md](README.md) — the manual-correction tables that catalogue the exact
  factual errors the guidance in §2 (and the lock fields in §3) are distilled
  from.
