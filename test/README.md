This project originally focused on translating Dante's "Divine Comedy" into Dravidian languages (Telugu, Tamil, Kannada, Malayalam), which are SOV agglutinative languages with limited training data in most LLMs. However, the translation methodology proved to be general-purpose and language-agnostic, containing no language-specific instructions.

Following successful generalization, additional target languages were added to validate the methodology's versatility: Japanese (another SOV agglutinative language), Romance languages closely related to Italian (French, Spanish, Portuguese), and Esperanto (a constructed auxiliary language with vocabulary and syntax heavily influenced by Romance languages).

The examples below show translations of the first 9 lines of Dante's "Divine Comedy" Inferno (original Italian), referencing the English translation (Norton). Grammatical and vocabulary issues are pointed out as a literal translation of the Italian original.

# Source Texts

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

# Dravidian languages

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

# Agglutinative non-Dravidian languages

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

## Estonian (GPT-OSS 120B)

```text
1 Meie elu teekonna keskel
2 Leidsin end pimedas metsas,
3 sest õige tee oli kaotatud.

4 Ah kui raske on öelda mis see oli
5 see mets on metsik ja karm ja tihe
6 mis mõttes uuendab hirmu!

7 Nii kibe on see et surm on veidi rohkem;
8 Aga et käsitleda head mida seal leidsin,
9 Räägin teistest asjadest mida seal olen näinud.
```

**Points of criticism (GPT-5.2)**:

- Line 5: The descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 6: “in thought” is rendered awkwardly; 「mis mõttes」 reads like “in meaning” rather than “in thought/mind”.
- Line 7: Comparative ellipsis (“death is a little more …”) is acceptable given “bitter” is explicit (OK for literal-first).

## Turkish (GPT-OSS 120B)

```text
1 Hayatımızın yolunun ortasında
2 kendimi karanlık bir ormanda buldum,
3 öyle ki doğru yol kaybolmuştu.

4 Ah ne söylemek ki ne olduğu zor bir şey
5 bu vahşi ve engebeli ve yoğun orman
6 ki düşüncede korkuyu yeniden canlandırır!

7 Öyle acı ki ölüm biraz daha fazladır;
8 Ama orada bulduğum iyiyi ele almak için,
9 Orada gördüğüm diğer şeyleri anlatacağım.
```

**Points of criticism (GPT-5.2)**:

- Line 3: 「öyle ki」 reads like “so that/such that”, not a clean causal “because/for”.
- Line 4: Ungrammatical/awkward; “how hard it is to say what it was” is not cleanly expressed.
- Line 5: Descriptor drift; 「engebeli」 (“bumpy/uneven”) does not match the source’s “rough/harsh/strong” bundle.
- Line 7: Comparative ellipsis (“death is a little more …”) is acceptable given “acı” is explicit (OK for literal-first).

# Romance languages

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

# Constructed languages

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

## Interlingua (GPT-OSS 120B)

```text
1 In medio del cammino de nostre vita
2 io me trovava in una selva obscure,
3 pro le via recte esseva perdita.

4 Ah quanto es difficile dicer qual era iste cosa
5 iste selva selvage e aspra e forte
6 que in le pensamento renova le paura!

7 Tanto es amar que poco es plus morte;
8 ma pro tractar del bon que io trovava ibi,
9 io dicera del alter cosas que io ha vidite ibi.
```

**Points of criticism (GPT-5.2)**:

- Line 2: Aspect/tense is off; 「io me trovava」 (imperfect) blurs the “I found myself” event.
- Line 9: Form/grammar is shaky ("alter" vs "altere"); weakens “the other things”.

# Indo-Iranian languages

## Hindi (GPT-OSS 120B)

```text
1 हमारी ज़िन्दगी के मार्ग के मध्य में
2 मैं खुद को एक अंधेरे जंगल में पाया,
3 क्योंकि सही रास्ता खो गया था।

4 आह यह बताना कि वह क्या था कितना कठिन काम है
5 यह जंगली और खुरदरा और घना वन
6 जो विचार में भय को फिर से जगा देता है!

7 यह इतनी कड़वी है कि मृत्यु उससे थोड़ा अधिक कड़वी है;
8 परन्तु मैं जहाँ अच्छा पाया उसके बारे में चर्चा करने के लिये,
9 मैं वहाँ देखी गई अन्य चीज़ों के बारे में बताऊँगा।
```

**Points of criticism (GPT-5.2)**:

- Line 7: Makes the comparison explicit as “death is a little more bitter than it”; acceptable under literal-first but slightly shifts emphasis (OK for literal-first).
- Line 8: 「जहाँ अच्छा पाया」 uses “where” where “there” is intended; slightly distorts “the good that there I found”.

## Bengali (GPT-OSS 120B)

```text
1 আমাদের জীবনের পথে মাঝখানে
2 আমি নিজেকে এক অন্ধকার বনে পেলাম,
3 কারণ সঠিক পথ হারিয়ে গিয়েছিল।

4 আহ কী কঠিন কাজ এটি বলতে যে তা কী ছিল
5 এই বন বন্য এবং কঠোর এবং ঘন
6 যা চিন্তায় ভয়কে পুনরুজ্জীবিত করে!

7 এতটাই তিক্ত যে মৃত্যু সামান্য বেশি;
8 কিন্তু আমি সেখানে যে মঙ্গল পেয়েছি তা নিয়ে আলোচনা করতে,
9 আমি সেখানে যে অন্যান্য জিনিসগুলি দেখেছি সেগুলি বলব।
```

**Points of criticism (GPT-5.2)**:

- Line 5: The descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 7: Comparative ellipsis (“death [is] a little more …”) is acceptable given “bitter” is explicit (OK for literal-first).

# Germanic languages

## German (GPT-OSS 120B)

