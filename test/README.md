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
1 మన జీవితం యొక్క ప్రయాణం మధ్యలో
2 నేను ఒక చీకటి అడవిలో తాను కనుగొన్నాను,
3 కోసం ఆ సరైన మార్గం ఉండి కోల్పోయింది.

4 అహ్, అది ఏమిటో చెప్పడానికి ఎంత కఠినమైన విషయం
5 ఈ అడవి అడవిగా మరియు గట్టిగా మరియు బలంగా ఉంది
6 అది ఆలోచనలో ఆ భయాన్ని పునరుద్ధరిస్తుంది!

7 ఇంతగా చేదుగా ఉంది అలానే మరణం కొంచెం ఎక్కువగా ఉంది;
8 కానీ నేను అక్కడ కనుగొన్న ద మంచి గురించి చర్చించడానికి,
9 నేను అక్కడ చేసి చూసిన ఇతర విషయాలను చెప్పుతాను.
```

**Points of criticism (GPT-5.2)**:

- Line 2: Reflexive meaning is broken ("I found myself"); the use of 「తాను」 reads like a 3rd-person/self pronoun mismatch.
- Line 3: The causal clause is garbled; it doesn’t clearly express “because the right way was lost”.
- Line 7: Comparative relation is muddled (reads like “also… death is a little more”); missing a clear “death is little more [bitter] than it”.
- Line 9: Adds an unsupported action nuance (「చేసి」 in 「చేసి చూసిన」), not present in the source.
- Line 8: Stray/typo-like particle in 「కనుగొన్న ద మంచి」 (OK for literal-first).

## Tamil (GPT-OSS 120B)

```text
1 எங்கள் வாழ்க்கையின் பயணத்தின் நடுவில்
2 நான் ஒரு இருண்ட காடில் என்னை கண்டேன்,
3 சரியான பாதை இழந்துவிட்டது.

4 ஆஹா! அது என்ன என்பதை சொல்லுவது எவ்வளவு கடினமானது
5 இந்த காடு காட்டு முரட்டான வலுவானது
6 அது மனதில் பயத்தை மீண்டும் எழுப்புகிறது!

7 அது இவ்வளவு கசப்பாக உள்ளது என மரணம் அதைவிட கொஞ்சம் அதிகமாக உள்ளது;
8 ஆனால் நான் அங்கே கண்ட நல்லதைப் என்று பற்றி பேசுவதற்காக,
9 நான் அங்கே பார்த்துள்ள என்று மற்றவற்றைச் சொல்லுவேன்.
```

**Points of criticism (GPT-5.2)**:

- Line 3: The causal link (“for/because”) is omitted; it reads as a standalone statement.
- Line 8: Grammatical noise in 「நல்லதைப் என்று பற்றி」 weakens “to treat of the good (that) I found there”.
- Line 9: 「பார்த்துள்ள என்று」 is ungrammatical/unstable and disrupts “the other things I have seen there”.
- Line 7: Ellipsis after “more” is acceptable given the preceding “bitter” (OK for literal-first).

## Kannada (GPT-OSS 120B)

```text
1 ನಮ್ಮ ಜೀವನದ ಮಾರ್ಗದ ಮಧ್ಯದಲ್ಲಿ
2 ನಾನು ಒಂದು ಕತ್ತಲೆ ಕಾಡಿನಲ್ಲಿ ನನ್ನನ್ನು ಕಂಡೆ,
3 ಆದ್ದರಿಂದ ಆ ಸರಿಯಾದ ಮಾರ್ಗ ಕಳೆದುಹೋಗಿತ್ತು.

4 ಆಹ್! ಎಷ್ಟು ಹೇಳಲು ಏನು ಆಗಿತ್ತು ಎಂದು ಹೇಳುವುದು ಕಷ್ಟದ ವಿಷಯ
5 ಈ ಕಾಡು ಕಾಡುಸ್ವಭಾವದ, ಕಠಿಣ ಮತ್ತು ದಟ್ಟ
6 ಇದು ಮನಸ್ಸಿನಲ್ಲಿ ಭಯವನ್ನು ಪುನಃ ಉಂಟುಮಾಡುತ್ತದೆ!

