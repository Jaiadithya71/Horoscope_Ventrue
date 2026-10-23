import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W,H = 1080,1920
FD='/usr/share/fonts/truetype/noto/'
RED=(238,60,60,255); WHITE=(250,249,252,255); GOLD=(255,214,120,255); SH=(0,0,0,220)
GAP=0.25

def dur(p):
    return float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())

def wrap_tamil(text, font, d, maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def draw_center(d, lines, font, y, fill, shadow=True, spacing=1.35):
    asc,desc=font.getmetrics(); lh=int((asc+desc)*spacing)
    for ln in lines:
        w=d.textlength(ln,font=font); x=(W-w)/2
        if shadow:
            for dx,dy in ((0,4),(4,0),(-4,0),(0,-4),(3,3),(-3,3),(3,-3),(-3,-3)):
                d.text((x+dx,y+dy),ln,font=font,fill=SH)
        d.text((x,y),ln,font=font,fill=fill)
        y+=lh
    return y

D='/downloads/'; V='/tmp/voice2/'
# scene list: (image, voice segment, caption lines or None, style)
scenes = [
 ('p_hook.png', 'hook', 'HOOK'),
 ('p_moon.png', 'mon1', 'திங்கட்கிழமை பிறந்த பெண்,\nசந்திரனின் மென்மையைச் சுமப்பாள்.'),
 ('p_face.png', 'mon2', 'இனிமையான பேச்சு, அழகிய கண்கள்,\nஅமைதியான மனம்.'),
 ('p_home.png', 'mon3', 'வீட்டில் அன்பைப் பரப்பும்\nபெண் இவள்.'),
 ('p_court.png', 'mon4', 'மதிய வெளிச்சம் போல், இவள்\nஇருப்பிடத்தைக் குளிர்விப்பாள்.'),
 ('p_pray.png','cta',  'CTA'),
]
tmp='/tmp/reelp'; os.makedirs(tmp,exist_ok=True)

# --- caption overlays (one transparent PNG per scene) ---
def fit_lines(text, font_path, size, maxw):
    f=ImageFont.truetype(font_path,size)
    im=Image.new('RGBA',(10,10)); d=ImageDraw.Draw(im)
    while size>44:
        f=ImageFont.truetype(font_path,size)
        lines=wrap_tamil(text,f,d,maxw)
        if all(d.textlength(ln,font=f)<=maxw for ln in lines) and len(lines)<=2:
            return f,lines
        size-=6
    return f,wrap_tamil(text,f,d,maxw)

caps=[]
for i,(img,seg,cap) in enumerate(scenes):
    p=f'{tmp}/cap{i}.png'
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if cap=='HOOK':
        f_h=ImageFont.truetype(FD+'NotoSansTamil-Bold.ttf',84)
        draw_center(d,['திங்கட்கிழமை பிறந்த'],f_h,820,RED)
        draw_center(d,['பெண்ணின் ரகசியம்'],f_h,820+int(84*1.9),WHITE)
    elif cap=='CTA':
        f_c=ImageFont.truetype(FD+'NotoSansTamil-Bold.ttf',62)
        draw_center(d,['உங்கள் வீட்டுப் பெண்'],f_c,1300,WHITE)
        draw_center(d,['எந்தக் கிழமையில் பிறந்தாள்?'],f_c,1300+int(62*1.6),WHITE)
        draw_center(d,['கமென்டில் சொல்லுங்கள்'],f_c,1300+int(62*3.2),GOLD)
    else:
        flat=cap.replace('\n',' ')
        f_c,lines=fit_lines(flat,FD+'NotoSansTamil-Bold.ttf',72,980)
        y0=1420 if len(lines)==2 else 1480
        draw_center(d,lines,f_c,y0,WHITE)
    im.save(p); caps.append(p)

# --- watermark overlay: FIXED font (Latin-capable NotoSans-Bold) ---
wm=f'{tmp}/wm.png'
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
f_wm=ImageFont.truetype(FD+'NotoSans-Bold.ttf',38)
t='@astro_guidance_108'
w=d.textlength(t,font=f_wm); x=(W-w)/2
d.text((x+2,1842),t,font=f_wm,fill=(0,0,0,120))
d.text((x,1840),t,font=f_wm,fill=(255,255,255,130))
im.save(wm)

# --- voice track: concat with gaps, per-scene start times ---
durs=[dur(V+s+'.mp3')+GAP for _,s,_ in scenes]
starts=[]; t0=0
for dd in durs: starts.append(t0); t0+=dd
total=sum(durs)
print('total',round(total,2),'scenes',len(scenes))
# build voice wav with silence gaps
segs=[V+s+'.mp3' for _,s,_ in scenes]
vin=''.join(f'-i {p} ' for p in segs)
n=len(segs)
fc_a=''.join(f'[{i}:a]aresample=44100[a{i}];' for i in range(n))
fc_a+=''.join(f'[a{i}]' for i in range(n))+f'concat=n={n}:v=0:a=1[va]'
subprocess.run(f'ffmpeg -y -v error {vin}-filter_complex "{fc_a}" -map "[va]" /tmp/reelp/voice_raw.wav',shell=True,check=True)
# pad gaps: easier - adelay each segment and amix
fc_b=''
for i,(p,st) in enumerate(zip(segs,starts)):
    ms=int(st*1000)
    fc_b+=f'[{i}:a]aresample=44100,adelay={ms}|{ms}[d{i}];'
fc_b+=''.join(f'[d{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0,atrim=0:{total:.3f}[va]'
subprocess.run(f'ffmpeg -y -v error {vin}-filter_complex "{fc_b}" -map "[va]" /tmp/reelp/voice.wav',shell=True,check=True)

# --- video assembly ---
inputs=[]
for i,(img,_,_) in enumerate(scenes):
    inputs+=['-loop','1','-t',f"{durs[i]:.3f}",'-i',D+img]
n=len(scenes)
inputs+=['-loop','1','-t',f'{total:.3f}','-i',wm]          # idx n
for i in range(n):
    inputs+=['-loop','1','-t',f'{total:.3f}','-i',caps[i]] # idx n+1+i
fc=[]
segsv=[]
for i in range(n):
    dd=durs[i]
    xexpr=f"'(in_w-out_w)*t/{dd:.3f}'" if i%2==0 else f"'(in_w-out_w)*(1-t/{dd:.3f})'"
    fc.append(f"[{i}:v]scale=1404:2496,crop=1080:1920:x={xexpr}:y=220,eq=brightness=-0.05:saturation=1.1,fps=24,format=yuv420p[v{i}]")
    segsv.append(f"[v{i}]")
fc.append(''.join(segsv)+f"concat=n={n}:v=1:a=0[cc]")
fc.append(f"[cc][{n}:v]overlay=0:0[cw]")
prev='cw'
for i in range(n):
    st=starts[i]; en=starts[i]+durs[i]
    out=f"co{i}"
    fc.append(f"[{prev}][{n+1+i}:v]overlay=0:0:enable='gte(t,{st:.3f})*lt(t,{en:.3f})'[{out}]")
    prev=out
fc.append(f"[{prev}]format=yuv420p[vv]")
cmd=['ffmpeg','-y']+inputs+[
 '-f','lavfi','-i',f"sine=frequency=110:duration={total:.3f}",
 '-f','lavfi','-i',f"sine=frequency=165:duration={total:.3f}",
 '-f','lavfi','-i',f"sine=frequency=220:duration={total:.3f}",
 '-filter_complex',';'.join(fc)+
 f";[{n+1+n}:a]volume=0.5[a1];[{n+2+n}:a]volume=0.3[a2];[{n+3+n}:a]volume=0.18[a3];[a1][a2][a3]amix=inputs=3:normalize=0,afade=t=in:st=0:d=1.2,afade=t=out:st={total-1.5:.3f}:d=1.5[aud]",
 '-map','[vv]','-map','[aud]','-t',f'{total:.3f}','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','/tmp/reelp/base.mp4']
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0:
    print(r.stderr[-2000:]); sys.exit(1)
print('OK base')
# mux voice over bed
r=subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/reelp/base.mp4','-i','/tmp/reelp/voice.wav',
 '-filter_complex','[0:a]volume=0.30[bed];[bed][1:a]amix=inputs=2:normalize=0,afade=t=out:st=%.3f:d=1.0[a]'%(total-1.2),
 '-map','0:v','-map','[a]','-t',f'{total:.3f}','-c:v','copy','-c:a','aac','-b:a','160k','/downloads/astro-monday-captioned-v2.mp4'],capture_output=True,text=True)
if r.returncode!=0:
    print(r.stderr[-1500:]); sys.exit(1)
print('OK final', total)
