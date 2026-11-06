"""Create the course15 spatial streak candidate from the bundled native noise rig."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-streaks.json')
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--seed', type=int)
ap.add_argument('--count', type=int)
ap.add_argument('--scale', type=float)
ap.add_argument('--depth', type=float)
a = ap.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
for key, value in [('seed', a.seed), ('count', a.count), ('scale', a.scale), ('depth', a.depth)]:
    if value is not None:
        cfg[key] = value
if not 0 <= cfg['seed'] <= 10000 or not 1 <= cfg['count'] <= 30 or not 100 <= cfg['scale'] <= 700 or not 100 <= cfg['depth'] <= 5000:
    raise ValueError('Candidate bounds: seed0–10000, count1–30, scale100–700, depth100–5000')
source = (a.profile.resolve().parent / cfg['input_project']).resolve()
if hashlib.sha256(source.read_bytes()).hexdigest() != cfg['input_sha256']:
    raise ValueError('Own input AEP SHA differs')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
target = out / 'inputs/noise.aep'
target.parent.mkdir()
shutil.copy2(source, target)
cfg['input_project'] = target.as_posix()
cfg['variant'] = any(v is not None for v in (a.seed, a.count, a.scale, a.depth))
(out / 'request.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
(out / 'plan.json').write_text(json.dumps(dict(
    skill='ae-advanced-compositing', branch='course15-streaks', status='candidate',
    steps=['Reuse own noise rig', 'Apply observed noise width/height',
           'Use prior-course random Position and final zero drift/Z bounds',
           'Reconstruct visible final scale and retain14 noise layers',
           'Native seed edit/save/reopen/restore and per-frame checks', 'Adobe render and original comparison'],
    inferred=['Base Position0 inferred from copied prior-course Position property',
              'Scale503 visible; replacing inherited scale expression with constant is reconstruction, not observed source code',
              '14 noise layers inferred from16-layer timeline including Camera1 and controls',
              'Exact noise random identities unproven']), indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'streaks.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
