This project originally focused on translating Dante's "Divine Comedy" into Dravidian languages (Telugu, Tamil, Kannada, Malayalam), which are SOV agglutinative languages with limited training data in most LLMs. However, the translation methodology proved to be general-purpose and language-agnostic, containing no language-specific instructions.

Following successful generalization, additional target languages were added to validate the methodology's versatility: Japanese (another SOV agglutinative language), Romance languages closely related to Italian (French, Spanish, Portuguese), and Esperanto (a constructed auxiliary language with vocabulary and syntax heavily influenced by Romance languages).

The examples below show translations of the first 9 lines of Dante's "Divine Comedy" Inferno (original Italian), referencing the English translation (Norton). Grammatical and vocabulary issues are pointed out as a literal translation of the Italian original.

## Italian (Dante)

```text
1 Nel mezzo del cammin di nostra vita
2 mi ritrovai per una selva oscura,
3 ché la diritta via era smarrita.

4 Ahi quanto a dir qual era è cosa dura
5 esta selva selvaggia e aspra e forte
6 che nel pensier rinova la paura!

7 Tant' è amara che poco è più morte;
8 ma per trattar del ben ch'i' vi trovai,
9 dirò de l'altre cose ch'i' v'ho scorte.
```

## English (Norton)

> Midway upon the road of our life I found myself within a dark wood, for the right way had been missed.
> Ah! how hard a thing it is to tell what this wild and rough and dense wood was, which in thought renews the fear!
> So bitter is it that death is little more. But in order to treat of the good that there I found, I will tell of the other things that I have seen there.

## Telugu (GPT-OSS 120B)

```text
1 మన జీవితము యొక్క మార్గం మధ్యలో
2 నేను ఒక చీకటి అడవిలో తాను కనుగొన్నాను,
3 అందుకే సరైన మార్గం కోల్పోయింది.

4 అయ్యో చెప్పడానికి ఎంత కష్టం అది ఏమిటో
5 ఈ అడవి వన్యమైన మరియు గట్టిగా మరియు ఘనంగా ఉంది
6 అది ఆలోచనలో భయాన్ని పునరుద్ధరించుతుంది!

7 అంతగా చేదుగా ఉంది, మరణం కొంచెం ఎక్కువగా ఉంది;
8 కానీ నేను అక్కడ కనుగొన్న మంచి గురించి చర్చించడానికి,
9 నేను అక్కడ చూసిన ఇతర విషయాలను చెప్పుతాను.
```

**Points of criticism (GPT-5.2)**:

- Line 2: “found myself” reflexive/argument structure is awkward. (OK for literal-first)
- Line 3: Causal marker reads as “therefore/so”, not “for/because”; the causal relation is weakened.
- Line 4: “what it was” is not explicitly realized.
- Line 7: Comparative is incomplete: “death is a little more” lacks an explicit scale/property (i.e., “more bitter”).

## Tamil (GPT-OSS 120B)

```text
1 எங்கள் வாழ்க்கையின் பாதையின் நடுவில்
2 நான் ஒரு இருண்ட காடில் என்னை கண்டேன்,
3 அதனால் அந்த சரியான பாதை தவறாகி விட்டது.

4 ஆஹ் அதை என்ன இருந்தது என்று சொல்ல எவ்வளவு கடினமானது என்பது ஒரு கடினமான விஷயம்
5 இந்த காட்டுப்பகுதி காட்டு மற்றும் கடினமான மற்றும் அடர்த்தியானது
6 அது நினைவில் அந்த பயத்தை புதுப்பிக்கிறது!

7 அதிகமாக கசப்பாக என்று மரணம் சிறிது அதிகம் உள்ளது;
8 ஆனால் நான் அங்கே கண்ட நல்லதைப் பற்றி விவாதிக்க,
9 நான் அங்கே பார்த்துள்ள மற்றவற்றைச் சொல்லுவேன்.
```

**Points of criticism (GPT-5.2)**:

- Line 3: Causal connector reads as “therefore/so”, not “for/because”.
- Line 4: Tautological/overlong (“hard … a hard thing”); structure is not clean. (OK for literal-first)
- Line 6: Uses “memory” rather than “thought”, drifting from the reference framing.
- Line 7: Comparative is not clean: missing the explicit “so bitter is it” frame and/or the comparison scale.

## Kannada (GPT-OSS 120B)

