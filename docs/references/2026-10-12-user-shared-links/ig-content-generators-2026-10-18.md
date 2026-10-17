# IG content generators (internal studio) - provenance note (2026-10-18)

Jai's instruction (WhatsApp, 2026-10-18 00:51): "Let's build all 4 but don't show on the front for now, we are
building it to create our own content on IG". The 4 reel topics come from the reference reels in
`instagram-tamil-astro-reels-2026-10-18.md`.

Built as `/studio` (page `app/studio.html`, API `api/studio.py`, data `engine/content_studio.py`, tests
`tests/test_content_studio.py`). The route is reachable but deliberately not linked from any public page, and
the page carries `noindex,nofollow` and an "Internal" badge.

## What each of the 4 is built on

### 1. Girl-child traits by birth weekday (`weekday`)
No book in the 8-book library gives character traits by weekday of birth, for girls or anyone else. Stri
Jataka (the female-horoscopy book) has no weekday rules either. The card therefore:
- cites the weekday's ruling planet (Astrological Self-Instructor 1893, weekday names derived from planetary
  horas, PDF pp. 99-100);
- renders that planet's nature (Phaladeepika 1937, ch. II, slokas 8-14, PDF pp. 49-51) and colour/direction
  (Brihat Jataka 1905, ch. II, sloka 5, PDF p. 61) as a **derived** chain, labelled as such on the card.
The card's notice says plainly that a reel presenting weekday-birth traits as a direct classical rule would be
claiming more than the sources say. Phaladeepika ch. XI (female horoscopy) has female-specific effects for
birth in certain nakshatras (Aslesha, Jyeshta, Visakha, Chittra, Ardra, Satabhishak, Moola, Krittika, Pushya) -
a possible future, properly-cited girl-child card, not built here.

### 2. Lucky deity by nakshatra (`nakshatra`)
The library has no direct nakshatra-presiding-deity table. The card gives:
- the nakshatra's birth traits, cited: Brihat Jataka ch. XVI (PDF pp. 208-212), corroborated by Astrological
  Self-Instructor ch. IX (PDF pp. 185-187);
- the derived deity chain, labelled derived: nakshatra -> Vimshottari dasha lord (Brihat Jataka ch. VIII, PDF
  p. 139) -> that planet's presiding deity (Phaladeepika ch. II, sloka 27, PDF p. 57; alternate deva list in
  Brihat Jataka ch. II, sloka 5, PDF p. 61).
Only 9 distinct deities result, because the chain passes through the 9 dasha lords; that is the honest shape
of the derivation.

### 3. 9-graha remedies (`graha`)
The modern "one remedy per graha" list is not in the books. What is cited per graha: presiding deity
(Phaladeepika II.27, p. 57; alternate in Brihat Jataka II.5, p. 61), gem (Phaladeepika II.29, pp. 57-58),
substance/metal (Phaladeepika II.30, p. 58; Brihat Jataka II.12, p. 63 - the two books disagree and both are
shown), grain (II.28, p. 57), flavour (II.31, p. 58), colour and direction (Brihat Jataka II.5, p. 61), place
and garment (Brihat Jataka II.12, p. 63), plus the general shanti rule for badly placed planets (Phaladeepika
XXVI.49-50, PDF p. 356). This is internal content tooling; the public app's "practical guidance, not
gemstones/mantras" direction is untouched.

### 4. Per-sign traits (`sign`)
Quoted classical Moon-in-sign character lists: Brihat Jataka ch. XVII (PDF pp. 213-216), corroborated by
Astrological Self-Instructor ch. IX (PDF pp. 187-189), plus the sign's body-part in the Kalapurusha frame
(Brihat Jataka ch. I, sloka 4, PDF pp. 46-47). The chapter caveat (effects are full only when the Moon, its
sign and the sign's lord are all powerful, Brihat Jataka ch. XVII sloka 13) is on every card.

## Content-drafting features
Each card assembles a ready caption: Tamil hook (identity question, as in the reference reels), Tamil points
rendered from the cited English, a comment CTA, and hashtags following the observed reference-reel pattern.
