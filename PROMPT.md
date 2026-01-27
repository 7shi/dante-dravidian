# Prompt Design for Translation with Local LLMs

When requesting translations from LLMs for languages with limited training data using simple instructions, grammatical structures often collapse, and meaning is frequently misinterpreted. This document outlines a method to improve quality by dividing the process into logical steps.

## Introduction

Compared to massive models like Gemini 3.0 Pro, local LLMs are more prone to grammatical collapse and hallucinations when dealing with "High-Difficulty Translations" where the following conditions overlap:

1.  **Classical/Poetic Text:** High context dependency, frequent omissions, and inversions.
    *   Example: Dante's *Divine Comedy* (Italian).
2.  **Low-Resource Languages:** Languages with relatively less training data.
    *   Example: Malayalam.
3.  **Agglutinative/SOV Languages:** Languages where word order and grammatical structure differ significantly from the source language (SVO).

This document explains the design philosophy and implementation details of "5-Stage Structured Prompting" to overcome these challenges and maximize the potential of local LLMs.

**Note**: The prompt design methodology introduced here was constructed through hypothesis testing via dialogue with Gemini and repeated translation experiments using GPT-OSS 120B.

## "Serialization" and "Fixation" of Thought

The primary reason LLMs fail in translation is the dispersion of computational resources (Attention) when attempting to perform "semantic interpretation," "grammatical mapping," "word order rearrangement," and "vocabulary selection" all at once.

To prevent this, we adopt the following strategies:

1.  **Context Lock:** Align the source text with a reference translation (English) to fix the meaning. (Language-independent)
2.  **Requirement Definition:** Define necessary "cases" and "tenses" in the target language.
3.  **Inventory & Assembly:** Separate vocabulary selection from sentence construction.

### Why Choose English as the Intermediate Language?

We adopt English as the intermediate language (bridge) not because of its structural superiority, but based on the "realistic constraint" that English dominates the training data of current LLMs, resulting in the most stable inference accuracy.

However, since English also contains polysemy and lexical ambiguity, translation into English does not completely fix the meaning. This method mitigates this ambiguity by explicitly verbalizing the "Contextual Definition" in Step 1, rather than just mapping English words.

Ideally, using an artificial language without semantic ambiguity or an abstract internal representation independent of specific natural languages would be desirable. However, such methods are technically unestablished and not yet at a practical level.

### Case Study

Here is the processing flow applied to Dante's *Inferno* (Canto 1, Line 8) and the effect of "Context Lock."

**Processing Flow:**

1.  **Source (Italian):** ma per trattar del ben ch'i' **vi** trovai,
2.  **Intermediate (English):** But in order to treat of the good that **there** I found,
3.  **Target (Malayalam):** പക്ഷേ ഞാന്‍ **അവിടെ** നല്ലതിന്റെ കണ്ടു ചെയ്യാൻ  
    (But I found the good **there**, and to speak about it)

The core of this process lies in handling the polysemous word **`vi`**.

1.  **The Trap of Polysemy:** Italian `vi` has two meanings: the pronoun "to you" (plural) and the locative adverb "there." Without context, LLMs tend to choose the more frequent "to you."
2.  **Fixation via English:** By mapping it to "found **there**" in Step 1 (using literal translation or reference), the meaning of `vi` is restricted to spatial "location."
3.  **Transfer to Target:** Subsequent steps force the use of the Malayalam word **`അവിടെ`** (avide), corresponding to "English: there." This physically eliminates the mistranslation "to you" which ignores context.

Using English as a "semantic checkpoint" structurally avoids contextual errors that direct translation cannot prevent.

## Architecture Details

This method consists of 5 steps. Step 1 is a language-independent analysis phase, while Step 2 and beyond apply to the target language.

### Step 1: Source-Reference Alignment & Semantic Analysis

#### Goal: Fixation of Meaning and Role (Language-Independent)

Map each word in the source text to the corresponding word in the reference translation (English) to determine the meaning of polysemous words. Furthermore, analyze the role each word plays in the sentence (Subject, Object, Modifier, etc.) at this stage. The target language (e.g., Malayalam) is not considered here at all.

#### Solution: Utilizing Existing Translations and Clarifying Definitions

Translate the entire sentence into English to fix the meanings. It is best to provide a reliable existing English translation (Reference Translation) as input.

It is crucial not just to list English words, but to explicitly verbalize "Contextual Definition" and "Grammatical Role" in separate columns.

**Prompt Example:**

