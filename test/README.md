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
2 నేను చీకటి అడవిలో తాను కనుగొన్నాను,
3 అందుకే సరైన మార్గం కోల్పోయింది.

4 అహ్ అది ఏమిటో చెప్పడం ఎంత కష్టం
5 ఈ వన్య మరియు కఠిన మరియు బలమైన అడవి
6 అది ఆలోచనలో భయాన్ని పునరుద్ధరిస్తుంది!

7 ఇంతగా చేదుగా ఉంది, అంటే మరణం కొంచెం ఎక్కువగా ఉంది;
8 కాని నేను అక్కడ కనుగొన్న మంచిని గురించి చర్చించడానికి,
9 నేను అక్కడ చూసిన ఇతర విషయాలను చెప్పుతాను.
```

**Points of criticism (GPT-5.2)**:

- Line 2: Reflexive meaning is broken ("I found myself"); 「తాను」 reads like a pronoun mismatch for 1st person.
- Line 3: 「అందుకే」 means “therefore/so”, but the source is “because/for”.
- Line 7: Comparative scale is incomplete/garbled; “death is a little more” is missing “more (bitter) than it / death is little more”.

## Tamil (GPT-OSS 120B)

```text
1 எங்கள் வாழ்க்கையின் பயணத்தின் நடுவில்
2 நான் ஒரு இருண்ட காடில் தன்னை கண்டேன்,
3 ஏனெனில் சரியான பாதை இழந்துவிட்டது.

4 ஆஹா எவ்வளவு சொல்லுவது அது இருந்தது என்பது கடினமான ஒன்று
5 இந்த காடு காட்டு கடினமான அடர்த்தியானது
6 அது மனதில் பயத்தை மீண்டும் எழுப்புகிறது!

7 அது இவ்வளவு கசப்பாக உள்ளது என்று மரணம் அதைவிட கொஞ்சம் அதிகமாக உள்ளது;
8 ஆனால் நான் அங்கே கண்ட நல்லதைப் பற்றி பேசுவதற்காக,
9 நான் அங்கே பார்த்த மற்றவற்றைச் சொல்லுவேன்.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Ungrammatical/awkward; “how hard it is to say what it was” is not cleanly expressed.
- Line 5: The stacked descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 7: The ellipsis after “more” is acceptable given “bitter” is explicit (OK for literal-first).

## Kannada (GPT-OSS 120B)

```text
1 ನಮ್ಮ ಜೀವನದ ಮಾರ್ಗದ ಮಧ್ಯದಲ್ಲಿ
2 ನಾನು ಕತ್ತಲೆಯ ಕಾಡಿನಲ್ಲಿ ನನ್ನನ್ನು ಕಂಡೆ,
3 ಏಕೆಂದರೆ ಸರಿಯಾದ ಮಾರ್ಗ ಕಳೆದುಹೋಗಿತ್ತು.

4 ಆಹ್ ಎಷ್ಟು ಹೇಳುವುದು ಕಷ್ಟದ ವಿಷಯ ಅದು ಏನು ಆಗಿತ್ತು
5 ಈ ಕಾಡು ಕಾಡು ಕಠಿಣ ಮತ್ತು ದಟ್ಟ
6 ಇದು ಮನಸ್ಸಿನಲ್ಲಿ ಭಯವನ್ನು ಪುನಃ ಉಂಟುಮಾಡುತ್ತದೆ!

7 ಇದು ಅಷ್ಟು ಕಹಿ ಮರಣವು ಸ್ವಲ್ಪ ಹೆಚ್ಚು;
8 ಆದರೆ ನಾನು ಅಲ್ಲಿ ಕಂಡ ಉತ್ತಮವನ್ನು ಚರ್ಚಿಸಲು,
9 ನಾನು ಅಲ್ಲಿ ನೋಡಿದ ಇತರ ವಿಷಯಗಳನ್ನು ಹೇಳುವೆ.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Clause structure is hard to parse; “to tell what it was” is not clearly conveyed.
- Line 5: The descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 7: Comparative is incomplete/ambiguous; missing an explicit target ("than it") and what the “more” refers to.

## Malayalam (GPT-OSS 120B)

```text
1 നമ്മുടെ ജീവിതത്തിന്റെ വഴിയുടെ മധ്യത്തിൽ
2 ഞാൻ ഒരു ഇരുണ്ട കാട്ടിൽ താനെ കണ്ടെത്തി,
3 കാരണം ശരിയായ വഴി നഷ്ടപ്പെട്ടിരുന്നു.

4 അഹ് എന്താണെന്ന് പറയാൻ എത്ര കഠിനമായ കാര്യം
5 ഈ വന്യവും കഠിനവും സാന്ദ്രവുമായ കാട്
6 ചിന്തയിൽ ഭയത്തെ പുതുക്കുന്നു!

