import json,os
from PIL import Image,ImageDraw,ImageFont,ImageOps
root='/tmp/murugan-preview'
archive='/tmp/horoscope-status/docs/insights/2026-10-26-murugan-nine-tuesdays-preview/generated-illustrations'
paths=[f'{archive}/scene-{i+1:02d}.png' for i in range(9)]
paths[0]=paths[4]
json.dump(paths,open(root+'/images-final.json','w'))
captions=[['9 செவ்வாய்கள்','வெற்றிலை தீபம்','ஒரு வழிபாட்டு மரபு'],['முதலில் தூய்மை','மஞ்சள் • குங்குமம்','பூ அலங்காரம்'],['புதிதாக வாங்கிய 6 வெற்றிலைகள்','கிழிவற்றவை • கழுவித் துடைக்கவும்','கடன் / மறுபயன்பாடு வேண்டாம்'],['மஞ்சள் • குங்குமம்','மயில் தோகை போல அடுக்கவும்'],['அகல் விளக்கு • நல்லெண்ணெய் / நெய்','விளக்கு வெறும் தட்டில் உறுதியாக','பூ, இலைகள் தீபத்திலிருந்து விலகி'],['பித்தளை அல்லது செம்புத் தட்டு','வெள்ளி வேண்டாம்','இது இம்மரபின் விதி'],['செவ்வாய்: காலை 6-7','மதியம் 1-2 • இரவு 8-9','தொடர்ந்து 9 செவ்வாய்கள்'],['அமைதியுடன் வேண்டுதல்','எரியும் விளக்கைத் தனியாக','விட்டுச் செல்லாதீர்கள்'],['இந்த முறை தெரியுமா?','ஓம் முருகா','கமென்டில் சொல்லுங்கள்']]
font='/usr/share/fonts/truetype/noto/NotoSansTamilUI-Regular.ttf'
for i,(p,lines) in enumerate(zip(paths,captions)):
 im=ImageOps.fit(Image.open(p).convert('RGB'),(720,1280)); ov=Image.new('RGBA',im.size); d=ImageDraw.Draw(ov)
 f=ImageFont.truetype(font,31); sm=ImageFont.truetype(font,22)
 boxh=len(lines)*52+36;y=1000-boxh//2
 d.rounded_rectangle((28,y,692,y+boxh),radius=16,fill=(12,13,15,224))
 for n,line in enumerate(lines):
  size=31 if i else 40; ft=ImageFont.truetype(font,size)
  while d.textlength(line,font=ft)>620:
   size-=1;ft=ImageFont.truetype(font,size)
  d.text((360,y+22+n*52),line,font=ft,fill='white',anchor='mt')
 d.rounded_rectangle((30,85,340,122),radius=7,fill=(10,10,10,150));d.text((43,92),'@astro_guidance_108',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22),fill='white')
 d.text((360,1185),'செயற்கைக் காட்சிகள், மரபு விளக்கம்',font=sm,fill='white',anchor='mt',stroke_width=1,stroke_fill='black')
 Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB').save(f'{root}/scene-{i+1:02d}.jpg',quality=94)
# contact sheet
out=Image.new('RGB',(810,1440))
for i in range(9):
 im=Image.open(f'{root}/scene-{i+1:02d}.jpg');im.thumbnail((270,480));out.paste(im,(i%3*270,i//3*480))
out.save('/downloads/murugan-captioned-scenes-qc.jpg')
