"""Original editable AE composition; reuse lab native execution/rendering tools."""
import argparse,json,math,wave
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--config',type=Path,default=ROOT/'skills/after-effects/ae-advanced-expressions/examples/compositions/resonance.json');a=p.parse_args()
c=json.loads(a.config.read_text(encoding='utf-8'));out=a.out.resolve();out.mkdir(parents=True,exist_ok=False);(out/'assets').mkdir()
assert (c['width'],c['height'],c['fps'],c['duration'])==(1920,1080,30,20)
c.update(name='RESONANCE_MASTER',animation='creative-combination',motion_expectation='required')
c['rgb']={k:[int(v[i:i+2],16)/255 for i in [0,2,4]] for k,v in c['palette'].items()}
# Self-authored harmonic score: no downloaded recordings, noise beds, or voice.
sr=48000;n=sr*20;t=np.arange(n)/sr;stems={name:np.zeros((n,2),dtype=np.float64) for name in ['pad','pulse','accents']}
def add(name,start,duration,frequencies,amp,pan=0):
 count=min(round(duration*sr),n-round(start*sr));u=np.arange(count)/sr
 attack=np.minimum(1,u/.8);release=np.minimum(1,(duration-u)/1.5);env=np.sin(np.clip(attack*release,0,1)*math.pi/2)**2
 sound=sum(np.sin(2*math.pi*f*u+0.08*j) for j,f in enumerate(frequencies))/len(frequencies)*env*amp
 pos=round(start*sr);stems[name][pos:pos+count,0]+=sound*math.sqrt((1-pan)/2);stems[name][pos:pos+count,1]+=sound*math.sqrt((1+pan)/2)
for start,freq in [(0,[130.8128,195.9977,261.6256]),(4,[110,164.8138,220]),(9,[146.8324,220,293.6648]),(14.5,[130.8128,195.9977,329.6276])]:add('pad',start,min(7,20-start),freq,.08)
for start in [1.1,4.2,9.2,15.4]:add('accents',start,3,[523.2511,1046.5023],.055,-.2 if start<9 else .2)
for j in range(19):add('pulse',4.2+j*.52,1.25,[65.4064,130.8128],.055,math.sin(j)*.25)
fade=np.minimum(1,t/.6)*np.minimum(1,(20-t)/1.2)
for name in stems:stems[name]*=fade[:,None]*10**(c.get('audio_gain_db',6)/20)
mix=sum(stems.values());assert np.max(abs(mix))<.8
def save(path,signal):
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.round(signal*32767).astype('<i2').tobytes())
for name,signal in stems.items():save(out/f'assets/{name}.wav',signal)
save(out/'assets/score.wav',mix)
c['audio_assets']=[(out/f'assets/{name}.wav').as_posix() for name in stems]
(out/'request.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'plan.json').write_text(json.dumps(dict(status='new_composition_unreviewed',theme='共振 / Resonance',timeline=[{'seconds':[0,4.2],'idea':'A single point radiates editable delayed contours'},{'seconds':[4.2,9.4],'idea':'A field turns toward a focus and scales by distance'},{'seconds':[9.2,15.5],'idea':'Recursive historical positions form a cinematic3D wave'},{'seconds':[15,20],'idea':'Orbiting points and alternating character reveal resolve into a title'}],reused_skills=['ae-procedural-motion: delayed repetition principle','ae-advanced-expressions: type-reveal/free-pointing/distance-controller/delayed-wave/orbit'],adaptation='New artwork, camera, colors, words, inputs and timing; not a course reference clip montage',audio='Three original harmonic PCM stems; nativeAE project contains separately editable tracks; FFmpeg final audio/video packaging'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=(ROOT/'tools/resonance_demo.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(ROOT/'skills/after-effects/ae-advanced-expressions/scripts/json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(c)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8')
(out/'audio-authorship.json').write_text(json.dumps(dict(source='Original deterministic sine partials/chords; no noise generator, speech, or external recordings',sample_rate=sr,channels=2,seconds=20,peak=float(np.max(abs(mix))),rms=float(np.sqrt(np.mean(mix**2))),stems=list(stems),limiting_or_clipping=False),indent=2)+'\n')
print(out/'build.jsx')
