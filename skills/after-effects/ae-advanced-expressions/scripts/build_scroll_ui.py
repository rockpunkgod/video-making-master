"""Course26/27 separate original expression variants, sharing native scene plumbing."""
import argparse,json,math,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--axis',choices=['vertical','horizontal'],default='vertical');p.add_argument('--profile',type=Path);p.add_argument('--asset',type=Path);p.add_argument('--text');p.add_argument('--overshoot',action='store_true');p.add_argument('--content-start',type=float);p.add_argument('--content-end',type=float)
a=p.parse_args();home=Path(__file__).resolve().parents[1];profile=a.profile or home/'examples'/('course-scroll-'+a.axis+'.json');cfg=json.loads(profile.read_text(encoding='utf-8'));changes={}
for k in ['text','content_start','content_end']:
    if getattr(a,k) is not None:cfg[k]=getattr(a,k);changes[k]=getattr(a,k)
if cfg['axis'] not in ['vertical','horizontal'] or cfg['duration']!=6 or cfg['fps']!=30 or [cfg['width'],cfg['height']]!=[960,720]:raise ValueError('Current candidate uses native320x240, delivery3x,6seconds30fps')
if not cfg['text'].strip() or len(cfg['text'])>10000:raise ValueError('Nonempty text required')
if any(not math.isfinite(cfg[k]) or abs(cfg[k])>2000 for k in ['content_start','content_end']):raise ValueError('Finite content endpoints within candidate bounds required')
if a.overshoot:
    lo,hi=cfg['range'];cfg['samples']=[[0,lo-60],[1,lo],[2,(lo+hi)/2],[3,hi],[4,hi+60],[5,lo-60],[6,lo]];changes['overshoot']=True
if len(cfg['samples'])<2 or cfg['samples'][0][0]!=0 or cfg['samples'][-1][0]!=6 or any(len(row)!=2 or not all(math.isfinite(v) for v in row) or abs(row[1])>1000 for row in cfg['samples']):raise ValueError('Finite timed axis samples spanning0–6seconds required')
if any(cfg['samples'][i][0]>=cfg['samples'][i+1][0] for i in range(len(cfg['samples'])-1)):raise ValueError('Strictly increasing samples required')
asset=a.asset or cfg.get('asset')
if asset:
    asset=Path(asset)
    if not a.asset and not asset.is_absolute():asset=profile.resolve().parent/asset
    asset=asset.resolve()
    if not asset.is_file() or asset.suffix.lower() not in ['.png','.jpg','.jpeg']:raise ValueError('Existing caller image required')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
if asset:
    (out/'assets').mkdir();dest=out/'assets'/('content'+asset.suffix.lower());shutil.copy2(asset,dest);cfg['asset']=dest.as_posix();changes['asset_source']=str(asset)
cfg['variant']=bool(changes);cfg['overrides']=changes
for name,obj in [('request.json',cfg),('plan.json',dict(skill='ae-advanced-expressions',branch='course26-27-scroll-ui',status='candidate',steps=['Create own editable text or caller-image normalized content','Build original-direction track and knob','Vertical: lock X only; vector linear content range','Horizontal: separate2D Null; clamp visible knob; linear content range','Replay observed manual positions or explicit overshoot test','Edit/save/reopen/restore; full native equations; actual render and pixel trajectory check'],fidelity='Original formulas retained separately; own materials and inferred layout; manual replay is not source animation keys'))]:
    (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
s=home/'scripts';body=(s/'scroll_ui.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