```text
1 ನಮ್ಮ ಜೀವನದ ಮಾರ್ಗದ ಮಧ್ಯದಲ್ಲಿ
2 ನಾನು ಒಂದು ಕತ್ತಲೆಯ ಕಾಡಿನಲ್ಲಿ ನನ್ನನ್ನು ಕಂಡುಕೊಂಡೆ,
3 ಆದರಿಂದ ಸರಿಯಾದ ಮಾರ್ಗವು ಕಳೆದುಹೋಗಿತ್ತು.

4 ಆಹ್ ಇದು ಎಷ್ಟು ಕಷ್ಟದ ವಿಷಯ ಎಂದು ಏನು ಆಗಿತ್ತು ಎಂದು ಹೇಳಲು
5 ಈ ಕಾಡು ಕಾಡು ಮತ್ತು ಕಠಿಣ ಮತ್ತು ದಟ್ಟ
6 ಇದು ಮನಸ್ಸಿನಲ್ಲಿ ಭಯವನ್ನು ಪುನಃ ಉಂಟುಮಾಡುತ್ತದೆ!

7 ಅದು ಅಷ್ಟು ಕಹಿ ಇದೆ ಎಂದು ಮರಣವು ಸ್ವಲ್ಪ ಹೆಚ್ಚು ಇದೆ;
8 ಆದರೆ ನಾನು ಅಲ್ಲಿ ಕಂಡ ಉತ್ತಮವನ್ನು ಚರ್ಚಿಸಲುಗಾಗಿ,
9 ನಾನು ಅಲ್ಲಿ ನೋಡಿದ ಇತರ ವಿಷಯಗಳ ಬಗ್ಗೆ ಹೇಳುವೆ.
```

**Points of criticism (GPT-5.2)**:

- Line 3: Causal connector reads as “therefore/so”, not “for/because”.
- Line 4: Scrambled phrasing; “what it was” is not explicit.
- Line 5: Repetition is clumsy (OK for literal-first), but the descriptor bundle is incomplete; mapping to wild/rough/dense/strong is not clean.
- Line 7: Comparative is incomplete; the scale/property for “a little more” is not explicit.

## Malayalam (GPT-OSS 120B)

```text
1 നമ്മുടെ ജീവിതത്തിന്റെ വഴിയുടെ മദ്ധ്യത്തിൽ
2 ഞാൻ ഒരു ഇരുണ്ട കാട്ടിൽ താനെ കണ്ടെത്തി,
3 അതിനാൽ ശരിയായ വഴി നഷ്ടപ്പെട്ടിരുന്നു.

4 അഹ് എത്ര പറയാൻ എന്തായിരുന്നു അത് ആണ് കഠിനമായ കാര്യം
5 ഈ വന്യവും കഠിനവും ശക്തവുമായ കാട്
6 അത് ചിന്തയിൽ ഭയത്തെ പുതുക്കുന്നു!

7 അത്രയേറെ കയ്പ്പാണ് അത് എന്നാൽ മരണം അല്പം കൂടുതലാണ്;
8 പക്ഷേ അവിടെ ഞാൻ കണ്ടെത്തിയത് നല്ലതിനെ പരിചരിക്കാൻ,
9 ഞാൻ അവിടെ കണ്ടത് മറ്റ കാര്യങ്ങളെപ്പറ്റി പറയും.
```

**Points of criticism (GPT-5.2)**:

- Line 3: Causal connector reads as “therefore/so”, not “for/because”.
- Line 4: Scrambled/ill-formed; “what it was” is not explicit.
- Line 5: Descriptor bundle is incomplete (missing at least one of dense/strong/rough); attachment is not fully clean.
- Line 7: Comparative is incomplete; the scale/property for “a little more” is not explicit.
- Line 8: Verb choice drifts (“take care of the good”) instead of “treat/discuss the good”.

## Japanese (GPT-OSS 120B)

```text
1 我々の人生の道の途中で
2 ある暗い森の中で自分を見つけた、
3 その正しい道が見失われていたために。

4 ああ、何であったかを語ることに、とても困難なことだ
5 この野生で荒々しく、そして、そして厚い森
6 それは思いの中でその恐怖を新たにする！

7 それほど苦いほど死はほんの少しだけ上回る;
8 しかし私がそこで見つけた善について論じるために、
9 私がそこで見た他の事柄を語ろう。
```

**Points of criticism (GPT-5.2)**:

- Line 4: Awkward phrasing; “what it was” is not cleanly expressed.
- Line 5: Duplicate connector (“そして、そして”); descriptor bundle is clumsy. (OK for literal-first)
- Line 6: “renews the fear” is paraphrased (“make it new”), reducing literal correspondence.
- Line 7: Comparative is incomplete/elliptical; the comparison scale/property is not explicit.

