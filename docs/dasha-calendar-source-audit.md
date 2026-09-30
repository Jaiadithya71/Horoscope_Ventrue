# Dasha calendar source audit

Original-scan evidence, September 30, 2026. No claim of predictive accuracy.

## Exact text-supported arithmetic

Phaladeepika XIX.2, PDF p. 229 (printed 192), gives the nine star lords and 6/10/7/18/16/19/17/7/20-year terms. XXI.2, PDF p. 258 (printed 221), gives the product of parent and child terms divided by 120, the repeating starting-lord order, and the same proportional subdivision for deeper levels. It converts remainder fractions into 12 months and then 30 days. These original page images were inspected. `engine.period_evidence.period_units` implements this as exact rational arithmetic, without interpreting its units as Gregorian months or fixed civil days.

## Initial balance is not settled by longitude alone

XIX.3, pp. 229-230, starts from remaining Moon traversal **time** in ghatikas. The checked English edition prints remaining ghatikas multiplied by the lord's years, divided by **60**. The 1950 second edition has the same English instruction on its PDF pp. 229-230, inspected as images. This is not authority to silently replace the divisor with actual star traversal duration or assume that every star takes exactly 60 ghatikas. It needs a Sanskrit/commentary cross-check or a source-supported worked example before adoption. The code preserves the printed formula as a candidate, not a selected method.

`python3 -m engine.period_evidence --birth-date 2000-01-01 --birth-time 14:30 --birth-tz Asia/Kolkata` numerically measures the Moon's entry and exit from its 13°20' Lahiri sector. It prints the literal fixed-divisor candidate, a separately sourced normalized-time candidate, and the existing equal-sector-longitude approximation. The last two are **not** attributed as exact instructions from XIX.3. The ghatika conversion (24 minutes) is page-checked in Row's *Astrological Self-Instructor*, PDF p. 99 (printed 85). Root brackets of 0.1 seconds are computational tolerances, not uncertainty bounds for the astronomical model or birth data.

For the synthetic example above, total traversal is about 66.075 ghatikas, yielding about 3.043 remaining years with the printed fixed 60 divisor, 2.763 with actual-time normalization, and 2.745 with the existing longitude approximation. No real user's birth data is used here. This difference is why no candidate silently replaces the existing hierarchy. Literal fixed-divisor results can even exceed the full lord's term near entry into a slower-traversed star; they must not automatically be treated as valid initial remainders.

## Solar year versus a civil timetable

XIX.4, p. 230 (printed 193), defines a solar year by return to the birth Sun position and says days follow by subdivision. It does not explicitly resolve the modern coordinate/ayanamsha convention or the fractional-year-to-UTC procedure when consecutive return-years differ. The 12/30 remainder arithmetic is a **unit decomposition**, not by itself proof of a 360-Gregorian-day year. `engine.solar_dates` solves integer Lahiri returns, then transparently interpolates elapsed UTC between adjacent returns. That is one named research convention, not a uniquely book-defined exact dasha timetable or verified Balaji setting.

Another book, commentary or dated worked example may resolve a choice, but must be verified and identified as a distinct source, not blended silently into this edition. Matching Balaji requires his own settings or complete worked readings. Book fidelity, model precision and independently observed prediction accuracy remain separate.

## Sources

- Original 1937 scan, visually checked XIX.2-4 and XXI.2: https://archive.org/details/in.ernet.dli.2015.92117
- 1950 second-edition scan, visually checked XIX.3-4: https://www.wisdomlib.org/uploads/ocr/essays/phaladeepika/phaladeepika-2nd-ed-1950-by-v-subrahmanya-sastri-text.pdf
- Online matching XIX.2-4 translation, not an independent resolution: https://www.siva.sh/phaladeepika/19/1-5
- Online XXI text used to find original p. 258, not authority by OCR alone: https://www.wisdomlib.org/hinduism/book/phaladeepika-by-mantreswara-text-and-translation/d/doc1621593.html
- Row source scan for time units: https://archive.org/details/Astrology_Books_by_B_Suryanarayana_Row


## Commentary and independent passage cross-check

The Kapoor *Phaladeepika* commentary reproduction, PDF pp. 175-176, inspected as rendered page images, explicitly documents the difference: Mantreswara's fixed 60 divisor versus total actual star duration. The commentator rejects treating every star duration as 60 ghatikas and also gives a longitude-based shortcut. This is evidence for **distinct supported profiles**, not license to rewrite the older edition or declare all three formulas identical.

Brihat Parasara Hora Sastra vol. II, chapter 46 verse 16, PDF p. 18 / printed p. 508, visually checked, explicitly divides elapsed Moon stay by total Moon stay and subtracts that fraction of the lord's term. The next page describes longitude as a simpler modern method. The library filename/catalog says Santhanam, but the actual vol. II preface names Gouri Shankar Kapoor as translator. The implementation cites the inspected edition accordingly.

The test suite independently checks the worked arithmetic. Kapoor's longitude example gives 14y 0m 21.6d expired and 4y 11m 8.4d remaining; the reproduction prints rounded days 22 and 8. BPHS p. 508 has arithmetic transcription problems: 58 ghatis 15 palas is **3495**, not its printed 3415; multiplied by 7 is **24465**, not printed 24435. Those printed numbers are not adopted as ground truth fixtures. Formula fidelity and printed-example arithmetic are checked separately.

`engine.solar_dates --balance-method normalized_actual_traversal_fraction` now uses the measured BPHS-supported time fraction with its own source evidence; `printed_XIX_3_fixed_60_divisor` uses the checked English formula when its balance fits within the lord's full term. Invalid overfull balances are rejected, not clipped. Omitting the option preserves the prior longitude-fraction profile. Each requested profile remains labeled and outputs the disagreement. None claims verified exact Gregorian dates.

The independent Sanskrit digital lead retrieved for cross-check was truncated before chapter XIX, so it does not establish a fresh translation of the divisor. The original Sanskrit images and repeated English translation were inspected, but no independent specialist translation has been authenticated. No dated Gregorian worked example resolving the fractional solar-year convention has yet been verified.

Additional inspected sources:
- Kapoor commentary reproduction, pp. 175-176: https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf
- BPHS source landing page: https://elibraryofyoga.com/items/13b2600f-95fd-4bb5-86b4-a18396c68993
- BPHS vol. II downloaded scan, pp. 18-19: https://elibraryofyoga.com/bitstreams/c4881ae4-af7a-4952-8194-71e42f2c7a5e/download
- Matching online BPHS 46.16 used as a search lead: https://www.siva.sh/brihat-parashara-hora-shastra/46/16