```
### Step 1: Source-Reference Alignment & Semantic Analysis

Perform a word-by-word alignment between the Source Text and the Reference Translation.

Goal: Identify the specific English meaning and precise semantic definition for each Source token in this context.

Instructions:
1. Use Reference for Context: Use the Reference Translation to disambiguate polysemous words (e.g., determining if "vi" is "you" or "there").
2. Define Semantics: For the [Contextual Definition] column, write the specific dictionary definition that applies to this context.
   - Example: For "trattar", do not just write "treat". Write "to discuss; to deal with a subject".
   - Example: For "ben", write "the good; virtue".
3. Analyze Grammar: Identify the grammatical role (Subject, Direct Object, etc.).

Table Columns:
- [Source Word]
- [Morphology] (Lemma, POS)
- [English Equivalent] (Literal word aligned with Source)
- [Contextual Definition] (Specific dictionary sense used here)
- [Grammatical Role] (Syntactic function)

Source Text:
[Input Source Text Here]

Reference Translation (English):
[Input Reliable English Translation Here]
```

This process completely fixes the meaning of polysemous words and the grammatical structure, cutting off misinterpretations at the source for subsequent steps.

### Step 2: Morphosyntactic Requirement Definition

#### Goal: Skeleton and Bonding Strategy for Target Language

Based on the "Definition" and "Role" determined in Step 1, define the rules for "Case" and "Agglutination" required in the target language.

Since the grammatical role (e.g., Direct Object) is already identified in Step 1, this step focuses on the transformation rule: "How to express that role in the target language."

**Adjustment Points for Target Language:**

*   **Method of Case/Suffix Indication:**
    *   **Agglutinative/Inflectional:** Define as "If Direct Object -> Accusative Case," "If Prepositional Phrase -> Suffix."
    *   **Isolating:** Define prepositions to be treated as independent words.

**Prompt Example:**

```
Target Language: [Input Language Name Here]

### Step 2: Morphosyntactic Requirement Definition

Based on the alignment and roles from Step 1, define the grammatical requirements for the Target Language.

Tasks:
1. Map Case/Suffix: Define the Target Language requirement based on the [Grammatical Role] identified in Step 1.
   - If Role is Direct Object -> Assign Accusative Case.
   - If Role is Prepositional Phrase -> Determine the Suffix (e.g., Locative).
2. Tense/Mood Mapping: Map the Source Tense to the appropriate Target Tense.

Output Format (Table):
- [Source Word]
- [Contextual Definition] (from Step 1)
- [Target Requirement] (e.g., "Accusative case (-e)", "Suffix (-il) on next noun")
```

### Step 3: Pre-assembled Lexical Inventory

#### Goal: Creating Assemble-able Parts

Generate words based on the requirements from Step 2. Crucially, elements defined as Suffixes should NOT be listed as separate lines but must be output in their **Agglutinated Form** fused with the corresponding noun. This physically prevents bonding errors in later stages.

**Prompt Example:**

```
### Step 3: Pre-assembled Lexical Inventory

Create a list of Target Language components ready for assembly.

STRICT RULES:
1. Agglutination: If Step 2 identified a word as a Suffix (e.g., "of", "in"), do NOT list it separately. Fuse it immediately with the head noun.
   - Bad: [forest] [in]
   - Good: [forest-in] (e.g., kattil)
2. Case Verification: Ensure the grammatical role from Step 2 is respected.
   - Direct Object: Must use Accusative form (e.g., enne).
3. Lexical Sanity: Ensure words are standard and natural. Verify that the chosen Malayalam word matches the Contextual Definition.

Table Columns:
- [Source Word]
- [Contextual Definition] (English dictionary definition/description of the meaning in this context. Do not just translate the word; explain it. e.g., "to discuss a topic" instead of "treat".)
- [Target Lemma]
- [Final Agglutinated Form] (The fully inflected word to be used in the sentence)
```

**Adjustment Points for Target Language:**

*   **Agglutination Rules:** Designed for agglutinative languages. Not necessary for isolating languages.

### Step 4: Slot-Based Syntactic Assembly

#### Goal: Placement into Structure

Arrange the "Pre-assembled Parts" created in Step 3 into the word order slots of the target language. Instead of abstract instructions, providing specific slot structures prevents word order collapse.

**Prompt Example:**

