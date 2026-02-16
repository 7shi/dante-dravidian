# GPT-OSS 120B Limitations in the Fix Pipeline: Spanish and Kannada Case Study

This document analyzes the post-translation fix pipeline results for two languages — Spanish (a Romance language closely related to Italian) and Kannada (a Dravidian language distant from Italian) — to identify recurring shortcomings in the GPT-OSS 120B initial translations and evaluate how prompt engineering and context design could address them.

## Pipeline Overview

The translations originate from GPT-OSS 120B via the 4-stage structured translation process (`test/`), then pass through a two-pass fix pipeline:

1. **Pass 1** (Gemini 3.0 Pro): Review → Fix
2. **Pass 2** (GPT-5.2): Review → Fix → Quote fix → Section split

## Findings by Language

### Spanish: A Closely Related Language

Spanish, as a Romance language, benefits from extensive lexical and syntactic overlap with Italian. The GPT-OSS 120B output was already largely comprehensible, but the fix pipeline revealed systematic weaknesses:

**Issues caught and corrected:**

- **Lexical false friends**: "leona" → "pantera/lonza" (line 32), "valor" → "virtud" (line 104), "magreza" → "magrura" (line 50). The model defaulted to surface-similar words without checking semantic fit.
- **Garbled line content**: Line 40 was a duplicate of line 43 instead of translating "mosse di prima quelle cose belle." This is a structural hallucination — the model lost track of which Italian line it was translating.
- **Pronoun/grammar errors**: "yo los mantuve detrás de él" (line 136) used a plural object where the Italian "li" is dative singular. Fixed to "yo le seguí detrás."
- **Missing quotation marks**: Direct speech boundaries (lines 65–66, 67, 76–78, 79–80, etc.) were inconsistently marked. The quote-fix stage systematically restored them.
- **Register/nuance drift**: "piedad" for "pieta" (line 21, meaning anguish not mercy), "molestia" for "noia" (line 76, too mild), "pesadez" for "gravezza" (line 52, too physical), "camino" for "viaggio" (line 91, journey not path).

**Issues remaining after the full pipeline:**

The GPT-5.2 second pass produced a substantially polished result. Most corrections were accurate, though a few nuances noted in the detailed review (e.g., the exact rendering of "pelago" as "piélago" vs. "mar", or "acquista" as mercantile vs. generic "gana") were left at an acceptable but not ideal level.

### Kannada: A Distant Language

Kannada presented fundamentally different and more severe challenges. The initial GPT-OSS 120B output contained errors that went beyond lexical slips into structural miscomprehension:

**Errors in the initial translation (by severity):**

*Critical — meaning lost or inverted:*

- **Wrong animal identification**: "lupa" (she-wolf) rendered as "ಹೆಣ್ಣು ನರಿ" (vixen/female fox, line 49) — a symbolically critical error in Dante scholarship. Fixed to "ಹೆಣ್ಣು ತೋಳ" in the final output.
- **Semantic inversion**: "ಹುಸಿಯಂತೆ" (false/lie, line 63) for Italian "fioco" (faint/hoarse) — the model confused phonetic similarity with meaning. Fixed to "ಕ್ಷೀಣವಾಗಿ."
- **Antonym substitution**: "ಸೊಂಪಿನಲ್ಲಿ" (plumpness, line 50) for "magrezza" (leanness) — exactly the opposite meaning. Fixed to "ಕ್ಷೀಣತೆಯಲ್ಲೇ."
- **Key term mistranslation**: "ವೆಲ್ಟ್ರೋ" (veltro/greyhound, lines 101–102) was rendered as "ಹೊಂಡು" (hole/pit) — a completely unrelated word. The fix pipeline transliterated it as "ವೆಲ್ಟ್ರೋ" rather than attempting a Kannada equivalent.

*Serious — structure or grammar broken:*

- **Broken syntax**: Multiple lines had Kannada word order that was ungrammatical even for SOV structure (e.g., line 28 object-verb mismatch, line 58 agent-patient confusion).
- **Pronoun inconsistency**: The text alternated between informal "ನೀನು" (you-singular) and formal "ನೀವು" (you-plural/formal) for the same addressee (Dante speaking to Virgil).

