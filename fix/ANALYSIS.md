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

**Critical errors in the initial translation:**

- **Wrong animal identification**: "lupa" (she-wolf) rendered as "ಹೆಣ್ಣು ನರಿ" (vixen/female fox, line 49) — a symbolically critical error in Dante scholarship. Fixed to "ಹೆಣ್ಣು ತೋಳ" in the final output.
- **Untranslated English loanwords**: "ಪಾಸ್" (pass, lines 26–27) left as a transliterated English word instead of using Kannada "ದಾರಿ" or "ಪಥ." Fixed to native Kannada.
- **Semantic inversion**: "ಹುಸಿಯಂತೆ" (false/lie, line 63) for Italian "fioco" (faint/hoarse) — the model confused phonetic similarity with meaning. Fixed to "ಕ್ಷೀಣವಾಗಿ."
- **Antonym substitution**: "ಸೊಂಪಿನಲ್ಲಿ" (plumpness, line 50) for "magrezza" (leanness) — exactly the opposite meaning. Fixed to "ಕ್ಷೀಣತೆಯಲ್ಲೇ."
- **Key term mistranslation**: "ವೆಲ್ಟ್ರೋ" (veltro/greyhound, lines 101–102) was rendered as "ಹೊಂಡು" (hole/pit) — a completely unrelated word. The fix pipeline transliterated it as "ವೆಲ್ಟ್ರೋ" rather than attempting a Kannada equivalent.
- **Broken syntax**: Multiple lines had Kannada word order that was ungrammatical even for SOV structure (e.g., line 28 object-verb mismatch, line 58 agent-patient confusion).
- **Pronoun inconsistency**: The text alternated between informal "ನೀನು" (you-singular) and formal "ನೀವು" (you-plural/formal) for the same addressee (Dante speaking to Virgil).

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

For Spanish, vocabulary errors were mostly false friends or register mismatches — the model had the right neighborhood but picked the wrong word. For Kannada, errors were more fundamental: antonyms, unrelated words, untranslated loanwords, and cross-script contamination. This suggests the model's Kannada vocabulary is sparse and it falls back to phonetic guessing or English bridging.

### 2. Structural Tracking Failure

Both languages showed line 40 garbled (Spanish duplicated line 43; Kannada was confused). Complex syntactic structures like the simile in lines 22–27 or the conditional in lines 44–45 broke down in both languages, but far more severely in Kannada. The model struggles to maintain tercet-level coherence when the Italian syntax spans multiple lines.

### 3. Cultural/Symbolic Blindness

The model lacks domain knowledge about Dante: "lonza" vs. "leone" vs. "lupa" distinctions, the symbolic significance of "veltro," the meaning of "tra feltro e feltro." For Spanish this manifested as choosing the wrong cat species; for Kannada it produced nonsense words.

### 4. Register and Pragmatics

Both outputs showed inconsistent register (formal/informal mixing, quotation mark omission for direct speech). The Spanish output was closer to natural prose; the Kannada output often read as translationese with broken word order.

## Recommendations for Prompt/Context Improvements

The following could improve GPT-OSS 120B output quality *before* the fix pipeline runs, reducing the burden on downstream models:

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

### 2. Add Tercet-by-Tercet Alignment Anchors

Instead of presenting the full 136 lines at once, chunk the input into tercets with explicit line numbering:

```
Translate lines 37–39:
37 Temp' era dal principio del mattino,
38 e 'l sol montava 'n sù con quelle stelle
39 ch'eran con lui quando l'amor divino
```

This reduces the structural tracking burden and prevents line-skipping/duplication errors.

### 3. Enforce Target-Language Purity Check

Add an explicit instruction: "Do NOT use English words or words from other scripts. Every word must be in [target language] script. If you are unsure of a term, transliterate the Italian original rather than using English."

This would prevent the "ಪಾಸ್" (pass) and cross-script contamination issues in Kannada.

### 4. Provide Parallel English as Bridge Context

For low-resource languages, include the English translation alongside the Italian to give the model a second reference point:

```
Italian: che non lasciò già mai persona viva.
English: that never yet left any person alive.
→ Translate to Kannada:
```

The 4-stage pipeline already does this (Step 1 alignment), but making the English more prominent in the translation step could help the 120B model avoid semantic inversions.

### 5. Add a Self-Check Instruction for Key Semantic Relations

Prompt the model to verify key relationships after translating:

```
After translating, verify:
- Line 7: Is the comparison "the forest is SO bitter THAT death is only slightly more"? (not the reverse)
- Line 49: Is the animal a she-WOLF (not fox, not dog)?
- Lines 55–57: Is this a SIMILE ("like one who...")?
```

This lightweight self-verification could catch the most common semantic inversions.

### 6. Use Few-Shot Examples from the Same Language Family

For Kannada, include a translated sample from another Dravidian language (e.g., Telugu or Tamil) as a structural reference. For Spanish, an existing high-quality Italian→Spanish literary translation of the same passage could serve as a register anchor.

## Conclusion

The fix pipeline is effective: it transforms GPT-OSS 120B output from rough drafts with critical errors into readable translations. For Spanish, the pipeline's main work is polishing register and fixing scattered lexical errors. For Kannada, it performs much heavier lifting — correcting wrong animals, removing loanwords, fixing inverted meanings, and restructuring broken syntax.

However, the pipeline cannot always recover information that was never encoded. When the 120B model produces "ಹೊಂಡು" (pit) for "veltro" (greyhound), no amount of review can recover the correct meaning without access to the Italian source — which is why the pipeline's design of always comparing against the original is essential.

The most impactful improvement would be **providing a domain-specific glossary** in the initial translation prompt. This single change could eliminate the highest-severity errors (wrong animals, wrong concepts, nonsense words) that currently require the most expensive downstream correction. Combined with tercet-level chunking and an explicit target-language purity constraint, GPT-OSS 120B could produce substantially cleaner first drafts, especially for low-resource languages like Kannada.
