"""Build course24 hinged-wing loop; not a substitute for missing Particular."""
import argparse,json,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
p.add_argument('--profile',type=Path,default=Path(__file__).resolve().parents[1]/'examples/course-butterfly-rig.json')
p.add_argument('--style',choices=['monarch','moth','petal','mechanical'])
p.add_argument('--mode',choices=['flap','flight'])
p.add_argument('--speed',type=float)
a=p.parse_args();cfg=json.loads(a.profile.read_text(encoding='utf-8'))
if a.style:cfg['style']=a.style
if a.mode:cfg['mode']=a.mode
speed=a.speed if a.speed is not None else cfg.get('speed',1)
if not math.isfinite(speed) or not .5<=speed<=2:raise ValueError('Speed must be0.5–2')
if cfg['style'] not in ['monarch','moth','petal','mechanical'] or cfg['mode'] not in ['flap','flight']:raise ValueError('Unsupported rig variant')
if cfg['fps']!=25 or cfg['width']!=790 or cfg.get('native_height',cfg['height'])!=633 or cfg['duration']!=8:raise ValueError('Current course rig uses790x633/25fps/8s')
if len(cfg['key_frames'])!=4 or len(cfg['key_angles'])!=4 or cfg['key_frames'][0]!=0 or sorted(set(cfg['key_frames']))!=cfg['key_frames']:raise ValueError('Four increasing course samples required')
if any(not math.isfinite(x) or abs(x)>70 for x in cfg['key_angles']):raise ValueError('Wing samples exceed candidate range')
if not math.isfinite(cfg['camera_tilt']) or not 0<=cfg['camera_tilt']<=80:raise ValueError('Camera tilt outside candidate bounds')
cfg['speed']=speed;cfg['variant']=bool(a.style or a.mode or speed!=1)
cfg['native_height']=633;cfg['height']=634;cfg['delivery_padding']=[0,1]
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
for name,value in [('request.json',cfg),('plan.json',dict(skill='ae-advanced-expressions',branch='course24-hinged-wing',status='candidate',steps=['Create original editable source artwork and mask it','Mirror wing precomp; place3D hinge anchors at body','Right four Y keys with pingpong loop, left opposite right','Parent body/wings to2D null; optional native spatial Bezier flight and Along Path orientation','Save/reopen; edit/restore key amplitude; native full-frame trace; render'],missing='Particular absent: no particle tail replacement or full lesson completion claim'))]:
    (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
scripts=Path(__file__).parent
body=(scripts/'butterfly_rig.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
