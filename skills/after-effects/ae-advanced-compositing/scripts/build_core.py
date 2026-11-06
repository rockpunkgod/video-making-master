"""Course16 dynamic shell from the self-made course11 editable equation rig."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-core.json')
ap.add_argument('--out', required=True, type=Path)
ap.add_argument('--count', type=int)
ap.add_argument('--speed', type=float)
a = ap.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if a.count is not None:
    cfg['count'] = a.count
if a.speed is not None:
    cfg['speed'] = a.speed
if not 20 <= cfg['count'] <= 176 or not 1 <= cfg['speed'] <= 150:
    raise ValueError('Candidate bounds count20–176 / speed1–150')
source = (a.profile.resolve().parent / cfg['input_project']).resolve()
if hashlib.sha256(source.read_bytes()).hexdigest() != cfg['input_sha256']:
    raise ValueError('Own native rig differs')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
dest = out / 'inputs/core.aep'
dest.parent.mkdir()
shutil.copy2(source, dest)
cfg['input_project'] = dest.as_posix()
cfg['variant'] = a.count is not None or a.speed is not None
(out / 'request.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
(out / 'plan.json').write_text(json.dumps(dict(
    skill='ae-advanced-compositing', branch='course16-core', status='candidate',
    steps=['Import own course11 rig', 'Gradient stroke plus animated alpha matte',
           'Animate Phase, Z increment and Radius', 'Tritone then Vector Blur then Lens',
           'Native per-layer per-frame equation checks', 'Edit/reopen/restore Phase increment',
           'Actual Adobe render and reference comparison'], provenance=cfg['provenance']), indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'core.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