```
### Step 4: Slot-Based Syntactic Assembly

Arrange the components from Step 3 into a strictly literal Target Language sentence.

Universal Rules:
1. Line Integrity: Do not merge the text into a single paragraph. Translate exactly one Source line at a time. The output must have the same number of lines as the Source.
2. Punctuation Transfer: Strictly copy punctuation marks (commas, periods, exclamation marks) from the end of the Source Line to the end of the Target Line. Do not add artificial periods if the source does not have them.
3. Transparency: Explicitly show which components are used for each line to allow debugging.

Target Language Specific Rules (Example for SOV/Agglutinative languages):
4. Slot Filling: Inside each line, arrange components into the following order: [Subject] + [Time/Place/Manner Adverbials] + [Object] + [Verb]
5. Head-Final Modifiers: Ensure adjectives and genitives are placed before the noun they modify. ([Adjective/Genitive] + [Noun])
6. No New Agglutination: Use the Final Agglutinated Forms from Step 3 exactly as they are. Do not separate suffixes again.

Final Output Format:
For each line, provide:
- Source Line: [Original Text]
- Component Mapping: [List of components used from Step 3 in their new order]
- Assembly Logic: [Brief explanation of word order changes or connections]
- Target Text: [Final translation for this line]
```

**Adjustment Points for Target Language:**

*   **Slot Filling (Word Order) / Modifiers:** Geared towards SOV languages (Japanese, Malayalam). For SVO or VSO languages, rewrite the order of the slots.

### Step 5: Self-Correction via Back-Translation

In automated processing, external human checks are not realistic. Instead, we incorporate a step where the LLM performs "Back-Translation" to self-verify logical consistency.

*   **Round-Trip Check:** Translate the sentence generated in Step 4 back into English (Intermediate Language).
*   **Consistency Verify:** Determine if the back-translation matches the "Locked Meaning" from Step 1, and urge automatic correction if there is a discrepancy.

**Prompt Example:**

```
### Step 5: Self-Correction via Back-Translation & Grammatical Check

Perform the verification and display the results for each step:

Table Columns:
- [Line #]
- [Target Text] (Copy the final text from Step 4)
- [Back-Translation] (Literal English)
- [Source Context] (Original Source text)
- [Verification Result] (OK / Correction Needed)

Rules:
1. Verify Meaning: Compare Back-Translation with the "Locked Meaning" from Step 1.
2. Verify Structure: Check against [Source Context] to ensure no structural elements are ignored.
3. Correction: If there is a mismatch or grammatical error, output a corrected version.
   - Constraint: Do NOT reorder words across lines. Corrections must happen strictly within each line.
4. Final Output: Present the final, verified Target Language text in a code block, separated line by line.
```

### Example of Error Detection (Language Confusion)

In multilingual models, "Language Confusion" can occur where words from a language different from the target language mix in. The back-translation process in Step 5 is effective not only for detecting semantic drifts but also for detecting this kind of anomaly.

**Real Example (Korean mixing into Kannada Translation):**
In a case where the Korean "나는" (I) mixed into the output of Step 4 instead of the Kannada pronoun, the Step 5 verification process detected this as "inappropriate language" and successfully corrected it to the correct Kannada "ನಾನು".

Thus, back-translation checks function as a safety valve filtering not only semantic consistency but also script/language anomalies.

## Evaluation of Translation Quality

Using this method, the first 3 lines of Dante's *Inferno* (Italian original) were translated into Dravidian languages (Telugu, Tamil, Kannada, Malayalam) referencing the English Norton translation. Below, we point out grammatical and lexical issues regarding them as literal translations of the Italian original.

For further details, please refer to [test/README.md](test/README.md).

## Inference Cost and Prospects for Large-Scale Deployment

The method introduced here is an approach to improve quality solely through prompt engineering without changing existing model weights. While easy to try, it faces the challenge of heavy processing and increased token consumption because generating a single translation requires multiple inference steps.

A fundamental solution to resolve this trade-off is to use high-quality data containing this Chain of Thought as training data to retrain the model itself. Specifically, by using Reinforcement Learning (RL) or Supervised Fine-Tuning (SFT) to distill this stepwise reasoning capability into the model, it becomes possible to output high-quality translations equivalent to this method in a single inference step.

However, since retraining such models requires enormous computational resources, it is difficult to execute at an individual level. On the other hand, for companies and research institutes with computational resources, this is already widely practiced as a standard engineering method to ensure scalability.

## Summary

The essence of this prompt engineering method lies in not treating translation merely as a "black box process of LLMs," but in explicitly simulating the cognitive process humans use when translating.

1.  **Meaning Understanding**: Align source and reference to fix meaning. (Language-Independent)
2.  **Requirement Definition**: Decide grammatical specifications (binding rules) required in the target language.
3.  **Vocabulary Selection**: Align correct parts that are inflected/agglutinated.
4.  **Syntax Construction**: Place them according to the slot (blueprint).
5.  **Self-Correction**: Verify and correct accuracy through back-translation and grammatical validation.

This flow serves as a general-purpose solution to achieve high accuracy even with models having fewer parameters in translation between languages with different structures.
