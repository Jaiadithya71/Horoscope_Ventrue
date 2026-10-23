# Bhavat Bhavam logic from the dasha-bhukti video (engine candidate)

Source video: https://youtu.be/ONyljEHjHQo

Full transcript: dasha-bhukti-video-transcript-ta.md (in this directory, stored as a research reference at the repo owner's direction; rights remain with the creator). These notes are our own paraphrase of the reported reasoning, not permission to reuse the creator's spoken text.

## Video (https://youtu.be/ONyljEHjHQo), Tamil, "why a well-placed planet gives bad results in its own dasha-bhukti"
Source: YouTube Tamil auto-captions (no manual subtitles; English track rate-limited, so Tamil only). Channel/speaker name not captured. Captions are auto-generated and some words are garbled; Tamil kept in my paraphrase, not verbatim. A short video followed by a course advertisement. The advertised course date is not verified and is not used here. The speaker's rule is a practitioner claim, not a cited classical text.

Full reasoning, in order:
1. Question: a planet is in a good house and has good lordship, yet its dasha-bhukti brings bad results. Why?
2. Example: Aquarius lagna. Jupiter (lord of 2 and 11) sits in the 11th. Lordship and house are good. Yet in Jupiter's dasha there is trouble: the 4th house of Aquarius is Taurus, and Jupiter in the 11th is in the 8th from Taurus. So the mother can face affliction or humiliation, property disputes, unrecoverable debt, even her death.
3. Principle "Bhavat Bhavam" (house from the house): the same planet can do good for the native while harming a relative or close circle. A planet in the 11th is good for the native but is 8th from the 4th, so it hurts what the 4th signifies (mother, property).
4. Rule as stated: for any planet, look at the houses counted from the houses it occupies. Where it falls 6th or 8th from a house (bhava), it harms that house's significations, and the warning must be given alongside the good result. "Even a planet that gives only gains (11th) will certainly harm mother and property" is his stated assertion.
5. Trigger: whenever a chart has a planet in own sign (aatchi), exaltation (ucham) or debilitation (neecham), the Bhavat Bhavam effect is certain to operate for the house of that rasi. A chart with three planets in own sign and two exalted can drive the whole family.
6. Timing: if several planets are in own/exalted sign, the effect stays dormant until the relevant dasha-bhukti arrives. With three or four such planets, it works when the dasha comes.
7. Split case: three planets in own sign as dasha lord, bhukti lord, antara lord can do very well for the native and hurt his relations. He gives an example of a native who takes loans from everyone and leaves, wrecking lenders (loosely phrased; low confidence on the caption).

Engine extraction (candidate, needs owner and classical cross-check):
- Per dasha/bhukti lord: compute house of placement P. For each house H where ((P - H) mod 12) + 1 is 6 or 8, flag "dasha of this planet may trouble H's significations" in addition to its own results. Separate output channel "effects on others/significations of H" from "effects on native".
- Condition flag: stronger when the planet is in own/exalted/debilitated sign (his statement), dormant until dasha.
- Open points: he does not say whether 6th/8th is counted from the planet's house or from the house; example is planet in 11 versus house 4 = 8th from 4. Decide direction with the engine owner. Also he gives no weight table or strength measure. Do not add precedence versus lordship rules; list as a separate rule.


Status: practitioner claim, not a cited classical rule. Cross-check against classical sources before use; no precedence vs other rules is implied.

Counting clarification: the expression above is 1-based inclusive counting from house H to the planet's placement P. For P=11 and H=4 it returns 8. This fixes the draft expression's 0-index wraparound only; it does not resolve the practitioner's claimed rule or validate any predicted harm.
