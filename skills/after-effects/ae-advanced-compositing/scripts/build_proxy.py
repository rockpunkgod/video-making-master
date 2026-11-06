"""Prepare native course18 high-quality alpha proxies without flattening collapsed3D uses."""
import argparse,hashlib,json,shutil
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--profile',type=Path,default=Path(__file__).resolve().parents[1]/'examples/course-proxy-lines.json')
p.add_argument('--out',type=Path,required=True)
p.add_argument('--final-policy',choices=['proxies','originals'])
a=p.parse_args();cfg=json.loads(a.profile.read_text(encoding='utf-8'))
if cfg['name']!='COURSE_P18_PROXY_DEMO' or not 0<cfg['duration']<=30 or cfg['fps']<=0:raise ValueError('Invalid bounded proxy request')
cfg['final_policy']=a.final_policy or cfg['final_policy'];cfg['variant']=a.final_policy is not None
sources={}
for role,spec in cfg['inputs'].items():
    src=(a.profile.resolve().parent/spec['project']).resolve()
    if src.suffix.lower()!='.aep' or hashlib.sha256(src.read_bytes()).hexdigest()!=spec['sha256']:raise ValueError('Changed native input: '+role)
    sources[role]=src
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
for role,spec in cfg['inputs'].items():
    dest=out/'inputs'/role/'project.aep';dest.parent.mkdir(parents=True);shutil.copy2(sources[role],dest);spec['project']=dest.as_posix()
(out/'assets').mkdir()
for name,value in [('request.json',cfg),('plan.json',dict(skill='ae-advanced-compositing',branch='course18-proxies',status='candidate',steps=['Audit collapsed uses before reducing project','Render native Best/Full ProRes4444 with alpha','Assign proxy, edit/reopen/toggle/restore original','Compare native alpha on dark/white and render declared final policy'],provenance=cfg['provenance']))]:
    (out/name).write_text(json.dumps(value,indent=2),encoding='utf-8')
scripts=Path(__file__).parent
for source,dest in [('proxy_prepare.jsx','build.jsx'),('proxy_attach.jsx','attach.jsx')]:
    body=(scripts/source).read_text(encoding='utf-8').replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8'))
    body=body.replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
    (out/dest).write_text(body,encoding='utf-8')
print(out/'build.jsx')
