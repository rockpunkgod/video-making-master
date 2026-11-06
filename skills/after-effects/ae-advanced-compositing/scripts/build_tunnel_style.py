"""Apply course17 tunnel continuation to a packaged own course16 assembly."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1]/'examples/course-tunnel-style.json')
p.add_argument('--out', required=True, type=Path)
p.add_argument('--rotation-speed', type=float)
a = p.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
if (cfg['name'], cfg['width'], cfg['height'], cfg['fps'], cfg['duration']) != ('COURSE_P17_TUNNEL_STYLE',1920,1080,24,20):
    raise ValueError('Candidate supports this course assembly contract only')
if a.rotation_speed is not None:
    if not 0 <= a.rotation_speed <= 60:
        raise ValueError('Candidate input range0..60 degrees/sec')
    cfg['rotation_speed'] = a.rotation_speed
cfg['variant'] = a.rotation_speed is not None
src = (a.profile.resolve().parent/cfg['input']['project']).resolve()
if src.suffix.lower() != '.aep' or hashlib.sha256(src.read_bytes()).hexdigest() != cfg['input']['sha256']:
    raise ValueError('Packaged native input differs')
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
(out/'inputs').mkdir()
shutil.copy2(src, out/'inputs/main.aep')
cfg['input']['project'] = (out/'inputs/main.aep').as_posix()
plan = dict(skill='ae-advanced-compositing', branch='course17-tunnel', status='candidate',
            steps=['Import own saved course16 assembly', 'Disable first static contour; shift null and enlarge spacing',
                   'Add outer time*speed+value rotation and opacity keys', 'Edit/reopen/restore', 'Native render and frame inspection'],
            provenance=cfg['provenance'])
for name, data in [('request.json',cfg), ('plan.json',plan)]:
    (out/name).write_text(json.dumps(data, indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts/'tunnel_style.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8')
print(out/'build.jsx')
