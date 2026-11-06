"""Original audiovisual test materials and a parameterized native Premiere sound plan.
Existing FFmpeg creates source textures; Windows SAPI supplies non-imitative lab speech.
All creative gain envelopes and timeline placement remain editable in Premiere.
"""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
import numpy as np
from pr_presets import sequence_preset,ROLES

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('E:/自媒体/Adobe Premiere Pro 2026/Settings/SequencePresets/HD 1080p/HD 1080p 23.976 fps.sqpreset')
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--variant',choices=['baseline','variation','reveal'],default='baseline');a=ap.parse_args()
out=a.out.resolve();(out/'inputs').mkdir(parents=True,exist_ok=False)

def run(cmd):
    result=subprocess.run(cmd,capture_output=True)
    if result.returncode:raise RuntimeError(result.stderr.decode('utf-8',errors='replace')[-2500:])
    return result
def length(path):return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]).stdout)
def normalize(raw,dest,peak):
    decoded=run(['ffmpeg','-v','error','-i',str(raw),'-ar','48000','-ac','2','-f','f32le','-']).stdout
    samples=np.frombuffer(decoded,dtype='<f4');maximum=float(np.max(np.abs(samples)))
    if maximum<=0:raise ValueError('Silent original input')
    run(['ffmpeg','-v','error','-n','-i',str(raw),'-af',f'volume={peak/maximum:.12f}','-ar','48000','-ac','2','-c:a','pcm_s24le',str(dest)])
def sound(name,filter,duration,peak):
    raw=out/'inputs'/(name+'-source.wav');dest=out/'inputs'/(name+'.wav')
    run(['ffmpeg','-v','error','-n','-f','lavfi','-i',filter,'-t',str(duration),'-ar','48000','-ac','2','-c:a','pcm_s24le',str(raw)])
    normalize(raw,dest,peak);return dest

variant=['baseline','variation','reveal'].index(a.variant);seed=237+variant*31
sources=[ROOT/'samples/tracking-fixture-001/source.mp4',ROOT/'samples/tracking-corridor-001/final.mp4',ROOT/'samples/tracking-gallery-001/final.mp4']
if variant==1:sources=[sources[2],sources[0],sources[1]]
if variant==2:sources=[sources[1],sources[2],sources[0]]
pictures=[];cursor=0
for i,src in enumerate(sources):
    dest=out/'inputs'/f'picture-{i}.mp4';shutil.copy2(src,dest);duration=length(dest)
    pictures.append({'path':str(dest),'start':cursor,'duration':duration,'in':0});cursor+=duration
duration=cursor;cuts=[p['start'] for p in pictures[1:]]
music=sound('music',f'aevalsrc=0.12*sin(2*PI*{110+variant*12}*t)+0.07*sin(2*PI*{165+variant*18}*t)+0.04*sin(2*PI*{220+variant*24}*t):s=48000:d={duration}',duration,.32)
rooms=[]
for i in range(3):rooms.append(sound(f'room-{i}',f'anoisesrc=color={"brown" if i%2 else "pink"}:amplitude=0.2:sample_rate=48000:seed={seed+i},lowpass=f={700+i*600+variant*70}',duration,.22))
foley=sound('foley',f'anoisesrc=color=white:amplitude=.3:sample_rate=48000:seed={seed+9},highpass=f=250,lowpass=f=3500,afade=t=out:st=0.03:d=0.27',.3,.45)
riser=sound('riser',f'aevalsrc=0.18*sin(2*PI*(180*t+{500+variant*100}*t*t)):s=48000:d=1.5',1.5,.4)
impact=sound('impact','aevalsrc=0.7*sin(2*PI*(80*t-12*t*t))*exp(-6*t):s=48000:d=1.2',1.2,.65)
detail=sound('detail',f'aevalsrc=0.2*sin(2*PI*{880+variant*220}*t)*exp(-12*t):s=48000:d=0.5',.5,.32)
phrases=[['Hold your position. Follow the signal.','The room is clear.'],['Wait for the door. Move when it opens.','We found another way.'],['Listen carefully. The signal is changing.','Now we can proceed.']][variant]
voices=[]
for i,text in enumerate(phrases):
    raw=out/'inputs'/f'dialogue-{i}-source.wav';dest=out/'inputs'/f'dialogue-{i}.wav'
    run(['powershell','-NoProfile','-File',str(ROOT/'tools/synthesize_lab_dialogue.ps1'),'-OutputPath',str(raw),'-Text',text]);normalize(raw,dest,.6);voices.append(dest)

