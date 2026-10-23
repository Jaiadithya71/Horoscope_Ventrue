import subprocess, sys
ci=int(sys.argv[1])
V='/tmp/voice3/'
ORDER=['hook','mon1','mon2','mon3','tue1','tue2','tue3','wed1','wed2','wed3','thu1','thu2','thu3','fri1','fri2','fri3','fri4','sat1','sat2','sat3','sun1','sun2','sun3','cta1','cta2']
IMGS={s:f'/downloads/d_{s}.png' for s in ORDER}; IMGS['hook']='/downloads/d_hook.png'
GAP=0.12
def dur(p):
    return float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
durs=[dur(V+s+'.mp3')+GAP for s in ORDER]
starts=[]; t=0
for d in durs: starts.append(t); t+=d
CHUNKS=[(0,9),(9,17),(17,25)]
a,b=CHUNKS[ci]; n=b-a
inputs=[]
for i in range(a,b): inputs+=['-loop','1','-t',f"{durs[i]:.3f}",'-i',IMGS[ORDER[i]]]
inputs+=['-loop','1','-t',f"{sum(durs[a:b]):.3f}",'-i','/tmp/reeld/wm.png']
for i in range(a,b): inputs+=['-loop','1','-t',f"{sum(durs[a:b]):.3f}",'-i',f'/tmp/reeld/cap{i}.png']
fc=[]; sv=[]
for j,i in enumerate(range(a,b)):
    dd=durs[i]
    xexpr=f"'(in_w-out_w)*t/{dd:.3f}'" if i%2==0 else f"'(in_w-out_w)*(1-t/{dd:.3f})'"
    fc.append(f"[{j}:v]scale=1404:2496,crop=1080:1920:x={xexpr}:y=220,eq=brightness=-0.05:saturation=1.1,fps=24,format=yuv420p[v{j}]")
    sv.append(f"[v{j}]")
fc.append(''.join(sv)+f"concat=n={n}:v=1:a=0[cc]")
fc.append(f"[cc][{n}:v]overlay=0:0[cw]")
prev='cw'; base=starts[a]
for j,i in enumerate(range(a,b)):
    st=starts[i]-base; en=st+durs[i]; out=f"co{j}"
    fc.append(f"[{prev}][{n+1+j}:v]overlay=0:0:enable='gte(t,{st:.3f})*lt(t,{en:.3f})'[{out}]")
    prev=out
fc.append(f"[{prev}]format=yuv420p[vv]")
cmd=['ffmpeg','-y','-nostdin','-v','error']+inputs+['-filter_complex',';'.join(fc),'-map','[vv]','-t',f"{sum(durs[a:b]):.3f}",'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-an',f'/tmp/reeld/chunk{ci}.mp4']
r=subprocess.run(cmd,capture_output=True,text=True)
print('rc',r.returncode, r.stderr[-400:] if r.returncode else 'ok')
