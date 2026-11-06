"""Import self-made editable course components; never use tutorial footage as layers."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-assembly.json')
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--background-blend', type=float)
a = ap.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if a.background_blend is not None:
    if not 50 <= a.background_blend <= 200:
        raise ValueError('Tested candidate range: background blend50–200')
    cfg['background_blend'] = a.background_blend
cfg['variant'] = a.background_blend is not None
sources = {}
for role, spec in cfg['inputs'].items():
    source = (a.profile.resolve().parent / spec['project']).resolve()
    if source.suffix.lower() != '.aep' or hashlib.sha256(source.read_bytes()).hexdigest() != spec['sha256']:
        raise ValueError('Native input differs: ' + role)
    sources[role] = source
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
for role, spec in cfg['inputs'].items():
    dest = out / 'inputs' / role / 'project.aep'
    dest.parent.mkdir(parents=True)
    shutil.copy2(sources[role], dest)
    spec['project'] = dest.as_posix()
(out / 'request.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
(out / 'plan.json').write_text(json.dumps(dict(
    skill='ae-advanced-compositing', branch='course15-assembly', status='candidate',
    steps=['Import self-made native components', 'Preserve course13 camera',
           'Apply course15 final visible depths and estimated starts',
           'Add native gradient/Curves background and radial fade',
           'Edit/save/reopen/restore gradient point',
           'Native checkpoints, Adobe render, decode, original comparison'],
    provenance=cfg['provenance']), indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'assembly.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
