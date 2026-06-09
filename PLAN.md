# Translation plan — the *Commedia*, scene by scene

Translate Dante **scene by scene**, not canto by canto. Each scene is a self-contained dramatic
beat (one place / speaker / action / topic): small enough to keep a local LLM on track, large
enough to carry the discourse context that the error traps below need. Every scene is run through
the existing 4-stage pipeline ([PROMPT.md](PROMPT.md)), preceded by a per-scene **context lock**
("Step 0") that pins down *identity* before translation begins.

Inputs come from two external packages and this plan is only about how **translation consumes**
them:

- **dante-corpus** serves the source text (tokens and quote spans).
- **dante-analyze** produces the **context lock** (identity / referent resolution is the analysis
  layer's job, not translation's).

(A separate retelling — the *digest edition* — is an analyze-side product built from the scene
split and `reading/`; it is not part of this pipeline.)

## 1. Scenes as translation units

- Translate scene by scene rather than canto by canto. Each scene gives the model just enough
  context without drowning it in a 140-line canto.
- The line ranges are contiguous and validated by dante-corpus (no gaps/overlaps; full coverage
  against the source), so translation can drive the pipeline (`translate.py`) unit by unit while
  guaranteeing nothing is skipped.
- The context each scene needs (who speaks, which realm, who "this light" is) is fixed up front in
  the **context lock** (§3) rather than left to the translator to re-derive implicitly. The
  split-time scene summaries are **not authoritative** and are not an input — proofreading found
  real factual errors in them (catalogued in the correction tables in [README.md](README.md)); the
  source text is always the final arbiter.

## 2. Translation traps to guard against

These are drawn from the error tendencies seen while proofreading the generated scene summaries
(Inferno, Purgatorio, Paradiso). The local model failed in consistent, predictable ways; the same
traps apply to translation, so guard against them explicitly. **Every correction in the README
tables maps to one of these traps**, and they are exactly what the context lock (§3) is designed to
pin down.

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

## 3. The context lock (Step 0)

Each scene is run through a per-scene **context lock** as pre-processing ("Step 0", §4): an
identity-only record — who speaks, where we are, who "this light" is — that defends against the §2
traps. It fixes identity only, never a paraphrase, and each entry is verifiable against the source
(it carries a `basis` quote).

**The lock is produced by dante-analyze, not authored here.** It *is* referent resolution (the
analysis layer's job), built on that repo's `tags/` + speaker/edge data, so its TOML schema, the
authoring process, the name-form open question, and the hand-written reference sample
(`dante-analyze/ref/inferno-01.toml`) live in dante-analyze `ref/PLAN.md`. Translation **consumes**
the verified lock and carries it through Steps 1–4.

A shared **glossary** (translation-side, planned as `gloss.toml`) is the companion the lock
references: fixed renderings of domain terms (`aguglia` = eagle), the canticle-specific realm
vocabulary, and the standard spelling of recurring proper names (`Cassio → Cassius`). It is a
*translation* concern (how terms are rendered in the target), injected into the pipeline (§4);
scenes reference it rather than repeating it.

## 4. Fit with the 4-stage pipeline ([PROMPT.md](PROMPT.md))

The translation use (§1) runs through the existing four-step pipeline (Step 1 alignment → Step 2
direct translation → Step 3 word-table coverage check → Step 4 correction). Checking that fit
surfaces what is already compatible, what is merely a prerequisite, and what new machinery is
needed.

### Already compatible

- **Chunk size is not hardcoded.** The prompts operate on an opaque `{source_text}`; a scene is
  just a differently-sized chunk than the current 3-line unit in `test.py`. The line-fidelity rules
  (preserve line count and end punctuation) hold unchanged for a scene.
- **More context, by design.** A scene is a coherent dramatic beat, so it gives the model exactly
  the discourse context the §2 traps need — context a 3-line window cannot supply.

### Prerequisites / blockers (required first, but not new mechanisms)

- **Reference-translation coverage.** Steps 1–2 consume a `{reference}` translation. Today only
  `en-norton/` (Inferno Canto 1) exists. Translating any other scene needs a reference for those
  lines first; this gates the whole translation use.
- **Table size vs. local-LLM stability.** A 30-line scene yields a large Step 1 alignment table and
  Step 3 word table — the kind of long, repetitive output that made local models degenerate (the
  failure the scene split was built around). A scene should therefore be the **context unit**, while
  Steps 1–4 may still run on **sub-chunks within the scene's locked context** (or scenes may be
  capped in size). A tuning decision for implementation.

### New mechanisms to add

1. **Scene-level context lock ("Step 0").** This is the context lock of §3, and it is **not**
   redundant with Step 1: Step 1 locks meaning *per token/line*, whereas the §2 errors are
   *discourse-level* (speaker, addressee, simile vehicle vs. tenor, deixis, realm). The lock is
   established once per scene and carried into Steps 1–4.
2. **Glossary injection.** The shared glossary (§3) needs a delivery slot the current prompts lack —
   a small term list passed into Step 1/Step 2 so recurring terms are translated uniformly instead
   of re-guessed.
3. **Scene-driven driver.** `test.py` chunks by a fixed line count; a new driver must read scene
   ranges from dante-analyze and feed scene (or sub-chunk) units through the pipeline. Mechanical,
   but new.

## Inputs & related files

- **Source text** — the normalized source `.txt` is served by **dante-corpus** through its API
  (`dc.canto(...).lines()`); not stored in this repo.
- **Scene ranges** — the per-canto scene ranges are served by **dante-analyze**
  (`dante_analyze.scenelib.load_scenes`).
- **Context lock** — produced by **dante-analyze**; the TOML spec and the hand-written sample
  (`inferno-01.toml`) live in dante-analyze `ref/PLAN.md`. Translation consumes it; it is not
  authored here.
- [README.md](README.md) — the manual-correction tables that catalogue the exact factual errors the
  guidance in §2 (and the lock fields) are distilled from.
- [PROMPT.md](PROMPT.md) — the full 4-stage pipeline prompts (§4).