clips=[];voiced=[]
def add(path,track,start,duration,role,db=0,fade_in=.03,fade_out=.08,shape=None,duck=0):
    item={'path':str(path),'track':track,'start':round(start,6),'duration':round(duration,6),'source_in':0,'role':role,'nominal_db':db,'fade_in':fade_in,'fade_out':fade_out,'shape':shape,'duck_db':duck}
    clips.append(item);return item
for i,path in enumerate(voices):
    start=.7 if i==0 else cuts[1]-.35;d=min(length(path),duration-start-.2)
    add(path,0,start,d,'dialogue',-1,.02,.06);voiced.append([start,start+d])
add(music,1,0,duration,'music',-6,.3,.6,duck=-10)
overlap=.8
for i,path in enumerate(rooms):
    start=0 if i==0 else cuts[i-1]-overlap/2
    end=duration if i==2 else cuts[i]+overlap/2
    add(path,2 if i%2==0 else 3,start,end-start,'ambience',-13,overlap if i else .25,overlap if i<2 else .5,'equal_power',-4)
for t in [.6,cuts[0]+.4,cuts[1]+.7]:add(foley,4,t,.3,'foley',-8,.01,.18)
add(riser,5,cuts[0]-1.5,1.5,'riser',-2,1.5,.025,'riser')
add(impact,6,cuts[0],1.2,'impact',-5,.005,.55)
add(detail,7,cuts[1],.5,'detail',-6,.005,.25)

def envelope(clip,t):
    local=t-clip['start'];d=clip['duration'];gain=10**(clip['nominal_db']/20)
    if local<0 or local>d:return 0
    fi=clip['fade_in'];fo=clip['fade_out'];g=min(1,local/fi) if fi else 1;g*=min(1,max(0,(d-local)/fo)) if fo else 1
    if clip['shape']=='equal_power':
        g=1
        if fi and local<fi:g*=math.sin(math.pi/2*local/fi)
        if fo and local>d-fo:g*=math.sin(math.pi/2*(d-local)/fo)
    if clip['shape']=='riser':g=(max(0,min(1,local/d))**2)*min(1,max(0,(d-local)/.025))
    if clip['duck_db']:
        reduction=0
        for start,end in voiced:
            if start-.15<=t<=end+.45:
                amount=min(1,max(0,(t-(start-.15))/.15),max(0,(end+.45-t)/.45))
                reduction=min(reduction,clip['duck_db']*amount)
        gain*=10**(reduction/20)
    return max(0,g*gain)

for clip in clips:
    d=clip['duration'];events={0,d}
    events.update(min(d,k/20) for k in range(math.ceil(d*20)+1))
    for v in voiced:
        for t in [v[0]-.15,v[0],v[1],v[1]+.45]:
            local=t-clip['start']
            if 0<=local<=d:events.add(local)
    for t in [clip['fade_in'],d-clip['fade_out']]:
        if 0<=t<=d:events.add(t)
    rounded={round(t,8) for t in events}
    clip['gain_keys']=[[t,envelope(clip,clip['start']+t)] for t in sorted(rounded)]
sequence_preset(BASE,out/'sequence.sqpreset')
plan={'variant':a.variant,'width':960,'height':540,'fps':24,'duration':duration,'picture_clips':pictures,'cuts':cuts,'track_roles':ROLES,'audio_clips':clips,'dialogue_windows':voiced,'native_unity_parameter':.17782793939114,'audio_sample_rate':48000,'reference_sources':['OagnZAD_9wY 11:46-19:09','KECzwyUursc 01:40-05:41'],'original_assets':True,'source_invention_notice':'Original test sound textures made by FFmpeg; speech by installed Windows SAPI; no copied tutorial sounds','plugin_effects':'No unverified reverb/EQ API calls; source sound textures are inputs, all timeline gain curves remain native and editable'}
(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
assets=[{'file':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (out/'inputs').iterdir() if p.is_file()]
(out/'assets.json').write_text(json.dumps(assets,indent=2),encoding='utf-8');print(out/'plan.json')
