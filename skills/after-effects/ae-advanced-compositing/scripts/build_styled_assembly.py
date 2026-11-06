"""Build course16 assembly from packaged self-made native components."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/course-styled-assembly.json')
p.add_argument('--out', type=Path, required=True)
p.add_argument('--polar-glow-intensity', type=float)
a = p.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if (cfg['name'], cfg['width'], cfg['height'], cfg['fps'], cfg['duration']) != ('COURSE_P16_STYLED_ASSEMBLY',1920,1080,24,20):
    raise ValueError('This candidate currently tests the course20s/1920x1080/24fps assembly contract only')
if a.polar_glow_intensity is not None:
    if not 0 <= a.polar_glow_intensity <= 2:
        raise ValueError('Candidate intensity range 0–2')
    cfg['polar_glow_intensity'] = a.polar_glow_intensity
cfg['variant'] = a.polar_glow_intensity is not None
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
plan = dict(skill='ae-advanced-compositing', branch='course16-styled-assembly', status='candidate',
            steps=['Import own assembly, accepted core and styled noise',
                   'Apply native polar palette, black key, Screen and Find Edges',
                   'Style radial and link opacity to core', 'Edit/reopen/restore Glow',
                   'Inspect native frame traces, render and compare'], provenance=cfg['provenance'])
for name, value in [('request.json', cfg), ('plan.json', plan)]:
    (out / name).write_text(json.dumps(value, indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts / 'styled_assembly.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts / 'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out / 'build.jsx').write_text(body, encoding='utf-8')
print(out / 'build.jsx')
