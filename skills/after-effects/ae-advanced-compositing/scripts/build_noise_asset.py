"""Course15 polar extension of the bundled, lab-made editable course7 noise rig."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-polar.json')
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--offset-speed', type=float)
ap.add_argument('--height', type=float)
ap.add_argument('--count', type=int)
ap.add_argument('--seed', type=int)
a = ap.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
for key, value in [('offset_speed', a.offset_speed), ('noise_height', a.height), ('count', a.count), ('seed', a.seed)]:
    if value is not None:
        cfg[key] = value
if not 1 <= cfg['offset_speed'] <= 300 or not 20 <= cfg['noise_height'] <= 600 or not 1 <= cfg['count'] <= 20:
    raise ValueError('Candidate limits: speed1–300, height20–600, count1–20')
if cfg.get('seed') is not None and not 0 <= cfg['seed'] <= 10000:
    raise ValueError('Seed outside0–10000')
source = (a.profile.resolve().parent / cfg['input_project']).resolve()
if hashlib.sha256(source.read_bytes()).hexdigest() != cfg['input_sha256']:
    raise ValueError('Bundled input AEP SHA differs')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
target = out / 'inputs/noise.aep'
target.parent.mkdir()
shutil.copy2(source, target)
cfg['input_project'] = target.as_posix()
cfg['variant'] = any(v is not None for v in (a.offset_speed, a.height, a.count, a.seed))
(out / 'request.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
(out / 'plan.json').write_text(json.dumps(dict(
    skill='ae-advanced-compositing', branch='course15-polar', status='candidate',
    steps=['Import own noise rig and retain FN7', 'Disable inherited camera',
           'Apply final course noise dimensions and Rect to Polar',
           'Offset Turbulence exact time expression and six-layer repetition',
           'Save/reopen, edit/restore expression, inspect every frame',
           'Render with Adobe, decode and inspect against original'],
    limitations=['Exact source random identities not recovered', 'No three-material generalization',
                 'This asset is separate from unfinished P15 main assembly']), indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'noise_asset.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
