import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920; FD='/usr/share/fonts/truetype/noto/'
RED=(238,60,60,255); WHITE=(250,249,252,255); GOLD=(255,214,120,255); SH=(0,0,0,220)
GAP=0.12
def dur(p):
    return float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
def wrap_tamil(text,font,d,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def draw_center(d,lines,font,y,fill,spacing=1.35):
    asc,desc=font.getmetrics(); lh=int((asc+desc)*spacing)
    for ln in lines:
        w=d.textlength(ln,font=font); x=(W-w)/2
        for dx,dy in ((0,4),(4,0),(-4,0),(0,-4),(3,3),(-3,3),(3,-3),(-3,-3)):
            d.text((x+dx,y+dy),ln,font=font,fill=SH)
        d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y
def fit_lines(text,size,maxw):
    d=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    while size>44:
        f=ImageFont.truetype(FD+'NotoSansTamil-Bold.ttf',size)
        lines=wrap_tamil(text,f,d,maxw)
        if all(d.textlength(ln,font=f)<=maxw for ln in lines) and len(lines)<=2: return f,lines
        size-=6
    return f,wrap_tamil(text,f,d,maxw)
D='/downloads/'; V='/tmp/voice3/'
scenes=[
 ('d_hook.png','hook','HOOK'),
 ('d_mon1.png','mon1','திங்கட்கிழமை பிறந்த பெண், சந்திரனின் மென்மையைச் சுமப்பாள்.'),
 ('d_mon2.png','mon2','இனிமையான பேச்சு, அழகிய கண்கள், அமைதியான மனம்.'),
 ('d_mon3.png','mon3','வீட்டில் அன்பைப் பரப்பும் பெண் இவள்.'),
 ('d_tue1.png','tue1','செவ்வாய்க்கிழமை பிறந்த பெண், இளமையான தோற்றமும் தைரியமான நடையும் கொண்டவள்.'),
 ('d_tue2.png','tue2','கோபம் இருந்தாலும் மனம் தாராளம்.'),
 ('d_tue3.png','tue3','இவள் வந்த வீட்டில் உற்சாகம் பெருகும்.'),
 ('d_wed1.png','wed1','புதன்கிழமை பிறந்த பெண், இனிமையான பேச்சும் நகைச்சுவையும் கொண்டவள்.'),
 ('d_wed2.png','wed2','சீரான மனம், பச்சை நிற விருப்பம்.'),
 ('d_wed3.png','wed3','இவள் சிரித்தால் வீடே ஒளிரும்.'),
 ('d_thu1.png','thu1','வியாழக்கிழமை பிறந்த பெண், மிகுந்த புத்திசாலி.'),
 ('d_thu2.png','thu2','சிங்கம் போன்ற குரல், செல்வம் தேடும் இயல்பு.'),
 ('d_thu3.png','thu3','இவள் யோசனை கேட்டு நடந்தால் குடும்பம் வளமாகும்.'),
 ('d_fri1.png','fri1','வெள்ளிக்கிழமை பிறந்த பெண், மிக அழகியவள்.'),
 ('d_fri2.png','fri2','அகன்ற கண்கள், கறுப்புச் சுருள் முடி.'),
 ('d_fri3.png','fri3','இசையும் கவிதையும் இவளுக்கு உடன்பிறந்தவை.'),
 ('d_fri4.png','fri4','வீட்டில் மகிழ்ச்சி பூக்கும்.'),
 ('d_sat1.png','sat1','சணிக்கிழமை பிறந்த பெண், உயரமான தோற்றமும் ஆழ்ந்த கண்களும் கொண்டவள்.'),
 ('d_sat2.png','sat2','மெதுவாக நடந்தாலும் பிடிவாதத்துடன் இலக்கை அடைவாள்.'),
 ('d_sat3.png','sat3','உழைப்பே இவளை மேலே கொண்டுச் செல்லும்.'),
 ('d_sun1.png','sun1','ஞாயிற்றுக்கிழமை பிறந்த பெண், துணிச்சலின் வடிவம்.'),
 ('d_sun2.png','sun2','சதுரமான தோற்றம், சூரியனின் தேஜஸ்.'),
 ('d_sun3.png','sun3','இவள் பிறந்த வீட்டிற்கும் புகுந்த வீட்டிற்கும் பெருமை சேர்ப்பாள்.'),
 ('d_cta1.png','cta1','எந்தக் கிழமையில் பிறந்தாலும், ஒவ்வொரு பெண்ணும் ஒரு சக்தி.'),
 ('d_cta2.png','cta2','CTA'),
]
tmp='/tmp/reeld'; os.makedirs(tmp,exist_ok=True)
caps=[]
for i,(img,seg,cap) in enumerate(scenes):
    p=f'{tmp}/cap{i}.png'
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if cap=='HOOK':
        f_h=ImageFont.truetype(FD+'NotoSansTamil-Bold.ttf',84)
        draw_center(d,['உங்கள் வீட்டுப் பெண் பிறந்த கிழமை'],f_h,820,RED)
        draw_center(d,['சொல்லும் ரகசியம்'],f_h,820+int(84*1.9),WHITE)
    elif cap=='CTA':
        f_c=ImageFont.truetype(FD+'NotoSansTamil-Bold.ttf',62)
        draw_center(d,['உங்கள் வீட்டுப் பெண்'],f_c,1300,WHITE)
        draw_center(d,['எந்தக் கிழமையில் பிறந்தாள்?'],f_c,1300+int(62*1.6),WHITE)
        draw_center(d,['கமென்டில் சொல்லுங்கள்'],f_c,1300+int(62*3.2),GOLD)
    else:
        f_c,lines=fit_lines(cap,72,980)
        y0=1420 if len(lines)==2 else 1480
        draw_center(d,lines,f_c,y0,WHITE)
    im.save(p); caps.append(p)
wm=f'{tmp}/wm.png'
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
f_wm=ImageFont.truetype(FD+'NotoSans-Bold.ttf',38)
t='@astro_guidance_108'; w=d.textlength(t,font=f_wm); x=(W-w)/2
d.text((x+2,1842),t,font=f_wm,fill=(0,0,0,120)); d.text((x,1840),t,font=f_wm,fill=(255,255,255,130))
im.save(wm)
durs=[dur(V+s+'.mp3')+GAP for _,s,_ in scenes]
starts=[]; t0=0
for dd in durs: starts.append(t0); t0+=dd
total=sum(durs); print('total',round(total,2),'scenes',len(scenes))
segs=[V+s+'.mp3' for _,s,_ in scenes]
vin=''.join(f'-i {p} ' for p in segs); n=len(segs)
fc_b=''
for i,(p,st) in enumerate(zip(segs,starts)):
    ms=int(st*1000); fc_b+=f'[{i}:a]aresample=44100,adelay={ms}|{ms}[d{i}];'
fc_b+=''.join(f'[d{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0,atrim=0:{total:.3f}[va]'
subprocess.run(f'ffmpeg -y -v error {vin}-filter_complex "{fc_b}" -map "[va]" /tmp/reeld/voice.wav',shell=True,check=True)
inputs=[]
for i,(img,_,_) in enumerate(scenes):
    inputs+=['-loop','1','-t',f"{durs[i]:.3f}",'-i',D+img]
inputs+=['-loop','1','-t',f'{total:.3f}','-i',wm]
for i in range(n):
    inputs+=['-loop','1','-t',f'{total:.3f}','-i',caps[i]]
fc=[]; segsv=[]
for i in range(n):
    dd=durs[i]
    xexpr=f"'(in_w-out_w)*t/{dd:.3f}'" if i%2==0 else f"'(in_w-out_w)*(1-t/{dd:.3f})'"
    fc.append(f"[{i}:v]scale=1404:2496,crop=1080:1920:x={xexpr}:y=220,eq=brightness=-0.05:saturation=1.1,fps=24,format=yuv420p[v{i}]")
    segsv.append(f"[v{i}]")
fc.append(''.join(segsv)+f"concat=n={n}:v=1:a=0[cc]")
fc.append(f"[cc][{n}:v]overlay=0:0[cw]")
prev='cw'
for i in range(n):
    st=starts[i]; en=starts[i]+durs[i]; out=f"co{i}"
    fc.append(f"[{prev}][{n+1+i}:v]overlay=0:0:enable='gte(t,{st:.3f})*lt(t,{en:.3f})'[{out}]")
    prev=out
fc.append(f"[{prev}]format=yuv420p[vv]")
si=2*n+1
cmd=['ffmpeg','-y','-nostdin']+inputs+[
 '-f','lavfi','-i',f"sine=frequency=110:duration={total:.3f}",
 '-f','lavfi','-i',f"sine=frequency=165:duration={total:.3f}",
 '-f','lavfi','-i',f"sine=frequency=220:duration={total:.3f}",
 '-filter_complex',';'.join(fc)+
 f";[{si}:a]volume=0.5[a1];[{si+1}:a]volume=0.3[a2];[{si+2}:a]volume=0.18[a3];[a1][a2][a3]amix=inputs=3:normalize=0,afade=t=in:st=0:d=1.2,afade=t=out:st={total-1.5:.3f}:d=1.5[aud]",
 '-map','[vv]','-map','[aud]','-t',f'{total:.3f}','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','/tmp/reeld/base.mp4']
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0:
    open('/tmp/reeld/err.txt','w').write(r.stderr); print(r.stderr[:1200]); sys.exit(1)
print('OK base')
r=subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/reeld/base.mp4','-i','/tmp/reeld/voice.wav',
 '-filter_complex','[0:a]volume=0.30[bed];[bed][1:a]amix=inputs=2:normalize=0,afade=t=out:st=%.3f:d=1.0[a]'%(total-1.2),
 '-map','0:v','-map','[a]','-t',f'{total:.3f}','-c:v','copy','-c:a','aac','-b:a','160k','/downloads/astro-7day-captioned-v3.mp4'],capture_output=True,text=True)
if r.returncode!=0: print(r.stderr[-1500:]); sys.exit(1)
print('OK final', total)
