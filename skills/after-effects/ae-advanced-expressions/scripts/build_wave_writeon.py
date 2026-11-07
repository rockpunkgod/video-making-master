"""Course22 native Write-on sine composition; reuse the installed AE runner/renderer."""
import argparse,json,math,shutil
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
p.add_argument('--mode',choices=['sine','sum','product','decay','slider'],default='sum')
p.add_argument('--duration',type=float,default=10);p.add_argument('--rate-a',type=float)
p.add_argument('--amplitude-a',type=float);p.add_argument('--rate-b',type=float,default=20)
p.add_argument('--amplitude-b',type=float);p.add_argument('--speed',type=float)
p.add_argument('--asset',type=Path,help='Opaque dark720x576 PNG; painted on original image, explicit material variant')
p.add_argument('--slider-profile',type=Path,help='Explicit keyframes [{time,value}]; no invented source keys')
a=p.parse_args();mode=a.mode
cfg=dict(name='COURSE22_'+mode.upper(),animation='wave-writeon',width=720,height=576,fps=25,
 duration=a.duration,mode=mode,rate_a=a.rate_a if a.rate_a is not None else (4 if mode in ['decay','slider'] else 3),
 amplitude_a=a.amplitude_a if a.amplitude_a is not None else (40 if mode=='product' else 100 if mode=='decay' else 80),
 rate_b=a.rate_b,amplitude_b=a.amplitude_b if a.amplitude_b is not None else (5 if mode=='product' else 20),
 speed=a.speed if a.speed is not None else (75 if mode in ['decay','slider'] else 60),
 offset_y=288,brush_size=2,hardness=.79,requested_spacing=.003 if mode=='product' else .01,
 asset=None,slider_profile=None,motion_expectation='required',source=dict(id='BV1c7GTzMEh5',page=22,url='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=22'),
 limits=['Square pixels inferred; source720x576/25fps/10s and expressions observed','Enabled course stage isolated into its own editable project; old disabled demonstration stages omitted','No exact source project or full-frame aesthetic identity claim'])
if not all(math.isfinite(cfg[k]) for k in ['duration','rate_a','amplitude_a','rate_b','amplitude_b','speed']):raise ValueError('Finite parameters required')
if not(4<=a.duration<=12 and abs(a.duration*25-round(a.duration*25))<1e-6 and .5<=cfg['rate_a']<=8 and 5<=cfg['rate_b']<=30 and 1<=cfg['amplitude_a']<=200 and 1<=cfg['amplitude_b']<=30 and 30<=cfg['speed']<=100):raise ValueError('Outside current candidate bounds')
if (mode=='slider')!=bool(a.slider_profile):raise ValueError('Slider requires an explicit profile; other modes do not use it')
if a.slider_profile:
 rows=json.loads(a.slider_profile.read_text(encoding='utf-8'))['keyframes']
 if len(rows)<2 or rows[0]['time']!=0 or rows[-1]['time']>a.duration or any(not all(math.isfinite(x[k]) for k in ['time','value']) or not 0<=x['value']<=300 for x in rows) or any(x['time']>=y['time'] for x,y in zip(rows,rows[1:])):raise ValueError('Invalid slider keyframes')
 cfg['slider_profile']=rows;cfg['limits'].append('Slider profile is caller-authored or explicitly source-inferred, never recovered source keys')
asset=None
if a.asset:
 from PIL import Image
 asset=a.asset.resolve();im=Image.open(asset).convert('RGBA')
 if asset.suffix.lower()!='.png' or im.size!=(720,576) or im.getchannel('A').getextrema()!=(255,255) or max(v[1] for v in im.convert('RGB').getextrema())>96:raise ValueError('Pixel QA supports opaque720x576 PNG with all RGB channels<=96')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
if asset:
 (out/'assets').mkdir();shutil.copy2(asset,out/'assets/material.png');cfg['asset']=(out/'assets/material.png').as_posix()
 cfg['limits'].append('Caller dark PNG is an explicit OnOriginalImage material variant, original course uses black Solid')
for name,data in [('request.json',cfg),('plan.json',dict(skill='ae-advanced-expressions',unit='writeon_history',branch='course22-wave-composition',status='candidate',source=cfg['source'],steps=['Create black full-frame Solid or copy declared material','Apply native Write-on and reviewed course expression','Save/reopen/edit brush/restore','Trace native formula and export effect on/off PNGs','Render actual AE frames and check retained history pixels'],course_fidelity='original expressions; explicit adapters and source uncertainty retained'))]:
 (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
scripts=Path(__file__).parent;body=(scripts/'wave_writeon.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
