# Astro IG reel render pipeline (astro_guidance_108)

Zero-cost local render: AI images (`tools image create`) + Tamil voiceover (edge-tts
`ta-IN-PallaviNeural`) + ffmpeg Ken Burns assembly + PIL text overlays. Python + ffmpeg only.

## Reels built with this

| Reel | File | Duration | Status |
| --- | --- | --- | --- |
| Monday single-point captioned v1 | astro-monday-captioned-v1.mp4 | 22.8s | Superseded by v2 (painterly look); kept for reference |
| Monday single-point captioned v2 (photoreal, benchmark-mimic) | astro-monday-captioned-v2.mp4 | 22.8s | Preview for user review 2026-10-23; NOT posted |

## v1 spec (2026-10-23, user's approved test idea)

His ask (WhatsApp 2026-10-23 14:18): "Let's remove the current post, and re-upload it with
the idea and see if it works" - the idea being Instinct's recommendation after the v6
retention diagnosis: **20-30 seconds, one specific point, readable Tamil captions throughout**.
v6 (89s, all 7 weekdays, voiceover-only after hook) got 195 views / ~10s avg watch; the
single-point captioned cut is the controlled next test.

- Theme: weekday-of-birth traits, ONE day per reel. v1 = Monday (திங்கள் / Moon). Sets up a
  7-part series; CTA asks viewers to comment their day.
- 6 scenes, one spoken sentence each, every sentence burned in as a large Tamil caption
  (NotoSansTamil-Bold, width-fitted to <=980px, white + black shadow; CTA line in gold).
- Hook on first frame only (red line 1, white line 2) - approved v6 style.
- 6 unique AI images, no repeats (his standing ask). Style string: "South Indian Tamil
  devotional digital painting style, warm golden cinematic lighting, rich colors, detailed,
  no text, no words, no letters, vertical composition", 9:16.
- Voice: edge-tts ta-IN-PallaviNeural, rate +6%. Segments timed to scene lengths.
- Music bed: sine 110/165/220 Hz drone at volume 0.30 under voice (same as v6).

## Tamil voiceover script (own wording, derived from engine/content_studio.py weekday
## points; content studio labels weekday-trait chains "derived" - no classical source
## gives weekday-of-birth character rules directly)

1. hook: திங்கட்கிழமை பிறந்த பெண்ணின் ரகசியம்
2. mon1: திங்கட்கிழமை பிறந்த பெண், சந்திரனின் மென்மையைச் சுமப்பாள்.
3. mon2: இனிமையான பேச்சு, அழகிய கண்கள், அமைதியான மனம்.
4. mon3: வீட்டில் அன்பைப் பரப்பும் பெண் இவள்.
5. mon4: மதிய வெளிச்சம் போல், இவள் இருப்பிடத்தைக் குளிர்விப்பாள்.
6. cta:  உங்கள் வீட்டுப் பெண் எந்தக் கிழமையில் பிறந்தாள்? கமென்டில் சொல்லுங்கள்.

## WATERMARK FIX (defect from v6, evidence docs/insights/2026-10-23-astro-ig-v6-reel/)

v6 burned "@astro_guidance_108" with NotoSansTamil-Bold.ttf, which has NO Latin glyphs -
it rendered as tofu boxes on every frame of the posted reel. Fix in render_reel.py:
watermark uses NotoSans-Bold.ttf (Latin). Verified visually on all v1 frames.

## Re-render

1. `python3 voiceover_tts.py` (needs `pip install edge-tts`) -> /tmp/voice2/*.mp3
2. Generate the 6 scene images into /downloads (style string above; subjects: mother+baby
   hook, girl under full moon, moon over temple tank, girl close portrait, moonlit home
   courtyard, girl praying before lamp).
3. `python3 render_reel.py` -> /downloads/astro-monday-captioned-v1.mp4

Scene image files expected: m_hook.png m_girl.png m_moon.png m_face.png m_home.png m_close.png
