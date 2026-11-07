"""Course35 native length/linear distance mapping; explicit hand-drag replay."""
import argparse,json,math,shutil
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['scale','blur'],default='scale');p.add_argument('--profile',type=Path);p.add_argument('--duration',type=float,default=5);p.add_argument('--radius',type=float,default=70);p.add_argument('--near-scale',type=float,default=250);p.add_argument('--far-scale',type=float,default=70);p.add_argument('--near-blur',type=float,default=40);p.add_argument('--control-time',type=float,default=.6);p.add_argument('--distance-method',choices=['two-point','sub-length'],default='two-point');p.add_argument('--assets',nargs=4,type=Path);a=p.parse_args()
s=Path(__file__).resolve().parent;profile=a.profile or s.parent/f'examples/p35-{a.mode}-replay-inferred.json';r=json.loads(profile.read_text(encoding='utf-8'));keys=r['keyframes'];duration=a.duration
if not all(math.isfinite(x) for x in [duration,a.radius,a.near_scale,a.far_scale,a.near_blur]):raise ValueError('Finite parameters required')
if not(3<=duration<=10 and abs(duration*25-round(duration*25))<1e-6 and 20<=a.radius<=120 and 150<=a.near_scale<=300 and 50<=a.far_scale<=100 and 5<=a.near_blur<=60):raise ValueError('Outside candidate input bounds')
if len(keys)<3 or keys[0]['time']!=0 or keys[-1]['time']<=0:raise ValueError('Replay needs ordered positions starting0')
previous=-1
for k in keys:
 if k['time']<=previous or len(k['position'])!=2 or not all(math.isfinite(v) and -100<=v<=420 for v in k['position']):raise ValueError('Invalid 2D replay profile')
 previous=k['time']
if not 0<=a.control_time<duration:raise ValueError('Diagnostic control time must lie inside movie')
last=keys[-1]['time'];keys=[dict(time=k['time']*duration/last,position=k['position']) for k in keys]
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False);assets=[]
if a.assets:
 from PIL import Image
 (out/'assets').mkdir()
 for i,f in enumerate(a.assets):
  im=Image.open(f).convert('RGBA')
  if f.suffix.lower()!='.png' or im.size!=(44,44) or im.getchannel('A').getextrema()!=(0,255):raise ValueError('Four44x44PNG with transparent exterior and opaque artwork required')
  dest=out/f'assets/art-{i}.png';shutil.copy2(f,dest);assets.append(dest.as_posix())
c=dict(name='COURSE35_DISTANCE',animation='distance-controller',mode=a.mode,width=320,height=240,pixel_aspect=1,fps=25,duration=duration,radius=a.radius,near_scale=a.near_scale,far_scale=a.far_scale,near_blur=a.near_blur,distance_method=a.distance_method,control_time=a.control_time,keyframes=keys,positions=[[41,120],[121,120],[201,120],[281,120]],background=[0,45/255,39/255],controller_color=[1,1,153/255],controller_opacity=30,controller_diameter=40,assets=assets,motion_expectation='required',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=35',inferred=['320x240canvas/PAR1 from recording and source positions; source Comp dialog not read','25fps is recording-replay adapter; source29.97 Preview not proof ofCompFPS','Own44px badge/Arial34 substitutes unavailableAI artwork; font/exactbounds not source identity','Source manual dragging mapped to measured controller keys; original had no motionKframes','Recorded darkgreen background approximated by explicit bottomSolid for predictable delivery; source matte implementation not read'],profile_provenance=r)
for name,v in [('request.json',c),('plan.json',dict(skill='ae-advanced-expressions',branch='distance-controller',status='candidate',steps=['Centered unparented2D artwork','Same-space length or sub/length','Vector linear250/70 or scalar FastBlur40/0 over0..70distance','Explicit measured controller replay without target property keys','Native save/reopen/edit/restore, actual render and independent pixel/parameter checks'],source=c['source']))]:
 (out/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=(s/'distance_controller.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(c)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