*Minor — meaning preserved but non-native phrasing:*

- **English loanwords**: "ಪಾಸ್" (pass, lines 26–27) used instead of native Kannada "ದಾರಿ" or "ಪಥ." While English loanwords are commonly used in everyday Kannada and the meaning is preserved, literary translation of Dante calls for native vocabulary. Fixed to native Kannada in the pipeline.

**What the fix pipeline accomplished for Kannada:**

The Gemini 3.0 Pro review (Pass 1) caught surprisingly few issues — it fixed "ಹಾರುತ್ತಿತ್ತು" (flying) to "ಓಡಿಹೋಗುತ್ತಿತ್ತು" (fleeing), "ಪಾಸ್" to "ದಾರಿ", "ಹುಸಿಯಂತೆ" to "ಕ್ಷೀಣವಾಗಿ", and "ಗಾಯಗೊಂಡರು" (wounded) to "ಗಾಯಗಳಿಂದ ಮರಣಹೊಂದಿದರು" (died of wounds), but left many other errors untouched.

The GPT-5.2 review (Pass 2) was far more thorough, producing detailed line-by-line analysis with Kannada-specific corrections. The final output shows substantial improvement: proper she-wolf identification, better syntax, corrected loanwords, and improved register. However, some issues persisted:

- Line 34 contains a Malayalam word "നിന്ന്" (ninn) mixed into the Kannada text — a script contamination artifact.
- Line 40 has a typo "ಚಲಿಸಿಸಿದಾಗ" (doubled syllable).
- Pronoun register remains inconsistent in places.
- Some lines remain syntactically awkward even after two passes.

## Systematic Weaknesses of GPT-OSS 120B

Comparing the two languages reveals patterns in the 120B model's failure modes:

### 1. Vocabulary Coverage Gap

For Spanish, vocabulary errors were mostly false friends or register mismatches — the model had the right neighborhood but picked the wrong word. For Kannada, errors were more fundamental: antonyms, unrelated words, and cross-script contamination. The model also fell back to English loanwords (e.g., "ಪಾಸ್" for "pass"), which are common in everyday Kannada but stylistically inappropriate for literary translation. The more severe issue is that the model's Kannada vocabulary is sparse enough to produce phonetic guessing and semantically unrelated substitutions.

### 2. Structural Tracking Failure

Both languages showed line 40 garbled (Spanish duplicated line 43; Kannada was confused). Complex syntactic structures like the simile in lines 22–27 or the conditional in lines 44–45 broke down in both languages, but far more severely in Kannada. The model struggles to maintain tercet-level coherence when the Italian syntax spans multiple lines.

### 3. Cultural/Symbolic Blindness

The model lacks domain knowledge about Dante: "lonza" vs. "leone" vs. "lupa" distinctions, the symbolic significance of "veltro," the meaning of "tra feltro e feltro." For Spanish this manifested as choosing the wrong cat species; for Kannada it produced nonsense words.

### 4. Register and Pragmatics

Both outputs showed inconsistent register (formal/informal mixing, quotation mark omission for direct speech). The Spanish output was closer to natural prose; the Kannada output often read as translationese with broken word order.

## Spanish vs. Kannada: Comparative Summary

The following table summarizes the qualitative difference between the two languages across key dimensions:

| Dimension | Spanish | Kannada |
|---|---|---|
| **Error severity** | Lexical: false friends, register drift (meaning approximately correct) | Semantic: antonyms, unrelated words, meaning lost or inverted |
| **Vocabulary fallback** | Surface-similar words from the same language | Phonetic guessing, English loanwords, cross-script borrowing (Malayalam) |
| **Structural fidelity** | Line 40 duplicated; otherwise structure preserved | Line 40 garbled; widespread SOV word-order violations, agent-patient confusion |
| **Cultural terms** | Wrong species within the right category (e.g., lioness for leopard) | Nonsense words (e.g., "pit" for "greyhound") |
| **Register** | Close to natural prose; minor formal/informal inconsistency | Translationese with broken word order; pronoun register inconsistency |
| **Fix pipeline workload** | Polish: register, nuance, quotation marks | Heavy lifting: animal correction, meaning inversion, syntax restructuring |
| **English loanwords** | Not observed | Present but minor (meaning preserved; stylistically inappropriate for literary text) |
| **Post-fix residual issues** | Few: some nuance-level choices left at acceptable level | Several: script contamination, doubled syllables, syntactic awkwardness |

