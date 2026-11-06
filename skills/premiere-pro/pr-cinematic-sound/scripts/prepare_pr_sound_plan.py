"""Copy caller-provided audiovisual inputs and derive an installed native preset."""
import argparse,hashlib,json,shutil
from pathlib import Path
from pr_presets import sequence_preset

ap=argparse.ArgumentParser();ap.add_argument('plan',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--sequence-base',type=Path,required=True);a=ap.parse_args()
plan=json.loads(a.plan.read_text(encoding='utf-8'));out=a.out.resolve()
if out.exists():raise FileExistsError('Choose a fresh case directory')
resolved=[]
for c in [*plan['picture_clips'],*plan['audio_clips']]:
    source=Path(c['path']);source=source if source.is_absolute() else a.plan.resolve().parent/source
    if not source.is_file():raise FileNotFoundError(source)
    resolved.append((c,source.resolve()))
if not a.sequence_base.is_file():raise FileNotFoundError('Caller must supply an installed Adobe sequence preset')
(out/'inputs').mkdir(parents=True)
copied={};records=[]
for c,source in resolved:
    if source not in copied:
        dest=out/'inputs'/f'asset-{len(copied):02}{source.suffix}';shutil.copy2(source,dest);copied[source]=dest
        records.append({'file':dest.relative_to(out).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    c['path']=str(copied[source])
plan['variant']=out.name
sequence_preset(a.sequence_base,out/'sequence.sqpreset',plan['width'],plan['height'],plan['fps'])
(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'assets.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(out)
