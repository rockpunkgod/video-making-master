"""Use licensed recorded cloth swishes, aligned by measured source energy peak."""
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1];source=root/'samples/pr-sound-suite-001/baseline-quiet-001';out=root/'samples/pr-sound-suite-001/baseline-soft-transitions-001'
out.mkdir(exist_ok=False);shutil.copytree(source/'inputs',out/'inputs');shutil.copy2(source/'sequence.sqpreset',out/'sequence.sqpreset')
plan=json.loads((source/'compiled-plan.json').read_text(encoding='utf-8'))
for spec in [*plan['picture_clips'],*plan['audio_clips']]:spec['path']=str(out/Path(spec['path']).relative_to(source))
sources=[('fs_495390_Foley_Whoosh_Clothes-wav.mp3',1.15,1.0,.30),('fs_391448_Shirt-Whoosh-1-wav.mp3',.20,1.1,.24)]
events=[]
for i,(name,start,duration,peak) in enumerate(sources):
    src=root/'samples/licensed-sfx-001'/name;raw=out/'inputs'/f'transition-{i}-recorded-source.wav';dest=out/'inputs'/f'transition-{i}.wav'
    subprocess.run(['ffmpeg','-v','error','-n','-ss',str(start),'-i',str(src),'-t',str(duration),'-af','highpass=f=80,lowpass=f=3500','-ar','48000','-ac','2','-c:a','pcm_s24le',str(raw)],capture_output=True,check=True)
    b=subprocess.run(['ffmpeg','-v','error','-i',str(raw),'-f','f32le','-'],capture_output=True,check=True).stdout
    samples=np.frombuffer(b,dtype='<f4').reshape(-1,2);maximum=float(np.abs(samples).max());mono=samples.mean(1);frames=len(mono)//480;energy=np.sqrt(np.mean(mono[:frames*480].reshape(frames,480).astype(float)**2,axis=1));event=float(np.argmax(energy))*.01
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-af',f'volume={peak/maximum:.12f}','-c:a','pcm_s24le',str(dest)],capture_output=True,check=True)
    events.append({'path':str(dest),'duration':len(samples)/48000,'peak_offset':event,'source_clip':str(src),'source_trim_start':start,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
plan['audio_clips']=[c for c in plan['audio_clips'] if c['role']!='foley']
for i,role in enumerate(['riser','detail']):
    clip=next(c for c in plan['audio_clips'] if c['role']==role);event=events[i];cut=plan['cuts'][i]
    clip.update(path=event['path'],start=cut-event['peak_offset'],duration=event['duration'],nominal_db=-6 if i==0 else -8,fade_in=.12,fade_out=.3,shape='recorded_whoosh',duck_db=0)
    duration=clip['duration'];times={0,duration,.12,duration-.3,event['peak_offset']};times.update(k/20 for k in range(math.floor(duration*20)+1));values=[]
    for t in sorted(times):
        g=math.sin(math.pi/2*min(1,t/.12))*math.sin(math.pi/2*min(1,max(0,(duration-t)/.3)))
        values.append([round(t,8),10**(clip['nominal_db']/20)*g])
    clip['gain_keys']=values;clip['measured_peak_offset_seconds']=event['peak_offset'];clip['target_cut_seconds']=cut
impact=next(c for c in plan['audio_clips'] if c['role']=='impact');impact['nominal_db']-=8;impact['gain_keys']=[[t,v*10**(-8/20)] for t,v in impact['gain_keys']]
plan['variant']='baseline-soft-transitions-001';plan['human_feedback']={'previous_revision':'baseline-quiet-001','verdict':'noise improved, transitions still need adjustment'}
plan['revision'].update({'recorded_transitions':events,'impact_gain_delta_db':-8,'removed_unmotivated_foley':True,'peak_alignment':'measured 10ms RMS peak aligned to each cut using native exact Time placement','subjective_status':'awaiting listening'})
plan['licensed_sources']=[{'id':'fs:495390','author':'Nox_Sound','title':'Foley_Whoosh_Clothes.wav','license':'CC0','source_url':'https://freesound.org/people/Nox_Sound/sounds/495390/'},{'id':'fs:391448','author':'saturdaysoundguy','title':'Shirt Whoosh 1.wav','license':'CC0','source_url':'https://freesound.org/people/saturdaysoundguy/sounds/391448/'}]
(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'credits.md').write_text('CC0 recorded transition sources, edited for this original lab sample:\n\n'+''.join('- '+x['title']+' — '+x['author']+' — '+x['source_url']+'\n' for x in plan['licensed_sources']),encoding='utf-8')
assets=[{'file':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (out/'inputs').iterdir() if p.is_file()]
(out/'assets.json').write_text(json.dumps(assets,indent=2),encoding='utf-8');print(out/'plan.json')