The gap is not merely quantitative (more errors in Kannada) but **qualitative**: Spanish errors are predominantly within the correct semantic neighborhood, while Kannada errors frequently cross into unrelated or opposite meanings. This reflects the 120B model's fundamentally different competence levels for the two languages — a difference that no prompt design can fully bridge.

## Prompt Improvement vs. Model Limitations

The 4-stage prompt pipeline (`PROMPT.md`) already incorporates several safeguards: reference-anchored translation (Step 1), structured word-level coverage checks (Step 3), correction passes (Step 4), and explicit target-language purity constraints. The pipeline also chunks input into 3-line tercets (`test.py`) to reduce structural tracking burden. Despite all of this, the 120B model still produced antonym substitutions, nonsense words, cross-script contamination, and broken syntax — particularly for Kannada.

This raises the question: **are these failures addressable through better prompting, or are they fundamental limitations of the 120B model?**

The evidence suggests that most Kannada-specific failures reflect **model-level limitations** rather than prompt design flaws:

- **Instruction non-compliance**: The model ignored explicit constraints it was given (e.g., target-language purity in Step 4, line-count fidelity in Step 2). A model that cannot reliably follow instructions it has already received is unlikely to follow additional ones.
- **Vocabulary gaps that prompts cannot fill**: The phonetic guessing and cross-script borrowing documented in the Kannada findings above are fallback behaviors triggered by missing vocabulary. (English loanword use is a less severe symptom — meaning is preserved — but the antonym substitutions and nonsense words indicate deeper gaps.) A glossary (Recommendation 1) could address known problem terms, but cannot cover the full gap.
- **Systematic quality difference by language**: The same language-agnostic prompt pipeline produced acceptable Spanish but severely broken Kannada, reflecting uneven training data coverage.
- **Self-check failures**: Steps 3–4 ask the model to identify and fix its own errors, but the model's Kannada competence is insufficient to reliably evaluate its own Kannada output. A model that produces "ಸೊಂಪಿನಲ್ಲಿ" (plumpness) for "magrezza" (leanness) is unlikely to catch this as WRONG in its own coverage check.

**This assessment led to the decision to build the fix pipeline** (`fix/`), which uses more capable models (Gemini 3.0 Pro, GPT-5.2) for post-hoc review and correction. The pipeline's design — always comparing against the Italian original — compensates for information that the 120B model failed to encode, which no amount of self-correction prompting could recover.

### Why not use large models from the start?

A natural question arises: if the 120B model's output requires extensive correction by GPT-5.2 anyway, why not use GPT-5.2 (or a comparable large model) for the initial translation as well?

The answer is **cost structure**. The 4-stage translation pipeline (`PROMPT.md`) is designed to be thorough: it performs source-reference alignment, word-by-word analysis, translation, coverage checking, and correction — all as a multi-turn conversation per tercet, per language. For 46 tercets × 20 languages, this amounts to hundreds of API calls with substantial prompt context. Running this entirely on large commercial models would be prohibitively expensive.

The current architecture separates the workload by cost profile:

- **Local 120B model** (free, unlimited): Handles the labor-intensive 4-stage pipeline — the bulk of the API calls. The output quality varies by language, but even for low-resource languages it provides a structured draft with line numbering, approximate meaning, and consistent formatting.
- **Large commercial models** (paid, per-token): Handle only the review-and-fix passes, which are comparatively lightweight — a single review pass and fix per language, not the full 4-stage pipeline. These models' superior cross-lingual competence is applied where it matters most: evaluating and correcting the draft against the Italian original.

This "cheap draft, expensive correction" architecture is a pragmatic trade-off, and the benefits extend beyond cost savings. Even if budget were unlimited, having a draft improves the reliability of the final output:

