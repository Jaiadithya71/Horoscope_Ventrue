# Monday captioned reel TTS - see README.md for spec
import asyncio, edge_tts
SEGMENTS = [
 ("hook", "திங்கட்கிழமை பிறந்த பெண்ணின் ரகசியம்"),
 ("mon1", "திங்கட்கிழமை பிறந்த பெண், சந்திரனின் மென்மையைச் சுமப்பாள்."),
 ("mon2", "இனிமையான பேச்சு, அழகிய கண்கள், அமைதியான மனம்."),
 ("mon3", "வீட்டில் அன்பைப் பரப்பும் பெண் இவள்."),
 ("mon4", "மதிய வெளிச்சம் போல், இவள் இருப்பிடத்தைக் குளிர்விப்பாள்."),
 ("cta",  "உங்கள் வீட்டுப் பெண் எந்தக் கிழமையில் பிறந்தாள்? கமென்டில் சொல்லுங்கள்."),
]
async def gen(name, text):
    tts = edge_tts.Communicate(text, voice='ta-IN-PallaviNeural', rate='+6%')
    await tts.save(f'/tmp/voice2/{name}.mp3')
async def main():
    for n, t in SEGMENTS:
        await gen(n, t); print('saved', n)
asyncio.run(main())
