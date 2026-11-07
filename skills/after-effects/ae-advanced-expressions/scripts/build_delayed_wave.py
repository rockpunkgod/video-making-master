"""Course34 recursive valueAtTime Z wave; native Solid scale and bottom controls."""
import argparse,json,math,shutil
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['fixed','controller'],default='fixed');p.add_argument('--count',type=int,default=23);p.add_argument('--duration',type=float,default=10);p.add_argument('--amplitude',type=float);p.add_argument('--rate',type=float);p.add_argument('--spacing',type=float);p.add_argument('--delay',type=float,default=.2);p.add_argument('--asset',type=Path);p.add_argument('--camera',type=Path,default=Path(__file__).resolve().parents[1]/'examples/p34-camera-inferred.json');a=p.parse_args()
c=dict(name='COURSE34_DELAYED_WAVE',animation='delayed-wave',width=720,height=576,fps=25,duration=a.duration,count=a.count,mode=a.mode,amplitude=a.amplitude if a.amplitude is not None else (40 if a.mode=='fixed' else 36),rate=a.rate if a.rate is not None else (3 if a.mode=='fixed' else 3.53),spacing=a.spacing if a.spacing is not None else (10 if a.mode=='fixed' else 21),delay=a.delay,pixel_aspect=128/117,delivery_sar='128/117',asset=None,depth_of_field=dict(enabled=True,aperture_mm=5,aperture_pixels=5*72/25.4,blur_level=100,focus='linked_to_fitted_zoom',unit_conversion='Actual AE26 CameraSettings GUI5mm readback14.1732283464567px on PAL720x576'),camera=json.loads(a.camera.read_text(encoding='utf-8')),motion_expectation='required',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=34',inferred=['Final source camera fit from selected two-bar endpoints; not recovered source camera values','23bar fixed-stage count observed near15:45; controller final count not independently read, same23bar count reused','PAL128/117 derived from source160:117 display aspect ratio, not rounded1.09','Exact source redRGB not read; pure red chosen; caller PNG is explicit artwork variant'])
if not all(math.isfinite(c[k]) for k in ['duration','amplitude','rate','spacing','delay']):raise ValueError('Finite parameters required')
if not (2<=c['count']<=30 and 4<=c['duration']<=12 and abs(c['duration']*25-round(c['duration']*25))<1e-6 and 5<=abs(c['amplitude'])<=60 and .2<=c['rate']<=6 and 4<=abs(c['spacing'])<=24 and .05<=c['delay']<=.4):raise ValueError('Outside tested candidate bounds')
asset=None
if a.asset:
 from PIL import Image
 asset=a.asset.resolve();im=Image.open(asset).convert('RGBA')
 if asset.suffix.lower()!='.png' or im.size!=(720,576) or im.getchannel('A').getextrema()!=(255,255):raise ValueError('Opaque720x576PNG required')
 if min(max(px[:3]) for px in im.getdata())<150:raise ValueError('Every material pixel needs a bright channel>=150 for current pixel probe adapter')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
if asset:
 (out/'assets').mkdir();shutil.copy2(asset,out/'assets/bar.png');c['asset']=(out/'assets/bar.png').as_posix()
for name,v in [('request.json',c),('plan.json',dict(skill='ae-advanced-expressions',branch='recursive-delayed-wave',status='candidate',steps=['Full PAL Solid scaled1/80 or explicit own PNG','First3DPosition=value+[0,0,A*cos(w*time)]','Duplicate beneath first; followers read previousPosition.valueAtTime(time-delay)+[spacing,0,0]','Keep camera/Null below all bars and bind all follower copies','Native save/reopen/edit/restore, full trace, projections, actual movie pixel QA'],source=c['source'],course_fidelity='Original recursive method, fitted camera/count/color bounds explicit'))]:
 (out/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=Path(__file__).parent;body=(s/'delayed_wave.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(c)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
