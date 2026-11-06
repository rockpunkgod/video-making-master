"""Assemble five editable lab-made AEP components using course13 native methods."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--profile',type=Path,default=Path(__file__).resolve().parents[1]/'examples/course-composite.json')
ap.add_argument('--out',required=True,type=Path)
ap.add_argument('--camera-time-scale',type=float,default=1)
ap.add_argument('--dot-seed',type=int)
ap.add_argument('--noise-width',type=float)
a=ap.parse_args();out=a.out.resolve();profile=a.profile.resolve()
if out.exists():raise FileExistsError('Fresh output required')
if not .5<=a.camera_time_scale<=1.5:raise ValueError('Candidate time scale bounds .5–1.5')
cfg=json.loads(profile.read_text(encoding='utf-8'))
if set(cfg['inputs'])!={'core','contours','noise','lines','dots'}:raise ValueError('Five explicit editable component roles required')
if len(cfg['camera_frames'])!=len(cfg['camera_z']) or sorted(set(cfg['camera_frames']))!=cfg['camera_frames']:
    raise ValueError('Ordered unique camera keyframe times required')
if a.dot_seed is not None:
    if not 0<=a.dot_seed<=10000:raise ValueError('Dot seed outside candidate bounds')
    cfg['dots']['seed']=a.dot_seed
if a.noise_width is not None:
    if not 100<=a.noise_width<=1000:raise ValueError('Noise width outside bounded candidate profile')
    cfg['noise']['width']=a.noise_width
out.mkdir(parents=True)
for role,item in cfg['inputs'].items():
    source=(profile.parent/item['project']).resolve()
    if source.suffix.lower()!='.aep' or not source.is_file():raise ValueError('Native AEP input missing: '+role)
    actual=hashlib.sha256(source.read_bytes()).hexdigest()
    if actual!=item['sha256']:raise ValueError('Input snapshot hash mismatch: '+role)
    dest=out/'inputs'/role/'project.aep';dest.parent.mkdir(parents=True);shutil.copy2(source,dest)
    item['project']=dest.as_posix();item['asset_relinks']=[]
    for asset in item.get('assets',[]):
        original=(profile.parent/asset['path']).resolve();dst=dest.parent/'assets'/original.name
        if not original.is_file() or original.suffix.lower() not in {'.png','.jpg','.jpeg'}:raise ValueError('Explicit image asset missing')
        dst.parent.mkdir(exist_ok=True);shutil.copy2(original,dst)
        item['asset_relinks'].append(dict(original_name=asset.get('original_name',original.name),path=dst.as_posix()))
cfg.update(name='COURSE_P13_COMPOSITE',width=1920,height=1080,fps=24,duration=20,
           motion_expectation='required',camera_time_scale=a.camera_time_scale,status='candidate',
           scope='Course13 rough spatial assembly, not the fully stylized title sequence',
           variant=(a.camera_time_scale!=1 or a.dot_seed is not None or a.noise_width is not None))
(out/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
(out/'plan.json').write_text(json.dumps(dict(skill='ae-advanced-compositing',status='candidate',source=cfg['source'],
    steps=['Preserve dirty/unrelated Adobe work','Import five copied native projects','Modify only imported components',
           'Apply selective collapse and white Linear Color Key','Create nested randomized point timing and main camera',
           'Save/reopen, inspect live properties, edit and restore camera','Native render then full decode and visual/source review'],
    parameter_provenance=cfg['provenance']),indent=2),encoding='utf-8')
scripts=Path(__file__).parent
body=(scripts/'composite.jsx').read_text(encoding='utf-8')
body=body.replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body=body.replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
