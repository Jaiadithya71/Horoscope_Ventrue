# astro_guidance_108 v6 weekday reel — native insights + reel inspection (2026-10-23)

Read-only inspection by Instinct, signed in as astro_guidance_108 on instagram.com web, ~14:13 IST, the day after posting (v6 weekday reel posted 2026-10-22 11:47 via Metricool). No account changes, no posts.

## Native insights (IG web, own account)

Source: https://www.instagram.com/insights/media/4013359489734229174/ (see native-insights-panel.png)

| Metric | Value | Note |
| --- | --- | --- |
| Views | 195 | Meta tooltip on screen: "The number of times your reel was played or displayed on screen." |
| Viewers | 172 | Tooltip: "Meta Accounts that have viewed your reel at least once. This metric is estimated and in development." |
| Followers / Non-followers | 0% / 100% | All distribution was cold recommendation traffic |
| Interactions | 4 | Likes 3, Comments 0, Saves 0, Shares 1 |
| Accounts engaged | 7 | |
| Profile activity / Follows | 2 / 2 | Live profile: 1 post, 1 follower, 0 following |

- Views minus Viewers = 23 repeat plays/displays; Meta does not split replays vs re-displays.
- Native Saves reads **0**; Metricool's same-morning snapshot read 1 save. Native is the source of truth.
- Video duration measured from the player: **88.67s** (not 86s).
- IG desktop web exposes **no average watch time and no retention curve** for this reel; that surface is mobile-app only. Metricool's 10s average watch time remains the only retention datapoint. The drop-off shape (early cliff vs steady fade) could not be read from web. Meta Business Suite not used (standing restriction).
- Retention curve is visible in the IG mobile app: reel → View insights → retention.

## Reel content inspection (frames at 0.2s / 5s / 15s / 40s / 48s)

- Hook frame (see hook-frame-0.2s.png) carries the Tamil hook text as approved: "உங்கள் வீட்டுப் பெண் பிறந்த கிழமை சொல்லும் ரகசியம்".
- Every frame after the hook is a clean AI scene with **zero on-screen text**; all information after ~2s is voiceover-only. Muted viewers get nothing past the hook frame.
- Caption repeats all 7 weekday traits + comment CTA; hashtags #astrotamil #tamiljothidam #tamilreels #tamilastrology.

## DEFECT: handle watermark renders as tofu boxes

The burned-in handle watermark at the bottom of **every frame** renders as missing-glyph boxes ("□□□□□□_□□□□□□□□_108") instead of "astro_guidance_108" — the render pipeline's watermark font does not cover the Latin glyphs. Visible in both attached screenshots. Fix the watermark font (or burn the handle in a covered font) before the next reel render.