## French (GPT-OSS 120B)

```text
1 Au milieu du chemin de notre vie
2 je me retrouvai dans une forêt sombre,
3 car la voie droite avait été perdue.

4 Ah comme il est dur de dire ce qu'était cette chose
5 cette forêt sauvage et âpre et dense
6 qui dans la pensée renouvelle la peur!

7 Tellement amère est‑elle que la mort n’est que légèrement plus;
8 mais pour traiter du bien que j’ai trouvé là,
9 je dirai des autres choses que j’ai vues là.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Slightly indirect phrasing; correspondence is acceptable but not maximally literal. (OK for literal-first)
- Line 7: Comparative is incomplete/elliptical (“la mort n’est que légèrement plus” lacks the explicit scale/property, i.e., “plus amère”).

## Spanish (GPT-OSS 120B)

```text
1 En medio del camino de nuestra vida
2 me encontré en una selva oscura,
3 pues la recta vía estaba perdida.

4 Ay cuanto es cosa dura a decir qué era
5 esta selva salvaje y áspera y fuerte
6 que en el pensamiento renueva la miedo!

7 Tan amarga es que la muerte es poco más;
8 Pero para tratar del bien que allí encontré,
9 Diré de las otras cosas que allí he visto.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Awkward structure; “what it was” is only partially realized. (OK for literal-first)
- Line 6: Agreement/grammar error (“la miedo”).
- Line 7: Comparative is incomplete (“la muerte es poco más” lacks the explicit scale/property).

## Portuguese (GPT-OSS 120B)

```text
1 No meio do caminho da nossa vida
2 encontrei‑me numa selva escura,
3 pois a via direita estava perdida.

4 Ai quão difícil é a dizer o que era coisa dura
5 esta selva selvagem e áspera e forte
6 que no pensamento renova o medo!

7 Tão amarga é que a morte é pouco mais;
8 Mas para tratar do bem que lá encontrei,
9 Direi das outras coisas que lá tinha visto.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Awkward phrasing (“é a dizer”); structure is not clean.
- Line 7: Comparative is incomplete (“a morte é pouco mais” lacks the explicit scale/property).
- Line 9: Tense/aspect drifts (“tinha visto” adds an unnecessary past-perfect nuance). (OK for literal-first)

## Esperanto (GPT-OSS 120B)

```text
1 En la mezo de la vojo de nia vivo
2 Mi trovis min en malluma arbaro,
3 ĉar la prava vojo estis perdita.

4 Ho, kiom malfacila estas por diri kio ĝi estis
5 ĉi tiu sovaĝa kaj aspra kaj densa arbaro
6 kiu en pensado renovigas la timon!

7 Tiom amara estas ĝi ke morto estas iom pli;
8 Sed por trakti bonon kiun mi trovis tie,
9 Mi diros pri la aliaj aferoj kiujn mi jam vidis tie.
```

**Points of criticism (GPT-5.2)**:

- Line 7: Comparative is incomplete (“morto estas iom pli” lacks the explicit scale/property, i.e., “pli amara”).
- Line 9: Adds “jam” (“already”), which is not supported by the source/reference.
- Capitalization varies by line, reducing stylistic consistency. (OK for literal-first)

## Ranking (GPT-5.2)

Ranking by fewest issues and providing an overall assessment.

(Ranking below ignores any points marked "OK for literal-first".)

1. French: Very close overall; main issue is the incomplete comparative scale in line 7.
2. Portuguese: Close overall; remaining issues are awkward line 4 phrasing and the incomplete comparative scale in line 7.
3. Esperanto: Generally faithful, but line 7 is incomplete and line 9 adds unsupported “already”.
4. Spanish: Mostly faithful, but has a clear agreement error (line 6) and an incomplete comparative (line 7).
5. Japanese: Mostly faithful, but has awkward line 4 phrasing, paraphrase in line 6, and an incomplete comparative in line 7.
6. Telugu: Good overall coverage, but the causal connector can read as “therefore/so” and the line 7 comparative scale is incomplete.
7. Tamil: Readable, but drifts in line 6 (“memory” vs “thought”) and has an incomplete comparative in line 7.
8. Kannada: Roughly traceable, but has an incomplete descriptor bundle (line 5) and an incomplete comparative scale (line 7).
9. Malayalam: Generally stable, but has multiple drift points (line 8 verb choice) and an incomplete comparative scale (line 7).
