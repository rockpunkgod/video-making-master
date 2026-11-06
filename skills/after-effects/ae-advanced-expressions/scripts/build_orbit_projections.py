"""Course29: separate no-keyframe orbit, Cartesian projections and self rotation."""
import argparse,json,shutil,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--radius',type=float,default=80);ap.add_argument('--speed',type=float,default=2);ap.add_argument('--asset',type=Path);ap.add_argument('--guides',action='store_true');ap.add_argument('--no-spin',action='store_true');a=ap.parse_args()
if not math.isfinite(a.radius) or not 40<=a.radius<=90:raise ValueError('Current400square scene supports radius40–90')
if not math.isfinite(a.speed) or not .2<=abs(a.speed)<=4:raise ValueError('Nonzero angular speed magnitude.2–4 radians/second')
if a.asset and (not a.asset.is_file() or a.asset.suffix.lower() not in ['.png','.jpg','.jpeg']):raise ValueError('Existing own PNG/JPG required')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
cfg=dict(name='COURSE_ORBIT_PROJECTIONS',animation='orbit-projections',motion_expectation='required',width=800,height=800,native_width=400,native_height=400,duration=10,fps=30,center=[200,200],radius=a.radius,speed=a.speed,projection_offset=150,guides=a.guides,spin=not a.no_spin,asset=None,background=[0,.2,.145],yellow=[1,1,.6],purple=[.64,.56,1],inferred=['Disc40,projection dots20,center dot10 from visible ratios','Background/purple colors approximated from footage, yellow255/255/153 visible in Info','Guide extent280 inferred; parentage and55percent opacity observed','2x output wrapper is self adaptation; source native400square explicitly spoken'],variant=a.radius!=80 or a.speed!=2 or bool(a.asset) or a.guides or a.no_spin)
if a.asset:
    (out/'assets').mkdir();dest=out/'assets'/('disc'+a.asset.suffix.lower());shutil.copy2(a.asset,dest);cfg['asset']=dest.as_posix()
for name,obj in [('request.json',cfg),('plan.json',dict(status='candidate',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=29',steps=['Own editable split-color disc or caller image precomp','Center layer drives cos/sin orbit and separateX/Y projections','Keep two guide parents and55opacity, hidden in final baseline','Original(time/Math.PI)*360 spin; no authored motion keys','Native edit/save/reopen/restore; all300frames; real movie checks'],course_fidelity='Original expression structure; own vectors/colors and image adaptation explicitly bounded'))]:
    (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=Path(__file__).resolve().parent;body=(s/'orbit_projections.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
