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

## Independent software-date check

The Astro-Vision/Clickastro Saturn sample report, original PDF pp. 3-5 inspected as images, explicitly prints a 365.25-day Vimshottari year. It publishes the birth instant, Chitra Paksha Moon longitude 149°27'59", and complete major-end dates through Mercury. `python3 -m engine.calendar_benchmark` uses that published longitude, not a secretly fitted birth time, to reproduce all **seven** complete local dates with longitude balance and fixed 365.25-day years. The return-interpolation profile matches the first three dates but differs by a day for the later 2032/2048/2067/2084 boundaries. The report's final Ketu endpoint is not a complete seven-year term and is excluded transparently.

This checks a concrete third-party **software convention**, not the correct interpretation of every classic, Balaji's settings, exact boundary times, or life events. The report publishes only dates. It cannot certify an hour-level algorithm. The source supports an optional software-comparison reference; the canonical book-sourced solar-return profile is not silently changed to match it.

Source: https://astrology.mathrubhumi.com/downloads/samples-pdf/saturnrep_eng.pdf

## Sanskrit divisor corroboration

A direct download of the full SanskritDocuments ITRANS source reaches XIX.3 and gives `natAptA` and `natena`, matching the nata form in the original page image. The readable-page fetch had cut off earlier; this follow-up recovers the relevant verse. With the fetched Katapayadi letter table (na = 0, dental ta = 6, reversed place order), nata corresponds to 60. The repeated English translation and Kapoor's explicit fixed-divisor discussion independently support that reading. This is a corroborated numeric reading, not specialist manuscript criticism or proof that the fixed-60 and normalized-total-duration methods are equivalent.

Sources inspected:
- Full Sanskrit transcription download: https://sanskritdocuments.org/doc_z_misc_sociology_astrology/phaladIpika.itx
- Katapayadi letter table and reversal rule: https://en.wikipedia.org/wiki/Katapayadi_system
- Independent university teaching text explaining the letter-table method: https://spmvv.ac.in/ddefiles/ugcproposals/2025/05/MAMUD1_2_Musical_Concepts_I.pdf

Conclusion at this stage: the fixed 60 is not merely an OCR mistake. Normalized traversal is separately supported by BPHS and commentary; longitude fraction plus 365.25 days can be checked against published software dates. Choose and label a profile rather than pretend these independent conventions collapse into one universally certain timetable.

## Further convention arbitration, not a false resolution

P.V.R. Narasimha Rao's2014 article [Re-defining Tajaka Varshaphal Charts](https://vedicastrologer.org/articles/pp_tajaka.pdf), PDF1-2 directly image-inspected, identifies a dated software disagreement explained by mean tropical365.242 versus sidereal365.256 year settings. The original [K.N. Rao2010 Chara Dasha article](http://www.journalofastrology.com/article.php?article_id=317), fetched live, reports August17 versus18 endpoints. This is a **Chara Dasha** example, not a Vimshottari validation. It establishes that a one-day discrepancy can reflect a chosen year profile; it does not determine Phaladeepika's fractional-return map or Balaji's settings. The modern article's proposal for tropical annual-return charts is likewise not silently substituted for this engine's named Lahiri calendar.

