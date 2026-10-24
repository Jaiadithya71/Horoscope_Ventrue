#!/bin/bash
set -e
D=/downloads; B=/tmp/nak_build
IMGS=($D/nak_hook.png $D/nak_s1.png $D/nak_s2.png $D/nak_s3.png $D/nak_s4.png $D/nak_hook.png)
VOIDX=(00 01 02 03 04 10)
PADS=(0.6 0.5 0.5 0.5 0.5 0.8)
N=5
declare -a DUR
for i in $(seq 0 $N); do
  f="$D/vo_${VOIDX[$i]}.wav"
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  DUR[$i]=$(python3 -c "print($vd + ${PADS[$i]})")
done
TOTAL=0; for d in "${DUR[@]}"; do TOTAL=$(python3 -c "print($TOTAL+$d)"); done
echo "scene durations: ${DUR[@]} total: $TOTAL"
for i in $(seq 0 $N); do
  frames=$(python3 -c "print(int(${DUR[$i]}*30))")
  ffmpeg -y -loglevel error -loop 1 -i "${IMGS[$i]}" -filter_complex "[0]scale=1200:2133:force_original_aspect_ratio=increase,crop=1200:2133,zoompan=z='1.04+0.06*on/$frames':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$frames:s=1080x1920:fps=30,format=yuv420p[v]" -map "[v]" -t "${DUR[$i]}" -c:v libx264 -preset medium -crf 19 -an $B/scene_$i.mp4
done
rm -f $B/vlist.txt; for i in $(seq 0 $N); do echo "file '$B/scene_$i.mp4'" >> $B/vlist.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i $B/vlist.txt -c copy $B/video_full.mp4
starts=(0); acc=0
for i in $(seq 0 $((N-1))); do acc=$(python3 -c "print($acc+${DUR[$i]})"); starts+=($acc); done
VO_IN=""; for i in $(seq 0 $N); do VO_IN="$VO_IN -i $D/vo_${VOIDX[$i]}.wav"; done
FILTER=""
for i in $(seq 0 $N); do ms=$(python3 -c "print(int(${starts[$i]}*1000))"); FILTER="$FILTER[$i:a]adelay=$ms|${ms}[a$i];"; done
MIXIN=""; for i in $(seq 0 $N); do MIXIN="$MIXIN[a$i]"; done
FILTER="$FILTER${MIXIN}amix=inputs=$((N+1)):normalize=0[vo]"
ffmpeg -y -loglevel error $VO_IN -f lavfi -i "sine=frequency=98:duration=$TOTAL" -f lavfi -i "sine=frequency=147:duration=$TOTAL" -f lavfi -i "anoisesrc=color=pink:amplitude=0.5:duration=$TOTAL" -filter_complex "${FILTER};[6:a]volume=0.020,lowpass=f=300[t1];[7:a]volume=0.014,lowpass=f=400[t2];[8:a]volume=0.006,lowpass=f=500[t3];[vo][t1][t2][t3]amix=inputs=4:normalize=0,alimiter=limit=0.9[aout]" -map "[aout]" -c:a aac -b:a 160k $B/audio_full.m4a
python3 - "$B" "${DUR[@]}" <<'PYEOF'
import sys
B=sys.argv[1]; durs=[float(x) for x in sys.argv[2:]]
names=["HOOK","அசுவினி","பரணி","கார்த்திகை","ரோகிணி","CTA"]
planet=["","திசாதிபதி: கேது","திசாதிபதி: சுக்கிரன்","திசாதிபதி: சூரியன்","திசாதிபதி: சந்திரன்",""]
deity=["","அதிதேவதை: பிரம்மா","அதிதேவதை: லட்சுமி","அதிதேவதை: ருத்திரன் (சிவன்)","அதிதேவதை: அம்பா (பார்வதி)",""]
def ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
hdr="""[Script Info]
PlayResX: 1080
PlayResY: 1920
ScriptType: v4.00+
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Noto Sans Tamil UI,66,&H00FFFFFF,&H00FFFFFF,&H80000000,&HB4000000,1,0,0,0,100,100,0,0,3,8,0,2,60,60,1050,1
Style: HookSub,Noto Sans Tamil UI,42,&H00F0E6C8,&H00F0E6C8,&H80000000,&HB4000000,0,0,0,0,100,100,0,0,3,6,0,2,60,60,1280,1
Style: Nak,Noto Sans Tamil UI,104,&H00FFFFFF,&H00FFFFFF,&H80000000,&HB4000000,1,0,0,0,100,100,0,0,3,10,0,2,60,60,640,1
Style: Planet,Noto Sans Tamil UI,58,&H00B8E9FF,&H00B8E9FF,&H80000000,&HB4000000,1,0,0,0,100,100,0,0,3,7,0,2,60,60,480,1
Style: Deity,Noto Sans Tamil UI,58,&H00FFFFFF,&H00FFFFFF,&H80000000,&HB4000000,1,0,0,0,100,100,0,0,3,7,0,2,60,60,340,1
Style: Foot,Noto Sans Tamil UI,34,&H00F0E6C8,&H00F0E6C8,&H80000000,&HEE000000,0,0,0,0,100,100,0,0,3,6,0,2,30,30,190,1
Style: WM,DejaVu Sans,26,&H66FFFFFF,&H66FFFFFF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,8,50,40,60,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
t=0; total=sum(durs)
foot="திசாதிபதி கிரகத்தின் அதிதேவதை · தொகுப்பு (derived)"
for i,d in enumerate(durs):
    st,en=ts(t),ts(t+d)
    if i==0:
        ev.append(f"Dialogue: 0,{st},{en},Hook,,0,0,0,,உங்கள் நட்சத்திர திசாதிபதியின்\\Nஅதிதேவதை தெரியுமா?")
        ev.append(f"Dialogue: 0,{st},{en},HookSub,,0,0,0,,முதல் 4 நட்சத்திரங்கள் · நூல் தொகுப்புப்படி")
    elif i==5:
        ev.append(f"Dialogue: 0,{st},{en},Hook,,0,0,0,,உங்கள் நட்சத்திரத்தை\\Nகமென்டில் சொல்லுங்கள்")
    else:
        ev.append(f"Dialogue: 0,{st},{en},Nak,,0,0,0,,{names[i]}")
        ev.append(f"Dialogue: 0,{st},{en},Planet,,0,0,0,,{planet[i]}")
        ev.append(f"Dialogue: 0,{st},{en},Deity,,0,0,0,,{deity[i]}")
        ev.append(f"Dialogue: 0,{st},{en},Foot,,0,0,0,,{foot}")
    t+=d
ev.append(f"Dialogue: 0,{ts(0)},{ts(total)},WM,,0,0,0,,astro_guidance_108")
open(f"{B}/caps.ass","w").write(hdr+"\n".join(ev)+"\n")
PYEOF
ffmpeg -y -loglevel error -i $B/video_full.mp4 -i $B/audio_full.m4a -filter_complex "[0:v]ass=$B/caps.ass:fontsdir=/usr/share/fonts/truetype/noto[v]" -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 20 -c:a copy -shortest $D/nakshatra_deity_reel_draft.mp4
echo BUILT

