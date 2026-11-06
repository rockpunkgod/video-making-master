"""Prepare an explicitly inferred reconstruction of the course's 25s ending.

The teacher changed this scene offscreen. This is a candidate fitting exercise,
not a recovered original camera rig or an accepted course baseline.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--profile', required=True, type=Path)
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if (cfg['name'], cfg['width'], cfg['height'], cfg['fps'], cfg['duration']) != ('COURSE_FINAL_RECONSTRUCTION', 1920, 1080, 24, 25):
    raise ValueError('Only the explicit 25-second candidate contract is supported')
src = (a.profile.resolve().parent / cfg['input']['project']).resolve()
if src.suffix.lower() != '.aep' or hashlib.sha256(src.read_bytes()).hexdigest() != cfg['input']['sha256']:
    raise ValueError('Native input differs from reviewed source')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
(out / 'inputs').mkdir()
shutil.copy2(src, out / 'inputs/main.aep')
cfg['input']['project'] = (out / 'inputs/main.aep').as_posix()
for name, value in [('request.json', cfg), ('plan.json', dict(
    skill='ae-advanced-compositing', branch='course-final-reconstruction', status='candidate',
    course_fidelity='unverified; offscreen camera/labels reconstructed from reference',
    steps=['Retain editable P13–17 components', 'Rebuild 25s timing and grouped labels',
           'Parent camera to drift null', 'Native edit/reopen/restore and preview',
           'Compare before any course-fidelity acceptance'],
    limitations=cfg['provenance']))]:
    (out / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'final_assembly.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
