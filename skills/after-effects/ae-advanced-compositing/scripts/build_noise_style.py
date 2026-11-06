"""Package own native inputs and build the course16 Colorama/Glow component."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-noise-style.json')
p.add_argument('--out', type=Path, required=True)
p.add_argument('--glow-intensity', type=float)
a = p.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if a.glow_intensity is not None:
    if not 0 <= a.glow_intensity <= 2:
        raise ValueError('Candidate intensity range 0–2')
    cfg['glow_intensity'] = a.glow_intensity
cfg['variant'] = a.glow_intensity is not None
sources = {}
for role, spec in cfg['inputs'].items():
    src = (a.profile.resolve().parent / spec['project']).resolve()
    if src.suffix.lower() != '.aep' or hashlib.sha256(src.read_bytes()).hexdigest() != spec['sha256']:
        raise ValueError('Native input differs: ' + role)
    sources[role] = src
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
for role, spec in cfg['inputs'].items():
    dest = out / 'inputs' / role / 'project.aep'
    dest.parent.mkdir(parents=True)
    shutil.copy2(sources[role], dest)
    spec['project'] = dest.as_posix()
for name, value in [('request.json', cfg), ('plan.json', dict(skill='ae-advanced-compositing', branch='course16-noise-style', status='candidate', steps=['Import own editable noise and native palette', 'Retain camera and course styling', 'Reopen and edit/restore native Glow', 'Check every frame fade and expressions', 'Render in Adobe and compare native checkpoints'], provenance=cfg['provenance']))]:
    (out / name).write_text(json.dumps(value, indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'noise_style.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
