# Translation plan — the *Commedia*, scene by scene

Translate Dante **scene by scene**, not canto by canto. Each scene is a self-contained dramatic
beat (one place / speaker / action / topic): small enough to keep a local LLM on track, large
enough to carry the discourse context that the error traps below need. Every scene is run through
the 4-stage pipeline ([PROMPT.md](PROMPT.md)), preceded by a per-scene **context lock** ("Step 0")
that pins down *identity* before translation begins.

Translation is the **top of a three-layer stack** and authors none of its own linguistic
substrate. It consumes two upstream projects and adds only the reference-bound, target-language
work:

- **dante-corpus** serves the source text and a **canon-neutral grammatical parse** of every line —
  tokens, morphology + lemma, an exhaustive noun-phrase enumeration, dependency / grammatical role,
  and a predicate-argument skeleton. All of it is recoverable from the Italian alone, with no
  reference translation. Translation reads this parse instead of re-deriving morphosyntax.
- **dante-analyze** produces the **context lock** (identity / referent resolution is the analysis
  layer's job, not translation's) and the scene ranges.

What is left for translation is exactly the part neither upstream layer computes: aligning the
source to a **reference translation**, fixing **in-context English/target equivalents and
truth-conditions**, and producing natural target-language lines. Those bind to an external
reference and a target language, so they live here and nowhere else.

(A separate retelling — the *digest edition* — is an analyze-side product; it is not part of this
pipeline.)

## 1. Scenes as translation units

- Translate scene by scene rather than canto by canto. Each scene gives the model just enough
  context without drowning it in a 140-line canto.
- The line ranges are contiguous and validated against the source (no gaps/overlaps; full
  coverage), so translation can drive the pipeline (`translate.py`) unit by unit while guaranteeing
  nothing is skipped.
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
pin down. The upstream layers now neutralize several of them mechanically — noted in the *Guard*
column.

