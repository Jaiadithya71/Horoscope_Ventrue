# Fixed-link reel chooser

The bio entry point is `/reels`. The homepage and existing application remain unchanged. Do not edit the Instagram bio as part of code deployment.

## Flow

- Tamil-first; English toggle shares the app's existing language preference.
- Search filters the local catalog only. No search terms are sent to analytics.
- A topic choice opens `/from/<stable-slug>`, internally rewritten to the existing chart application. Unknown uses `/from/unknown`; skip uses `/`.
- These paths are visitor-reported attribution. They do not prove the selected reel caused a visit. Repeated loads, forgotten choices, shared links and skips limit inference.
- No additional visitor-level store or custom event is introduced. Vercel Web Analytics records page visits on the allowed paths. In the dashboard, distinguish page views from visitors. Do not describe either as exact Instagram link taps, chart completions or conversions.

## Adding another reel

After publication is confirmed, add its recognizable Tamil and English title plus a new permanent slug to `app/reels-catalog.js`. The list and analytics path allowlist use that single catalog. Never reuse an existing slug. The initial catalog uses previously verified published topics; the unknown option covers omitted or unremembered reels. A catalog entry is not a claim that a post remains public forever.

## Privacy

`app/analytics.js` permits only known page paths, catalog topic paths and legacy `/r/` campaign paths. Unknown paths collapse to `/other`. Query strings and fragments are stripped; malformed URLs are dropped. The chooser asks for no birth details. Existing chart privacy notices and calculation endpoints are unchanged.

## Local verification

`npx playwright test app/tests/reels.spec.js` tests both phone and desktop, all catalog links, skip, unknown, keyboard access, no-JavaScript fallback, 320px layout and the analytics sanitizer. Analytics requests are blocked in these tests. No production verification page views are generated.

The legacy suite at baseline `700efdc` has 10 failures across phone and desktop: five assertions per viewport involving language/weekly-header content, old chart counts/expectations, and 320px chart overflow. The same 10 failures reproduced after this change; no new regression was found. Keep those existing issues separate from the chooser's passing tests.
