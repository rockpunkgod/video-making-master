"""Course25 adjustment-mask/Bulge linkage, with explicit manual-replay adaptation."""
import argparse,json,math,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--profile',type=Path,default=Path(__file__).resolve().parents[1]/'examples/course-magnifier.json');p.add_argument('--asset',type=Path);p.add_argument('--blur',type=float);p.add_argument('--bulge-height',type=float);p.add_argument('--text')
a=p.parse_args();cfg=json.loads(a.profile.read_text(encoding='utf-8'));changes={}
for key in ['blur','bulge_height','text']:
    val=getattr(a,key)
    if val is not None:cfg[key]=val;changes[key]=val
if cfg['width']!=1024 or cfg['height']!=846 or cfg['fps']!=25 or cfg['duration']!=6:raise ValueError('Current candidate uses1024x846/25fps/6s')
if not all(math.isfinite(cfg[k]) for k in ['blur','bulge_height','mask_radius','mask_feather','mask_expansion']):raise ValueError('Finite parameters required')
if not 1<=cfg['blur']<=16 or not .2<=cfg['bulge_height']<=2 or cfg['adjustment_size']!=2000:raise ValueError('Outside current candidate limits')
if not 140<=cfg['mask_radius']<=190 or not 0<=cfg['mask_feather']<=120 or not -50<=cfg['mask_expansion']<=0:raise ValueError('Mask outside candidate limits')
if cfg['font']!='KaiTi':raise ValueError('Current text branch requires actual KaiTi, no silent replacement')
if not isinstance(cfg['text'],str) or not cfg['text'].strip() or len(cfg['text'])>10000:raise ValueError('Nonempty text of at most10000 characters required')
if not all(math.isfinite(cfg[k]) for k in ['font_size','leading']) or not 20<=cfg['font_size']<=48 or not cfg['font_size']<=cfg['leading']<=60:raise ValueError('Text size/leading outside candidate bounds')
if len(cfg['bulge_radii'])!=2 or any(not math.isfinite(v) or not 40<=v<=300 for v in cfg['bulge_radii']):raise ValueError('Invalid Bulge radii')
rows=cfg['positions']
if len(rows)<2 or rows[0][0]!=0 or rows[-1][0]!=6 or any(len(row)!=3 or not all(math.isfinite(x) for x in row) for row in rows):raise ValueError('Finite timed XY samples spanning0–6s required')
if any(rows[i][0]>=rows[i+1][0] for i in range(len(rows)-1)):raise ValueError('Strictly increasing times required')
if any(not 40<=x<=980 or not 40<=y<=806 for _,x,y in rows):raise ValueError('Candidate positions could expose adjustment boundary')
asset=a.asset or cfg.get('asset')
if asset:
    asset=Path(asset)
    if not a.asset and not asset.is_absolute():asset=a.profile.resolve().parent/asset
    asset=asset.resolve()
    if not asset.is_file() or asset.suffix.lower() not in ['.png','.jpg','.jpeg']:raise ValueError('Existing caller image required')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
if asset:
    (out/'assets').mkdir();dest=out/'assets'/('content'+asset.suffix.lower());shutil.copy2(asset,dest);cfg['asset']=dest.as_posix();changes['asset']=str(asset)
cfg['variant']=bool(changes);cfg['overrides']=changes
for name,val in [('request.json',cfg),('plan.json',dict(skill='ae-advanced-expressions',branch='course25-adjustment-magnifier',status='candidate',steps=['Create original lens artwork and mask its center opening','Create editable text or normalize caller image in full-frame precomp','Apply Bulge to content and Fast Blur to oversized adjustment solid','Subtract centered feathered mask; bind both centers to lens Position','Replay observed manual positions with explicitly inferred keyframes','Edit/save/reopen/restore; native full trace, controls and real render'],fidelity='Optical mechanism follows course; movement is manual-replay adaptation, no claim of source animation keys'))]:
    (out/name).write_text(json.dumps(val,ensure_ascii=False,indent=2),encoding='utf-8')
s=Path(__file__).parent;body=(s/'magnifier.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
