# SrirangamInfo spot checks, 11 October 2026

Three synthetic test charts were entered through the normal calculator UI at
https://srirangaminfo.com/Jathagam-tamil.php . No bulk scraping, real client
records, copied interpretation content or changed engine defaults.

Inputs: Madurai, India, UTC+05:30. Site place choice: latitude 9.919,
longitude 78.1195. Its coordinate boxes round to 9°55′ N / 78°07′ E;
our comparisons used the underlying decimal place-choice coordinates.

| Synthetic case | Site lagna | Our lagna | Site and our Moon star |
|---|---|---|---|
| A: 15 Aug 1998, 06:20 | Leo, 120.11° | Leo, 120.11644° | Krittika pada 2 |
| B: 1 Jan 2000, 14:30 | Aries, 25.21° | Aries, 25.21227° | Swati pada 4 |
| C: 15 Aug 1998, 06:19 | Cancer, 119.87° | Cancer, 119.87357° | Krittika pada 2 |

The one-minute Cancer/Leo boundary agrees. This is arithmetic agreement on
three samples, not empirical validation of predictions or an exhaustive
astronomy benchmark.

## Dasha dates differ

Dates below are local India calendar dates. The site gives day-only dates;
our conditional timelines include clock time. The labels describe our four
existing alternatives. None is selected as correct by this comparison.

| Case | Boundary | Site | Moon-time, 365.242264-day | Longitude, 365.242264-day | Moon-time, 360-day | Longitude, 360-day |
|---|---|---|---|---|---|---|
| A | Sun/Rahu ends | 4 Oct 1998 | 4 Oct 1998 | 1 Oct 1998 | 4 Oct 1998 | 1 Oct 1998 |
| A | Sun maha ends | 15 Sep 2002 | 16 Sep 2002 | 13 Sep 2002 | 26 Aug 2002 | 23 Aug 2002 |
| B | Rahu/Sun ends | 20 Mar 2000 | 19 Mar 2000 | 12 Mar 2000 | 18 Mar 2000 | 11 Mar 2000 |
| B | Rahu maha ends | 7 Oct 2002 | 6 Oct 2002 | 30 Sep 2002 | 22 Sep 2002 | 15 Sep 2002 |
| C | Sun/Rahu ends | 6 Oct 1998 | 6 Oct 1998 | 3 Oct 1998 | 5 Oct 1998 | 2 Oct 1998 |
| C | Sun maha ends | 18 Sep 2002 | 18 Sep 2002 | 15 Sep 2002 | 27 Aug 2002 | 24 Aug 2002 |

The site's dates lie closest to our Moon-time / 365.242264-day alternative,
with a residual of zero to about one calendar day in these boundaries.
That does not prove the site's formula or authorize changing our convention.
Our longitude balance alternatives differ by days; 360-day profiles can differ
by weeks over several years. Compare settings and original source conditions
before interpreting a disagreement as an engine bug.

## Comparator caveats

The landing page calls its method Thirukkanida. Actual results explicitly label
ayanamsa Lahiri. These are not mutually exclusive choices. No Vakya birth-chart
mode was observed, so this is not a Thirukkanida-versus-Vakya test.

The result displays the same '-24.23 (Lahiri)' ayanamsa for the 1998 and 2000
charts, and labels Madurai's longitude 'W' despite its form using E. A first
manual-coordinate attempt showed 0° coordinates in the result metadata even
though the chart degree agreed with the entered DMS coordinates; it was excluded
from the valid comparison and rerun using the normal place picker. Do not treat
this website as a ground-truth oracle. Its AI marriage suggestions are neither
rule evidence nor benchmark outcomes, and were not imported.

Result URL observed: https://srirangaminfo.com/Jathagam-tamil-result.php .
This page depends on session input; it is not a durable per-chart report link.
The site exposes share links containing birth data. Never use them for real
clients without explicit permission.

Our evidence: engine/natal.py and engine/timing_conditional.py, modern
Swiss Moshier/Lahiri, explicit four-timeline output; source decisions unchanged.