- **Generation vs. verification**: Translating 136 lines of tercets from scratch is a *generation* task — the model must produce correct output for every line while maintaining structural fidelity. Even large models can skip lines, duplicate content, or hallucinate under these conditions. With a draft in hand, the task becomes *verification and correction* — comparing two texts and identifying discrepancies — which is fundamentally more constrained and less prone to omission or hallucination.
- **Structural scaffolding**: The 120B model's draft, however flawed in content, provides line numbering, consistent formatting, and a one-to-one correspondence with the source. This scaffolding anchors the large model's review, making it unlikely to lose track of which line it is processing.
- **Error locality**: When the large model works from a draft, errors are localized — it needs to fix specific words or phrases, not reconstruct entire passages. This keeps each correction small and verifiable, reducing the risk of introducing new errors during the fix process.

That said, some improvements to the initial translation prompts could still reduce the fix pipeline's workload, particularly for high-severity errors that are expensive to correct downstream.

## Recommendations for Prompt/Context Improvements

The following could improve GPT-OSS 120B output quality *before* the fix pipeline runs, reducing the burden on downstream models. However, given the model limitations discussed above, these should be understood as **incremental improvements** rather than solutions — the fix pipeline remains essential:

### 1. Provide a Glossary of Dante-Specific Terms

Include a pre-translation glossary in the prompt:

```
Key terms:
- lonza → [target language: leopard/panther], NOT lioness
- lupa → she-wolf (symbolic: avarice)
- veltro → greyhound/hound (symbolic: prophesied savior)
- pieta → anguish/distress (NOT piety/mercy in this context)
- peltro → pewter/metal (NOT peltre)
```

This directly addresses the vocabulary gap for culturally loaded terms.

### 2. Add Tercet-by-Tercet Alignment Anchors *(already implemented)*

The pipeline already chunks input into 3-line tercets with explicit line numbering (`test.py`, lines 82–98), but structural tracking errors (e.g., line 40 duplication) still occurred. Additional anchoring — repeating line numbers in the translation instruction or adding explicit "do not skip or duplicate lines" constraints — could further reduce these errors.

### 3. Enforce Target-Language Purity Check *(already implemented)*

Step 4 already includes a target-language purity constraint, but the 120B model still produced loanwords and cross-script contamination. Moving this instruction earlier (e.g., into Step 2 as a translation constraint) could help, since the model may not retain Step 4 instructions when generating Step 2 output.

### 4. Provide Parallel English as Bridge Context *(already implemented)*

Step 1 already provides the English reference alongside the Italian source, but for low-resource languages the English context may not carry through to later steps. Making key English phrases more prominent in the Step 2 translation instruction could help avoid semantic inversions.

### 5. Add a Self-Check Instruction for Key Semantic Relations *(partially implemented)*

Steps 3–4 already implement word-level coverage checks (MISSING/WRONG/GRAMMAR/UNNECESSARY) and correction passes. However, this misses semantic-relation errors. Adding passage-specific verification prompts (e.g., "Is the animal a she-WOLF?" or "Is this a resultative 'so X that Y' structure?") could catch antonym substitutions and structural inversions that word-level checks miss.

### 6. Use Few-Shot Examples from the Same Language Family

For Kannada, include a translated sample from another Dravidian language (e.g., Telugu or Tamil) as a structural reference. For Spanish, an existing high-quality Italian→Spanish literary translation of the same passage could serve as a register anchor.

## Conclusion

The fix pipeline is effective but language-dependent in scope: for Spanish, it mainly polishes register and scattered lexical errors; for Kannada, it performs heavy lifting — correcting wrong animals, fixing inverted meanings, and restructuring broken syntax. (English loanword use, while stylistically undesirable in literary translation, is a comparatively minor issue since meaning is preserved.) The pipeline cannot recover information that was never encoded, which is why its design of always comparing against the Italian original is essential.

The failures documented above are primarily **model capability limitations**, not prompt design flaws: the 120B model's training data is insufficient for low-resource languages like Kannada, regardless of prompt structure. The most impactful prompt-level improvement would be **providing a domain-specific glossary** (Recommendation 1), but the quality gap between high-resource and low-resource languages will persist at this model scale. **The fix pipeline using more capable models is not merely a convenience but a necessity** — a deliberate architectural choice to separate "fast local draft generation" from "accurate quality correction."
