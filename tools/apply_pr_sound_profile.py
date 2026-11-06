"""Explicit quiet-transition style profile; parameters are choices, not universal mix rules."""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
import numpy as np

def run(cmd):
    result=subprocess.run(cmd,capture_output=True)
    if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace')[-2000:])
    return result

ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--first-source',type=Path,required=True);ap.add_argument('--second-source',type=Path,required=True);ap.add_argument('--first-trim',type=float,default=1.15);ap.add_argument('--second-trim',type=float,default=.20);ap.add_argument('--ambience-delta-db',type=float,default=-18);ap.add_argument('--ambience-lowpass',type=float,default=400);a=ap.parse_args()
source=a.source.resolve();out=a.out.resolve()
if not -40<=a.ambience_delta_db<=0 or not 80<=a.ambience_lowpass<=10000:raise ValueError('Invalid explicit room-bed profile')
plan=json.loads((source/'plan.json').read_text(encoding='utf-8'))
out.mkdir(exist_ok=False);shutil.copytree(source/'inputs',out/'inputs');shutil.copy2(source/'sequence.sqpreset',out/'sequence.sqpreset')
for clip in [*plan['picture_clips'],*plan['audio_clips']]:
    original=Path(clip['path']).resolve();clip['path']=str(out/original.relative_to(source))
for clip in plan['audio_clips']:
    if clip['role']=='ambience':
        src=Path(clip['path']);dest=src.with_name(src.stem+'-profile.wav')
        run(['ffmpeg','-v','error','-n','-i',str(src),'-af',f'lowpass=f={a.ambience_lowpass}','-c:a','pcm_s24le',str(dest)])
        clip['path']=str(dest);clip['nominal_db']+=a.ambience_delta_db;clip['gain_keys']=[[t,v*10**(a.ambience_delta_db/20)] for t,v in clip['gain_keys']]
events=[]
for i,(src,start,duration,peak) in enumerate([(a.first_source.resolve(),a.first_trim,1.0,.3),(a.second_source.resolve(),a.second_trim,1.1,.24)]):
    raw=out/'inputs'/f'recorded-transition-{i}-source.wav';dest=out/'inputs'/f'recorded-transition-{i}.wav'
    run(['ffmpeg','-v','error','-n','-ss',str(start),'-i',str(src),'-t',str(duration),'-af','highpass=f=80,lowpass=f=3500','-ac','2','-ar','48000','-c:a','pcm_s24le',str(raw)])
    b=run(['ffmpeg','-v','error','-i',str(raw),'-f','f32le','-']).stdout;samples=np.frombuffer(b,dtype='<f4').reshape(-1,2)
    maximum=float(np.abs(samples).max());mono=samples.mean(1);n=len(mono)//480
    if maximum<=0 or n<30:raise ValueError('Insufficient recorded transition')
    energy=np.sqrt(np.mean(mono[:n*480].reshape(n,480).astype(float)**2,axis=1));peak_offset=float(np.argmax(energy))*.01
    run(['ffmpeg','-v','error','-n','-i',str(raw),'-af',f'volume={peak/maximum:.12f}','-c:a','pcm_s24le',str(dest)])
    events.append({'path':str(dest),'duration':len(samples)/48000,'peak_offset':peak_offset,'source':str(src),'source_trim_start':start,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
plan['audio_clips']=[c for c in plan['audio_clips'] if c['role']!='foley']
for i,role in enumerate(['riser','detail']):
    clip=next(c for c in plan['audio_clips'] if c['role']==role);event=events[i];duration=event['duration'];cut=plan['cuts'][i]
    clip.update(path=event['path'],start=cut-event['peak_offset'],duration=duration,nominal_db=-6 if i==0 else -8,shape='recorded_whoosh',duck_db=0,fade_in=.12,fade_out=.3,target_cut_seconds=cut,measured_peak_offset_seconds=event['peak_offset'])
    times={0,duration,.12,duration-.3,event['peak_offset']};times.update(k/20 for k in range(math.floor(duration*20)+1))
    clip['gain_keys']=[[round(t,8),10**(clip['nominal_db']/20)*math.sin(math.pi/2*min(1,t/.12))*math.sin(math.pi/2*min(1,max(0,(duration-t)/.3)))] for t in sorted(times)]
impact=next(c for c in plan['audio_clips'] if c['role']=='impact');impact['nominal_db']-=8;impact['gain_keys']=[[t,v*10**(-8/20)] for t,v in impact['gain_keys']]
plan['profile']={'name':'quiet_recorded_transitions','ambience_gain_delta_db':a.ambience_delta_db,'ambience_lowpass_hz':a.ambience_lowpass,'recorded_events':events,'impact_gain_delta_db':-8,'unmotivated_foley_removed':True,'reference_approval':'User accepted baseline-soft-transitions-001; this new case still needs its own checks'}
(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
records=[{'file':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (out/'inputs').iterdir() if p.is_file()]
(out/'assets.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(out/'plan.json')