7 ಇದು ಅಷ್ಟು ಕಹಿ ಎಂದು, ಮರಣವು ಸ್ವಲ್ಪ ಹೆಚ್ಚು;
8 ಆದರೆ ಅಲ್ಲಿ ನಾನು ಕಂಡ ಉತ್ತಮವನ್ನು, ಅದನ್ನು, ಚರ್ಚಿಸಲು,
9 ಅಲ್ಲಿ ನಾನು ನೋಡಿದ ಇತರ ವಿಷಯಗಳ ಬಗ್ಗೆ ಹೇಳುವೆ.
```

**Points of criticism (GPT-5.2)**:

- Line 3: 「ಆದ್ದರಿಂದ」 (“therefore/so”) reverses the intended causal relation (should be “because/for”).
- Line 4: Clause structure is hard to parse; “to tell what it was” is not cleanly conveyed.
- Line 7: 「ಮರಣವು ಸ್ವಲ್ಪ ಹೆಚ್ಚು」 lacks an explicit comparison target (“than it” / “bitter”) and reads incomplete.

## Malayalam (GPT-OSS 120B)

```text
1 നമ്മുടെ ജീവിതത്തിന്റെ വഴിയുടെ മധ്യത്തിൽ
2 ഞാൻ താനെ ഒരു ഇരുണ്ട കാട്ടിൽ കണ്ടെത്തി,
3 അങ്ങനെ ശരിയായ വഴി നഷ്ടപ്പെട്ടിരുന്നു.

4 അഹ് അത് എന്തായിരുന്നു എന്ന് പറയാൻ എത്ര കഠിനമായ കാര്യമാണെന്ന്
5 ഈ വന്യവും കഠിനവും സാന്ദ്രവുമായ കാട്ടു
6 അത് ചിന്തയിൽ ഭയത്തെ പുതുക്കുന്നു!

7 ഇത് അത്ര കയ്പ്പുള്ളതാണു മരണം അതിനേക്കാൾ അല്പം മാത്രമേ കൂടുതലുള്ളൂ;
8 എന്നാൽ ഞാൻ അവിടെ കണ്ടെത്തിയ നല്ലതിനെക്കുറിച്ച് വേണ്ടി സംസാരിക്കാൻ,
9 ഞാൻ അവിടെ കണ്ടിട്ടുണ്ട് മറ്റുള്ള കാര്യങ്ങളെക്കുറിച്ച് പറയും.
```

**Points of criticism (GPT-5.2)**:

- Line 8: 「നല്ലതിനെക്കുറിച്ച് വേണ്ടി」 has redundant/awkward marking; intent is still recoverable (OK for literal-first).
- Line 9: Word order + 「കണ്ടിട്ടുണ്ട്」 reads clunky but remains understandable (OK for literal-first).

## Japanese (GPT-OSS 120B)

```text
1 人生の道の真ん中で
2 ある暗い森の中で自分を見つけた、 
3 それでその正しい道が失われていた。

4 ああ、どれほど語ることは何だったことが困難だ
5 この野生で荒くてと濃い森
6 それは思考の中で恐怖を新たにする！

7 それほど苦く死はほんの少しだけそれ以上に苦い;
8 しかし私がそこで見つけた善について論じるために,
9 私はそこで見た他の事柄について語ろう.
```

**Points of criticism (GPT-5.2)**:

- Line 3: 「それで」 suggests “therefore/so” rather than the intended “because/for”.
- Line 4: Ungrammatical; the meaning “how hard it is to say what it was” is hard to recover.
- Line 5: Fragmentary/ungrounded adjective bundle; does not cleanly render the stacked descriptors.
- Lines 7–9: Mixed semicolon/comma usage is stylistically rough (OK for literal-first).

## French (GPT-OSS 120B)

```text
1 Au milieu du chemin de notre vie
2 Je me retrouvai dans une forêt sombre,
3 car la voie droite était perdue.

