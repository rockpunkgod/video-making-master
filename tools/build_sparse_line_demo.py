"""Produce the selected original one-line direction; native execution is separate."""
import argparse
import hashlib
import json
import math
import wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--duration', type=int, choices=[6, 20], default=6)
p.add_argument('--amplitude', type=float, default=90)
a = p.parse_args()
if not 30 <= a.amplitude <= 150:
    raise ValueError('Amplitude outside demo range')
out = a.out.resolve(); out.mkdir(parents=True, exist_ok=False); (out/'assets').mkdir()
brief = ROOT/'skills/video-art-direction/examples/resonance-brief.json'
c = dict(name='ONE_LINE', width=1920, height=1080, duration=a.duration, fps=30,
         animation='original-single-line', amplitude=a.amplitude, motion_expectation='required',
         selected_direction='single-line', brief_sha256=hashlib.sha256(brief.read_bytes()).hexdigest(),
         course_fidelity='original_variant_not_a_course_reproduction')
c['path_expression'] = r'''
var A=thisComp.layer("LINE_CONTROLS").effect("Amplitude")(1), t=time;
function smooth(a,b,v){var q=Math.max(0,Math.min(1,(v-a)/(b-a)));return q*q*(3-2*q);}
function packet(x,start,speed){var age=t-start;if(age<=0)return 0;var center=430+speed*age;
 return smooth(0,.22,age)*Math.exp(-age/4.2)*Math.exp(-Math.pow((x-center)/190,2))*Math.sin((x-center)/70);}
function y(x){var u=(x-260)/1400,edge=Math.pow(Math.max(0,Math.sin(Math.PI*u)),1.3),blend=smooth(9,13,t);
 var local=packet(x,1.1,190)+.8*packet(x,5.4,175)+.65*packet(x,8.3,160);
 var global=.62*Math.sin(2*Math.PI*.55*t)*Math.sin(3*Math.PI*u),settle=1-.97*smooth(17,20,t);
 return 690-A*edge*((1-blend)*local+blend*global)*settle;}
var P=[],I=[],O=[],step=1400/120;
for(var i=0;i<=120;i++){var x=260+i*step,derivative=(y(Math.min(1660,x+.5))-y(Math.max(260,x-.5)))/(i==0||i==120?.5:1);
 P.push([x,y(x)]);I.push([-step/3,-derivative*step/3]);O.push([step/3,derivative*step/3]);}
createPath(P,I,O,false);
'''
# Self-authored sparse harmonic impacts; no noise, pad, ASR, or external recording.
sr=48000; n=sr*a.duration
stems={name:np.zeros((n,2)) for name in ['impulses','harmony']}
def event(name,start,length,freqs,gain,pan=0):
    if start>=a.duration:return
    count=min(round(length*sr),n-round(start*sr));t=np.arange(count)/sr
    env=(1-np.exp(-t/.012))*np.exp(-t/.65)*np.minimum(1,np.maximum(0,length-t)/.4)
    if name=='harmony':env=np.minimum(1,t/.4)*np.exp(-t/2)*np.minimum(1,np.maximum(0,length-t)/1)
    signal=sum(np.sin(2*math.pi*f*t) for f in freqs)/len(freqs)*gain*env
    pos=round(start*sr);stems[name][pos:pos+count,0]+=signal*math.sqrt((1-pan)/2);stems[name][pos:pos+count,1]+=signal*math.sqrt((1+pan)/2)
for start,freq,gain in [(1.1,196,.32),(5.4,220,.28),(8.3,246.9417,.24)]:event('impulses',start,3,[freq,freq*2],gain,-.1)
event('harmony',13.35,6.1,[196,293.6648],.25,.05)
t=np.arange(n)/sr
for name in stems:stems[name]*=np.minimum(1,np.maximum(0,a.duration-t)/.4)[:,None]
mix=sum(stems.values());assert np.max(abs(mix))<.7
for name,signal in {**stems,'score':mix}.items():
    with wave.open(str(out/f'assets/{name}.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.round(signal*32767).astype('<i2').tobytes())
c['audio_assets']=[(out/f'assets/{name}.wav').as_posix() for name in stems]
(out/'request.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'plan.json').write_text(json.dumps(dict(status='original_direction_native_test_pending',selected_brief=str(brief),brief_sha256=c['brief_sha256'],duration=a.duration,subtractions=['chapter cards','112-vector field','orbit scene','header and footer','continuous pad'],scope='Live editable vector path with amplitude control; new original variant of wave/delay principles, not the course Write-on workflow'),indent=2)+'\n',encoding='utf-8')
body=(ROOT/'tools/sparse_line_demo.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(ROOT/'skills/after-effects/ae-advanced-expressions/scripts/json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(c)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8')
(out/'audio-authorship.json').write_text(json.dumps(dict(source='Original sparse sine partials; no noise or constant pad',sample_rate=sr,channels=2,seconds=a.duration,peak=float(np.max(abs(mix))),listening='pending'),indent=2)+'\n',encoding='utf-8')
print(out/'build.jsx')
