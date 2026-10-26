import subprocess,json
root='/tmp/murugan-preview'
bounds=[0,6.55,14.91,24.55,30.32,42.86,49.77,61.06,69.36,73.72]
json.dump(bounds,open(root+'/timings.json','w'))
for i in range(9):
 frames=round(bounds[i+1]*24)-round(bounds[i]*24)
 cmd=['ffmpeg','-v','error','-y','-i',f'{root}/scene-{i+1:02d}.jpg','-vf',f"zoompan=z='min(zoom+0.000025,1.02)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=720x1280:fps=24",'-frames:v',str(frames),'-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p',f'{root}/part-{i+1:02d}.mp4']
 subprocess.run(cmd,check=True)
open(root+'/concat.txt','w').write('\n'.join(f"file '{root}/part-{i+1:02d}.mp4'" for i in range(9)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',root+'/concat.txt','-i','/downloads/speech-20261026-173401-26e0f17d.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','23','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest','/downloads/murugan-nine-tuesdays-review.mp4'],check=True)