```text
1 Mitten auf dem Weg unseres Lebens
2 fand ich mich in einem dunklen Wald,
3 denn der rechte Weg war verfehlt.

4 Ach wie schwer ist es zu sagen was es war
5 dieser Wald ist wild und rau und dicht
6 der im Denken die Angst erneuert!

7 So bitter ist es, dass der Tod nur ein wenig mehr bitter ist;
8 Aber um das Gute zu behandeln, das ich dort fand,
9 Ich werde von den anderen Dingen erzählen, die ich dort gesehen habe.
```

**Points of criticism (GPT-5.2)**:

- Line 7: "ein wenig mehr bitter" is clunky; the comparison is understandable but stylistically strained (OK for literal-first).

## Dutch (GPT-OSS 120B)

```text
1 Midden op de weg van ons leven
2 Vond ik mezelf in een donker bos,
3 want de juiste weg was gemist.

4 Ach hoe moeilijk het is om te vertellen wat het was is een harde zaak
5 dit woud is wild en ruw en dicht
6 die in gedachten de angst vernieuwt!

7 Zo bitter is het dat de dood iets meer is;
8 Maar om het goede dat ik daar vond te behandelen,
9 Ik zal over de andere dingen die ik daar heb gezien vertellen.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Ungrammatical word order/run-on; the clause is hard to parse.
- Line 6: Relative pronoun agreement error (“woud” is neuter; should be “dat” not “die”).
- Line 7: Comparative is incomplete/unclear (“de dood iets meer is” — more what?).

# Slavic languages

## Serbian (Latin script) (GPT-OSS 120B)

```text
1 U sredini puta našeg života
2 našao sam se u mračnoj šumi,
3 jer prava staza je bila izgubljena.

4 Ah koliko je teško reći šta je bila teška stvar
5 ova šuma divlja i gruba i gusta
6 koja u mislima obnavlja strah!

7 Tako je gorka da je smrt malo više;
8 Ali da bih govorio o dobru koje sam tamo našao,
9 Reći ću o drugim stvarima koje sam tamo video.
```

**Points of criticism (GPT-5.2)**:

- Line 4: Ungrammatical/duplicative; “teško reći šta je bila teška stvar” does not cleanly express “how hard it is to say what it was”.
- Line 7: Comparative ellipsis (“death is a little more …”) is acceptable given “gorka” is explicit (OK for literal-first).

## Bulgarian (GPT-OSS 120B)

```text
1 В средата на пътя на нашия живот
2 се намерих в тъмна гора,
3 защото правият път беше изгубен.

4 Ах колко трудно е да се каже какво беше
5 това диво и грубо и плътно дърво
6 което в мисълта възобновява страха!

7 Така е горчиво че смъртта е малко повече;
8 Но за да разгледам доброто което намерих там,
9 Ще разкажа за другите неща които видях там.
```

**Points of criticism (GPT-5.2)**:

- Line 5: Uses 「дърво」 (“tree/wood”) where “forest/wood” is intended; meaning drift from “selva/wood”.
- Line 5: The descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 7: Comparative ellipsis (“death is a little more …”) is acceptable given “горчиво” is explicit (OK for literal-first).

## Polish (GPT-OSS 120B)

```text
1 W połowie drogi naszego życia
2 odnalazłem się w mrocznym lesie,
3 bo właściwa droga została zgubiona.

4 Ach jak trudne jest powiedzieć czym to było
5 ten dziki i szorstki i gęsty las
6 który w myśli odnawia strach!

7 Tak gorzka jest że śmierć jest nieco większa;
8 ale aby rozmawiać o dobru które znalazłem tam,
9 powiem o innych rzeczach które widziałem tam.
```

**Points of criticism (GPT-5.2)**:

- Line 5: The descriptor bundle is incomplete (missing the “strong/forte” component).
- Line 7: Comparative meaning drifts; 「śmierć jest nieco większa」 (“death is a bit bigger/greater”) does not preserve “death is little more (bitter)”.

## Ranking (GPT-5.2)

Ranking by fewest issues and providing an overall assessment.

(Ranking below ignores any points marked "OK for literal-first".)

1. Malayalam: Excellent fidelity with no meaning-critical issues.
2. German: Excellent fidelity; only minor stylistic strain noted.
3. French: High quality with only a small meaning nuance in line 9.
4. Hindi: Very faithful overall; one minor deictic choice in line 8.
5. Spanish: Strong flow with one syntactically awkward exclamatory passage.
6. Bengali: Readable and faithful, but drops one descriptor in line 5.
7. Esperanto: Generally faithful with one incomplete comparative structure.
8. Serbian: Traceable overall, but the complex exclamatory clause in line 4 breaks down.
9. Interlingua: Very close overall; minor tense/grammar instability.
10. Portuguese: Solid translation with gaps in logical connectors and awkward line 4 phrasing.
11. Estonian: Mostly faithful, but has one missing descriptor and an awkward “in thought” rendering.
12. Tamil: Core meaning conveyed despite grammatical rough edges and a missing descriptor.
13. Bulgarian: Mostly faithful, but has a forest/wood meaning drift and a missing descriptor.
14. Polish: Mostly faithful, but the comparative in line 7 drifts (“bigger/greater” vs “little more (bitter)”).
15. Japanese: Understandable overall, but drops the causal connector and has an incomplete comparative.
16. Kannada: Narrative is traceable but shows strain in complex clauses, descriptors, and comparatives.
17. Turkish: Traceable overall, but has a wrong causal framing (line 3) and breaks down in the exclamatory clause/descriptor bundle.
18. Dutch: Multiple clear grammar/agreement failures plus an incomplete comparative.
19. Telugu: Multiple meaning-critical issues in pronouns, causal logic, and comparative structure.