7 ഇത് അത്ര കയ്പ്പുള്ളതാണു മരണം അതിനേക്കാൾ അല്പം മാത്രമേ കൂടുതലുള്ളു;
8 എന്നാൽ ഞാൻ അവിടെ കണ്ടെത്തിയ നല്ലതിനെക്കുറിച്ച് സംസാരിക്കാൻ,
9 ഞാൻ അവിടെ കണ്ട മറ്റുള്ള കാര്യങ്ങളെക്കുറിച്ച് പറയും.
```

**Points of criticism (GPT-5.2)**:

- Line 2: 「താനെ」 as 1st-person reflexive is slightly unusual but still recoverable (OK for literal-first).
- Line 7: Comparison leaves “more (bitter)” implicit but “bitter” is explicit (OK for literal-first).

## Japanese (GPT-OSS 120B)

```text
1 人生の道の真ん中で
2 暗い森の中で自分を見つけた、 
3 正しい道が失われていた。

4 ああ、何であるかを語ることはどれほど困難なことか
5 この野生で荒くて濃い森
6 それは思考の中で恐怖を新たにする！

7 それほど苦く死はほんの少しだけそれ以上だ；
8 しかしそこで見つけた善について論じるために、  
9 私がそこで見た他の事柄について語ります。
```

**Points of criticism (GPT-5.2)**:

- Line 3: Missing the causal connector (“for/because”); line 3 reads as a standalone statement.
- Line 7: Comparative is incomplete/unclear; missing “death is little more (bitter)” / explicit comparison target.
- Line 9: Polite register (“語ります”) is a style shift (OK for literal-first).

## French (GPT-OSS 120B)

```text
1 Au milieu du chemin de notre vie
2 Je me retrouvai dans une forêt sombre,
3 car la voie droite était perdue.

4 Ah comme il est difficile de dire ce qu’il était
5 cette forêt sauvage et âpre et dense
6 qui dans la pensée renoue la peur!

7 Si amère est‑elle que la mort n’est que légèrement plus;
8 mais pour traiter du bien que j’ai trouvé là,
9 je dirai des autres choses que j’ai vues là.
```

**Points of criticism (GPT-5.2)**:

- Line 6: 「renoue」 is a slightly off verb choice for “renews” (OK for literal-first).
- Line 7: The “little more (bitter)” comparison is left implicit but “amère” is explicit (OK for literal-first).
- Line 9: 「des autres choses」 reads as “some other things”, not “the other things” (meaning drift).

## Spanish (GPT-OSS 120B)

```text
1 En medio del camino de nuestra vida
2 me encontré dentro de una selva oscura,
3 pues el camino recto se había perdido.

4 Ay cuánto cuesta decir qué era cosa dura
5 esta selva salvaje y áspera y fuerte
6 que en el pensamiento renueva el miedo!

7 Tan amarga que la muerte es poco más;
8 pero para tratar del bien que allí encontré,
9 diré de las otras cosas que allí he visto.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Still awkward/elliptical; “decir qué era” is not cleanly formed.
- Line 7: The ellipsis after “más” is acceptable given “amarga” is explicit (OK for literal-first).

## Portuguese (GPT-OSS 120B)

```text
1 No meio da jornada da nossa vida
2 encontrei‑me numa floresta escura,
3 a via reta estava perdida.

4 Ah quão difícil é dizer o que era coisa dura
5 esta selva selvagem e áspera e densa
6 que no pensamento renova o medo!

7 Tão amargo é que a morte é pouco mais;
8 Mas para tratar do bem que eu encontrei lá,
9 Direi das outras coisas que eu vi lá.
```

**Points of criticism (GPT-5.2)**:

- Line 3: Drops the causal connector (“pois/porque”); the relation to line 2 is weakened.
- Line 4: Unidiomatic/awkward; “how hard it is to say what it was” is not cleanly expressed.
- Line 7: The ellipsis after “pouco mais” is acceptable given “amargo” is explicit (OK for literal-first).
- Lines 8–9: Mid-paragraph capitalization is stylistically inconsistent (OK for literal-first).

## Esperanto (GPT-OSS 120B)

```text
1 Meze de la vojo de nia vivo
2 mi trovis min en malluma arbaro,
3 ĉar la prava vojo estis perdita.

4 Aĥi kiom malfacila afero estas diri kio ĝi estis
5 ĉi tiu sovaĝa kaj aspra kaj densa arbaro
6 kiu en la penso renovigas la timon!

7 Tiom amara estas ĝi ke morto estas iom pli;
8 Sed por trakti pri la bono kiun mi trovis tie,
9 Mi diros pri la aliaj aferoj kiujn mi vidis tie.
```

**Points of criticism (GPT-5.2)**:

- Line 7: Missing an explicit comparator (“ol ĝi”); 「morto estas iom pli」 is incomplete/ambiguous.

## Ranking (GPT-5.2)

Ranking by fewest issues and providing an overall assessment.

(Ranking below ignores any points marked "OK for literal-first".)

1. Malayalam: Excellent fidelity with no meaning-critical issues.
2. French: High quality with only minor article nuance affecting one phrase.
3. Spanish: Strong natural flow with one syntactically awkward exclamatory passage.
4. Esperanto: Generally faithful with one incomplete comparative structure.
5. Portuguese: Solid translation with occasional gaps in logical connectors and phrasing.
6. Tamil: Core meaning conveyed despite some grammatical rough edges and a missing descriptor.
7. Japanese: Captures the contemplative tone well but has gaps in logical connectors and comparative structure.
8. Kannada: Narrative is traceable but shows strain in complex clauses, descriptors, and comparatives.
9. Telugu: Multiple meaning-critical issues in pronouns, causal logic, and comparative structure.
