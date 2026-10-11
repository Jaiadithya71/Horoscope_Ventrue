# Tamil-first jathagam preview
12 October 2026. Owner-approved build; deployment verification tracked separately.

A bilingual Tamil birth sheet sits beside the existing life reading. No account,
new database, analytics, automatic client collection, or copied interpretations.

## Included
- Tamil solar month/day and sixty-year name under an explicit local-sunset Lahiri
  ingress profile, not a Vakya calendar or guaranteed Chennai-reference calendar.
- Birth-instant tithi, paksha, star/pada, yoga and karana.
- Sea-level apparent-upper-limb sunrise/sunset, with standard atmospheric model;
  previous sunrise for pre-sunrise udayadi, and no invented polar event.
- Udayadi nazhikai/vinadi (1 nazhikai = 24 minutes; 1 vinadi = 24 seconds).
- Signed-longitude local apparent sidereal clock, not planetary hora.
- Date-specific Lahiri ayanamsa, full-precision positions, South Indian fixed-sign
  rasi/navamsa chart. Navamsa uses the existing source-checked geometry.
- Explicit mean/true Rahu choice. Mean remains the existing default. Ketu on the
  sheet is the point 180 degrees opposite Rahu, not an independently calculated body.
- Tamil maha/bhukti date lists for all four existing Vimshottari alternatives.
  Dates display in the birth timezone. From is inclusive, To is exclusive.
- Place lookup suggests an editable IANA timezone. Historical civil offsets are
  still resolved for the birth date, not copied from the current city offset.
- Node/view options persist only when the user explicitly saves a client locally.
  Older backups remain valid and default to their prior mean-node behavior.
- Embedded Noto Tamil font data in CSS (SIL OFL 1.1), no third-party font requests.

## Preserved limits
No winner selected for year length or balance method. No source priority changed,
no competitor dasha formula claimed, and no predictive accuracy claim. This is a
bilingual sheet, not a complete Tamil translation of all English life readings.
Historical timezone borders may differ from current polygon lookup: verify old
birth locations and boundary cases manually. A zone hint is not proof of historical
jurisdiction. High-latitude sunset absence means Tamil date is unavailable.
Modern solar date and sunrise profiles may differ from a family's chosen almanac.
Terrain, elevation and observed atmospheric conditions are not inferred.

## Dependencies
`tzfpy==2.1.1`, MIT, with bundled simplified coordinate-to-timezone boundaries,
and `tzdata==2026.5`. Timezone suggestions can differ near borders. Confirm the
Vercel Python artifact size and native wheel support before deployment. Existing
pyswisseph/AGPL terms still apply. Font attribution/license in app/fonts/LICENSE.txt. No separate font request is required.

## Sources
- https://ennkanitham.com/methodology/panchangam/ (birth panchang angles, local
  sunset solar-date profile and 1987 cycle anchor; updated 8 Sep 2026)
- https://www.tamilcalendar.app/methodology (Chennai-reference alternative,
  kept distinct rather than silently averaged with the local profile)
- https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?geoname-id=1264527
  (Chennai 11 Oct 2026 rise05:59/set17:52; modern check within2min)
- https://omtamilcalendar.com/tamil_new_year_names/index.html
- http://tamil-panchangam.blogspot.com/2009/11/tamil-years-60-year-cycle.html
  (independent year sequence, published21 Nov2009)
- https://www.astro.com/swisseph/swephprg.htm (rise_trans/sidtime/sidereal model)
- https://github.com/ringsaturn/tzfpy/blob/main/README.md
- https://pypi.org/project/tzfpy/
- https://github.com/notofonts/tamil
- Existing Phaladeepika1937 PDF61-62 geometry and existing timing alternatives;
  their underlying source audits are preserved unchanged.

Tests cover independent Chennai solar references, London2000 offset, pre-sunrise,
polar absence, civil/UTC date separation, Tamil year boundary, explicit true node,
invalid options, option persistence, place-zone suggestion and phone widths320/390.
Passing tests verify arithmetic and behavior, not predictive truth or all almanacs.