| Trap | What goes wrong | Guard |
|---|---|---|
| **Speaker / referent misidentification** (most common, most serious) | The model assigns lines to the wrong person, or confuses who is being referred to: Justinian→"Farinata", Beatrice↔Matelda, Charon↔the heaven-sent messenger, Chiron↔Nessus, Nicholas III↔Boniface. | The context lock fixes speaker/addressee/described per scene (analyze's resolved referents), carried through every step. |
| **Simile read as literal identity** | "X, *like* the shade of Anchises, …" collapsed into "the shade of Anchises". | Analyze tags each clause's frame (literal/simile/…); the lock carries the simile vehicle as imagery, not a character. The corpus dependency layer already isolates the comparison's syntax. |
| **A referent self-identifying vs. pointing to another** | Folco, speaking, was made to "identify itself as Rahab" when pointing to a *neighboring* soul. | Deixis is resolved upstream (analyze coref over the corpus pronoun/pro-drop forms); the lock states who is "I" and who is "this light / that one". |
| **Reference point misread as subject** | "whence thy lady sent Virgil" (= Limbo, a *place* marker) became "a history of Virgil". | The corpus grammatical-role layer marks the actual subject; a name fixing a place/time is typed as such, not as the topic. |
| **Mistranslated domain nouns** | `aguglia` ("eagle") rendered as "needle", repeatedly. | The glossary (§3) fixes recurring technical/poetic renderings; the corpus lemma layer makes recurrences findable. |
| **Realm / topography slips** | "circle" vs "terrace" vs "heaven/sphere"; Inferno / Purgatory / Limbo confused. | The lock anchors every scene to its realm (Inferno = **circles**; Purgatorio = **terraces**; Paradiso = **heavens / spheres**), from analyze's topography. |
| **Theological / scriptural over-reading** | "chosen *from* the cross for the great office" (John entrusted with Mary) became "died on the cross". | Translate what the line says; do not "complete" allusions. The Step-1 truth-conditions are bounded to the source line. |
| **Garbled or invented proper names** | "Rinvieri", "Forese Giunchi", "Anchimates" — names mangled or given spurious surnames. | Copy proper names exactly from the source; the glossary fixes the standard spelling. Verify any name against the source line. |
| **Latin / scripture tags** | Embedded Latin (`Diligite iustitiam`, `Ave Maria`) is easy to drop or paraphrase. | Preserve embedded Latin/scripture verbatim; do not translate or omit it. |

## 3. The context lock (Step 0)

Each scene is run through a per-scene **context lock** as pre-processing ("Step 0", §4): an
identity-only record — who speaks, where we are, who "this light" is — that defends against the §2
traps. It fixes identity only, never a paraphrase, and each entry is verifiable against the source
(it carries a `basis` quote).

**The lock is produced by dante-analyze, not authored here.** It *is* referent resolution (the
analysis layer's job), now built on that repo's interpretive scene artifact (resolved referents +
classified relations) over the corpus parse. Its TOML schema, the authoring process, the name-form
open question, and the hand-written reference sample (`dante-analyze/ref/inferno-01.toml`) live in
dante-analyze `ref/PLAN.md`. Translation **consumes** the verified lock and carries it through
Steps 1–4.

A shared **glossary** (translation-side, planned as `gloss.toml`) is the companion the lock
references: fixed renderings of domain terms (`aguglia` = eagle), the canticle-specific realm
vocabulary, and the standard spelling of recurring proper names (`Cassio → Cassius`). It is a
*translation* concern (how terms are rendered in the **target**), injected into the pipeline (§4);
scenes reference it rather than repeating it.

## 4. Fit with the 4-stage pipeline ([PROMPT.md](PROMPT.md))

The translation use (§1) runs through the four-step pipeline (Step 1 alignment → Step 2 direct
translation → Step 3 word-table coverage check → Step 4 correction). With the corpus parse now
available, Step 1 changes shape; the rest is as before.

### Step 1 is now a thin reference-alignment delta

Step 1 ("Source-Reference Alignment & Semantic Analysis") used to do two jobs in one LLM call:
recover the **morphosyntax** of each line *and* align it to the reference translation. The
morphosyntax is now upstream — the corpus parse already gives, per token, lemma / part of speech /
features and grammatical role, and per line the noun phrases. So Step 1 keeps only the
**reference-bound** work that nothing upstream can do (it requires the reference, which the corpus
must never see):

- **Reference equivalent** — the in-context English/target word the reference chose for each token.
- **Interpretation Lock (truth-conditions)** — the per-line locked meaning, including comparative
  entities/relations/degree.

The morphology and grammatical-role columns are **read from the corpus parse**, not regenerated.
This makes Step 1 smaller and more stable on local models (the long, repetitive table was a known
degeneration trigger), and guarantees the source-side grammar is identical to what analyze used.

### Already compatible

- **Chunk size is not hardcoded.** The prompts operate on an opaque `{source_text}`; a scene is just
  a differently-sized chunk than the current 3-line unit in `test.py`. The line-fidelity rules
  (preserve line count and end punctuation) hold unchanged for a scene.
- **More context, by design.** A scene is a coherent dramatic beat, giving the model exactly the
  discourse context the §2 traps need.

### Prerequisites / blockers (required first, but not new mechanisms)

- **Reference-translation coverage.** Steps 1–2 consume a `{reference}` translation. Today only
  `en-norton/` (Inferno Canto 1) exists. Translating any other scene needs a reference for those
  lines first; this gates the whole translation use.
- **Corpus parse coverage.** Step 1's morphology/role columns now depend on the corpus grammatical
  layers being built for the target lines. Until a canto's parse is frozen upstream, Step 1 falls
  back to deriving them itself (the old behaviour) — so this is a soft dependency, not a hard
  blocker.
- **Table size vs. local-LLM stability.** A scene should be the **context unit**, while Steps 1–4
  may still run on **sub-chunks within the scene's locked context** (or scenes may be capped in
  size). A tuning decision for implementation — eased now that Step 1 no longer regenerates the
  morphology table.

### New mechanisms to add

1. **Scene-level context lock ("Step 0").** The context lock of §3; **not** redundant with Step 1.
   Step 1 locks meaning *per token/line*; the §2 errors are *discourse-level* (speaker, addressee,
   simile vehicle vs. tenor, deixis, realm). Established once per scene, carried into Steps 1–4.
2. **Parse injection into Step 1.** A delivery slot for the corpus morphology/role/NP layers so Step
   1 aligns against a given parse instead of regenerating it.
3. **Glossary injection.** The shared glossary (§3) needs a delivery slot the current prompts lack —
   a small term list passed into Step 1/Step 2 so recurring terms are translated uniformly.
4. **Scene-driven driver.** `test.py` chunks by a fixed line count; a new driver must read scene
   ranges from dante-analyze, pull the corpus parse, and feed scene (or sub-chunk) units through the
   pipeline. Mechanical, but new.

## Inputs & related files

- **Source text & grammatical parse** — the normalized source `.txt` and the canon-neutral parse
  (tokens, morphology + lemma, noun phrases, dependency/role, predicate-argument skeleton) are
  served by **dante-corpus** through its API; not stored in this repo.
- **Scene ranges** — the per-canto scene ranges are served by **dante-analyze**
  (`dante_analyze.scenelib.load_scenes`).
- **Context lock** — produced by **dante-analyze**; the TOML spec and the hand-written sample
  (`inferno-01.toml`) live in dante-analyze `ref/PLAN.md`. Translation consumes it; it is not
  authored here.
- [README.md](README.md) — the manual-correction tables that catalogue the exact factual errors the
  guidance in §2 (and the lock fields) are distilled from.
- [PROMPT.md](PROMPT.md) — the full 4-stage pipeline prompts (§4).