4 Ah comme il est difficile de dire ce qu'était, c'est une chose dure
5 cette forêt sauvage et âpre et dense
6 qui dans la pensée renoue la peur!

7 Si amère qu’elle est, la mort n’est que légèrement plus;
8 mais pour traiter du bien que j’ai trouvé là,
9 je dirai les autres choses que j’ai vues là.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Run-on/duplicated framing (“…c’est une chose dure”) clutters the clause and weakens readability.
- Line 6: 「renoue la peur」 is a slightly off verb choice for “renews” (OK for literal-first).
- Line 7: The “little more [bitter]” comparison is left implicit (OK for literal-first).

## Spanish (GPT-OSS 120B)

```text
1 En medio del camino de nuestra vida
2 me encontré dentro de una selva oscura,
3 pues el camino recto se había perdido.

4 Ay cuánto cuesta decir qué era es cosa dura
5 esta selva salvaje y áspera y fuerte
6 que en el pensamiento renueva el miedo!

7 Tan amarga es que la muerte es poco más;
8 pero para tratar del bien que allí yo encontré,
9 diré de las otras cosas que allí yo he visto.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Grammar break in 「qué era es」; the line is awkward to parse.
- Line 7: Ellipsis in 「la muerte es poco más」 is acceptable given the preceding “amarga” (OK for literal-first).

## Portuguese (GPT-OSS 120B)

```text
1 No meio da jornada da nossa vida
2 encontrei‑me numa floresta escura,
3 pois o caminho reto estava perdido.

4 Ah quão difícil é a dizer qual era a coisa
5 esta selva selvagem e áspera e densa
6 que no pensamento renova o medo!

7 Tão amargo é isso que a morte é pouco mais;
8 Mas para tratar do bem que eu encontrei lá,
9 Direi das outras coisas que eu tenho visto lá.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Grammar/idiom error in 「é a dizer」; should be 「é dizer」 / 「é difícil dizer」.
- Lines 8–9: Mid-paragraph capitalization (Mas/Direi) is stylistically inconsistent (OK for literal-first).

## Esperanto (GPT-OSS 120B)

```text
1 En la mezo de la vojo de nia vivo
2 mi trovis min en malluma arbaro,
3 ĉar la prava vojo estis perdita.

4 Aĥi kiom malfacila afero estas por diri kio ĝi estis
5 ĉi tiu sovaĝa kaj aspra kaj densa arbaro
6 kiu en penso renovigas la timon!

7 Tiom amara estas ĝi ke morto estas iom pli;
8 Sed por trakti pri la bono kiun mi trovis tie,
9 Mi diros pri la aliaj aferoj kiujn mi tie vidis.
```

**Points of criticism (GPT-5.2)**:

- Line 7: Missing an explicit comparator (“ol ĝi”); 「morto estas iom pli」 is incomplete/ambiguous.
- Line 4: Phrasing/punctuation could be cleaner but meaning is still recoverable (OK for literal-first).

## Ranking (GPT-5.2)

Ranking by fewest issues and providing an overall assessment.

(Ranking below ignores any points marked "OK for literal-first".)

1. Malayalam: No issues noted; remaining points are stylistic only.
2. French: Very close overall; main issue is the run-on/duplicated line 4.
3. Portuguese: Close overall; main issue is the unidiomatic/incorrect line 4 phrasing.
4. Spanish: Mostly faithful; main issue is the line 4 grammar break.
5. Esperanto: Generally faithful; main issue is the incomplete comparative in line 7.
6. Tamil: Understandable overall, but drops the causal link (line 3) and has instability in lines 8–9.
7. Kannada: Traceable, but has a flipped causal connector (line 3), a broken line 4, and an incomplete line 7.
8. Japanese: Multiple grammar failures (lines 4–5) plus a flipped causal connector (line 3).
9. Telugu: Several meaning-critical issues (broken reflexive in line 2, garbled line 3, incomplete comparative in line 7, added action in line 9).