[Shyamasundaradasa's year-length discussion](https://shyamasundaradasa.com/jyotish/resources/articles/how_long_year/how_long_year_5.html) and [Jyotishvidya's reproduction](https://jyotishvidya.com/dasa.htm), both fetched, argue for solar reckoning and distinguish lunar tithi from fixed civil days. Their arguments do not uniquely resolve interpolation between unequal consecutive solar-return years. Jyotishvidya repeats substantial portions of the same discussion, so it is not counted as independent confirmation. Their claims of predictive superiority are not verified event evidence. No new source examined here resolves the outstanding fractional-return convention; the explicit profiles remain necessary.

The calendar benchmark now prints both computed UTC estimates and their hour spread alongside the published date-only boundaries. This quantifies model convention drift without pretending that the vendor supplied exact reference times. No boundary-time accuracy metric is calculated from date-only evidence. Existing7/7 fixed-year and3/7 return-interpolation local-date agreement remains unchanged.

## Another dated worked example fails its internal consistency check

The fetched secondary [Saravali Dasa Balance page](https://saravali.github.io/astrology/dasa_balance.html) publishes both entry/exit times and a Moon longitude for a1935 birth, with two exact1944 endpoints. Its time fraction0.5463158976 is correct from its own inputs; longitude fraction0.54625 is also correct. However the time method has a smaller remaining fraction and should finish earlier under the same increasing calendar, whereas the printed endpoint is later. Their endpoint times imply different fixed year lengths365.2467134 versus365.1755420 days. Under365.25 the endpoints disagree by about0.716 and16.217 hours. `dated_example_audit.py` checks this without fitting a year or altering our calendar. The source does not state a sufficiently precise alternate procedure to explain the reversal; it cannot arbitrate the book convention. Modern recomputation of its birth longitude/traversal also differs from its rounded historic inputs, which is separate from the internal contradiction. No event-prediction claim is evaluated.

## Author-documented angular-time calendar, separately implemented

The software author's [official feature list](https://www.vedicastrologer.org/jh/features.htm), fetched directly, specifies solar years with the Sun's angle as the measure of time. The [7.65 change log](https://www.vedicastrologer.org/jh/update_7.65.htm) explicitly distinguishes true sidereal/tropical angular years from mean sidereal/tropical day-count years. The [7.5 change log](https://vedicastrologer.org/jh/update_7.5.htm) reports360-degree-year subperiod fixes. This is stronger evidence for a modern fractional convention than third-party notes. It supports a separate `sidereal_solar_angular_progress` option: solve the Sun's360*fraction angular progress within each natal-return revolution. Integer return roots agree with the elapsed-UTC-interpolation profile but fractional roots differ materially. Default interpolation remains unchanged, and neither is called the unique classic instruction or Balaji's setting. No software binary/default configuration or exact worked JHora endpoint was verified; this is not a byte-for-byte replica. The same published fixed365.25 date-only fixture is compared without fitting; angular/date disagreements remain exposed along with computed hours of spread, never a precision claim.

## Modern book does not give an interchangeable calendar oracle

PVR Narasimha Rao's [Vedic Astrology: An Integrated Approach](https://vedicastrologer.org/articles/vedic_astro_textbook.pdf), original PDF24 and222-224/printed12 and210-212 directly image-inspected, is stronger primary evidence for the Sun-angle calendar definition (360degree year,30degree month,1degree day). But PDF223 expressly says this book's nakshatra-dasha calculations instead use savana360-day years, not as a recommendation. These explicit scopes cannot be merged. Example50 has correctly calculated257/800 remaining fraction and2.24875 Mars years; its published2000-April28 05:50 UTC-4 birth plus360-day years produces2002-July16 19:02, not its printed approximateJuly15 19:00. `modern_book_date_audit.py` exposes that24.0333-hour mismatch without changing the birth, fitting a year, or treating an approximate endpoint/rounded Moon as exact truth. Solar interpolation and angular comparisons are separately reported. This source supports named calendar choices, not arbitration to one universal classic or Balaji setting. No book PDF is redistributed.

## Numerical root cross-check, not empirical or exact-software validation

The separate `swe.solcross_ut` library routine agrees with our angular bisection to under.1second across six synthetic fractional offsets including negative years and80years. Both share the astronomical model; this checks solver implementation only, not independent ephemeris accuracy. The pinned third-party [PyJHora drik helpers](https://github.com/naturalstupid/PyJHora/blob/48e57d29b47a3143519910a24866758116467485/src/jhora/panchanga/drik.py), read from a checkout at48e57d29, corroborate separate true angular versus mean fixed-day profiles conceptually. Its stored Example50 tests check balance units rather than a dated true-angular endpoint. No source implementation is copied and no claim of exact PyJHora/JHora endpoint/default replication is made. Classic uniqueness, Balaji settings and actual event validation remain open.

## Explicit fixed365.25 comparison in hierarchy output

The previously date-benchmarked vendor365.25 profile can now be requested for full hierarchy estimates as `fixed_365_25_day_software_comparison`, with the original vendor source/pages on its calendar record rather than misattributing fixed day-count to Phaladeepika XIX.4. No solar-root tolerance is claimed for it, default remains elapsed-return interpolation, and birth-balance methods stay separately selected/labeled. This makes practical software comparison available without silently choosing a universal calendar or unlocking outcome timing. The synthetic published birth/longitude fixture's first end reproduces1997-April2; only date-level vendor truth is available.

Explicit longitude-balance selection now keeps the unrounded model fraction, separating7-decimal display output. Previously its evidence candidate borrowed display-rounded `moon_periods` balance, creating tiny avoidable differences from the implicit identical profile. A regression checks default and explicit longitude-selected hierarchy consistency without changing source conventions or pretending this fixes the larger disagreements.

## Single convention matrix, no majority oracle

`engine.calendar_comparison` reports all3 calendar x3 balance combinations together, preserving each valid hierarchy, provenance and convention name, plus invalid/out-of-horizon reasons. Overfull fixed60 balances are not clipped or silently replaced. Distinct active-lord paths and agreement are visible, but agreement does not establish true timing, select a winner or unlock outcomes. This comparison uses only supplied birth/query data; synthetic tests and CLI examples contain no owner birth data.

Comparison regressions explicitly check a slow-sector near-entry birth where fixed60 balance exceeds the full term: all3 fixed60 combinations remain invalid while the other6 compute. Naive query clocks are rejected before any result instead of being silently localized by datetime conversion.

## A newly verified mean-Sun dated example has a different system and two constants

Sripati VII.18-20 [original scan](https://archive.org/details/dli.ernet.203510), PDF175-178 image-checked, explicitly uses Mean Sun revolutions, not modern apparent true Sun. Its terrestrial-day/year ratio is1577917828/4320000. Summary PDF207-208, also image-checked, uses approximate365.256374-day-year arithmetic for1853-Apr30 05:35local plus49.6847years and gives1903-Jan6 21:15. Earlier yuga ratio givesJan7 00:06:18; summary's own251.6531day addition givesJan6 21:15:27.84. `engine.historical_mean_year_audit` preserves the difference, local5h20mEast of Greenwich and chronology. This longevity-derived dasha system is not Vimshottari, so its mean calendar cannot silently arbitrate XIX.4 or Balaji settings. A dated example found is not automatically an exact reference.

## Convention uncertainty changes applicable evidence at real numerical boundaries

`engine.convention_condition_report` connects all nine profiles to checked scoped main/subperiod conditions without choosing one. The synthetic fixture at one second after the fixed365.25/longitude first major endpoint routes one profile to Jupiter/Jupiter/Jupiter and others to Rahu/Mars/Moon or Rahu/Mars/Venus. Regression verifies separate pair evidence and no final outcome. Calendar agreement in another sample is not permission to assume the choice never matters. Period offsets now retain full numerical precision before calendar mapping, with9decimal display fields separately labeled.

Broad half-open regression sweeps6synthetic longitudes and1200offsets each, checks4203unique nested boundaries, and excludes10expected final-horizon ends. These counts test numerical boundary consistency only, not independent astronomical or event accuracy. No observed client predictions form this suite.

Independent JhaSudha BPHS edition: actualPDF310/printed278 chapter46.14 useselapsedBhayaata/totalBhabhoga timeslordyears. WorkedRohini25;34/56;40×10 gives767/170 expired and933/170remainingyears. Exact12/30/60/60 arithmetic givesexpired4y6m4d14g7p+1/17p; printed7p istruncated, and itscomplementremaining53p sumsbackto10. The futureSun table printsbirth4sign25°45′55″ andlater10sign21°31′48″. Addingprintedremainingyears×360 tobirthSun reproduces321.53degrees exactly; exactfractiontarget differs by-1/17arcsecond. `jha_dasha_balance_audit` exposes this independent normalizedbalance andnamedsolar-targetarithmetic hypothesis. Samvat/Sunlabels do not supplyfullcivil timestamps, calendarconversion or ephemerismodel, so noexactUTCendpoint/universalcalendarwinner follows. DefaultappCLI/schema andselectedcalendarnull remainunchanged. Source https://archive.org/download/bmmv_brihat-parashar-hora-shastra-of-parashar-muni-with-sudha-commentary-by-pt.-dev-c/Brihat%20Parashar%20Hora%20Shastra%20of%20Parashar%20Muni%20with%20Sudha%20Commentary%20by%20Pt.%20Dev%20Chandra%20Jha%20Kashi%20Sanskrit%20Series%20No.%20220%20-%20Chaukhamba.pdf . No copyrightedPDF/transcriptionredistribution is implied.

Jha input-profile distinction: actualPDF53/printed21 chapter4 Mooncommentary explicitly constructslongitude=(elapsedcompletestars+Bhayaata/Bhabhoga)×40/3. ItsAnuradha2755/3434pala,16elapsedstars example yieldsapproximately224°1′49″. `jha_traversal_moon` implements a separatelysuppliedlinearizedMoon profile and exactprintedsecondaudit. Timefraction/sectorlongitudefractionagreebyconstruction, not by universalidentity for moderntrueMoonmotion. The samepagewarns dailytrue-speedinterpolation iscoarseforMoon. This supplies usefulsourcecontext for46.14 but nohistoricalPanchanga, ayanamsa, sectorinstant oruniqueGregoriancalendar. Boundedsearch of46.14/52.1-2tablecontext foundnoexplicitcivilmapping; gaps remainunknown. Tonightappschema/defaults unchanged.

## Independent Pathak angular-target commentary

Hari Shankar Pathak's Hindi Phaladeepika commentary, actual PDF222-223 /
printed204-205, XIX.3-4, inspected as original images, gives a1994-June16
10:10 worked birth and normalized remaining Venus balance950/167 years.
It explicitly tells the reader to add remaining year units to birth Samvat
and Sun coordinates, then end when the Sun reaches the target sign/degrees.
This supports a named angular-target convention, stronger than inferring
fractional mapping from an annual-return definition. It does not establish a
unique critical-edition interpretation or Balaji's settings.

The worked addition itself has a270-degree error: printed birthSun5sign1°2′31″
plus printed5y8m7d54g15p gives sign1,8°56′46″, not printed sign10,8°56′46″.
The printed balance is15/167 pala below exact normalization. The scan's
birth place/timezone and complete civil endpoint are not established here.
`pathak_solar_target_audit` preserves both discrepancies with no guessed
sign correction, calendar conversion or default change. The source supplies
commentary-convention evidence, not a reliable exact civil benchmark.
Source: https://archive.org/details/phala-dipika-of-shri-mantreshwar-hindi-commentary-by-dr.-hari-shankar-patak-chau

Pathak title/copyright actualPDF7-8 confirms commentator Dr. Hari Shankar
Pathak, Chaukhamba Surabharati series349, reprint2007 and publisher all rights
reserved. The digitizer's CC0 watermark does not clear those edition rights.
The worked passage explicitly identifies endpoint sign10 as Aquarius, so it
uses that zero-based sign index there; no alternate input-sign explanation
was found in that passage. This preserves an arithmetic discrepancy rather
than asserting a corrected misprint. `calendar_comparison` now adds the
independent commentary audit as evidence only, retaining all nine choices
and no selected profile. Birth-input defaults and numeric calendars unchanged.
