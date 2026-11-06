"""Reuse the lab-authored native Curves template; never replace its course effect chain."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-radial.json')
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--speed', type=float)
ap.add_argument('--seed', type=int)
ap.add_argument('--duration', type=float)
a = ap.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
for key, value in [('speed', a.speed), ('seed', a.seed), ('duration', a.duration)]:
    if value is not None:
        cfg[key] = value
if not 1 <= cfg['speed'] <= 150 or not 1 <= cfg['duration'] <= 20 or not 0 <= cfg['seed'] <= 10000:
    raise ValueError('Candidate limits: speed 1–150, duration 1–20, seed 0–10000')
if abs(cfg['duration'] * cfg['fps'] - round(cfg['duration'] * cfg['fps'])) > 1e-6:
    raise ValueError('Duration must contain whole frames')
source = (a.profile.resolve().parent / cfg['template']).resolve()
if hashlib.sha256(source.read_bytes()).hexdigest() != cfg['template_sha256']:
    raise ValueError('Native template SHA differs')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
dest = out / 'inputs/radial-template.aep'
dest.parent.mkdir()
shutil.copy2(source, dest)
cfg['template'] = dest.as_posix()
cfg['variant'] = any(x is not None for x in (a.speed, a.seed, a.duration))
(out / 'request.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
(out / 'plan.json').write_text(json.dumps(dict(
    skill='ae-advanced-compositing', branch='course-p15-radial', status='candidate',
    steps=['Import own editable template with native RGB channel curves',
           'Change explicitly requested evolution parameters', 'Save/reopen and edit/restore native controller',
           'Render through Adobe', 'Decode every frame and compare against the course'],
    limitations=['Curve points inferred from source UI', 'No three-material generalization yet',
                 'P15 polar/streak/main assembly not provided by this branch']), indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'radial.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
