"""Course23 width-normalized spring: native artwork and original expression logic."""
import argparse
import json
import math
import hashlib
import shutil
import struct
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1]/'examples/course-spring-connector.json')
p.add_argument('--out', type=Path, required=True)
p.add_argument('--graphic', choices=['coil', 'zigzag', 'ribbon', 'chain'])
p.add_argument('--asset', type=Path, help='Caller PNG:64–256px wide,32px high, transparent, horizontal endpoints at mid-height')
p.add_argument('--asset-width', type=int)
p.add_argument('--design-width', type=int)
p.add_argument('--angular-rate', type=float)
p.add_argument('--amplitude', type=float)
p.add_argument('--decay-end', type=float)
p.add_argument('--duration', type=float)
p.add_argument('--mode', choices=['linear_decay', 'constant'])
p.add_argument('--b-anchor-x', type=float)
a = p.parse_args()
cfg = json.loads(a.profile.read_text(encoding='utf-8'))
changes = {}
external = None
asset_argument = a.asset or cfg.get('external_png')
if asset_argument:
    if a.graphic or a.asset_width is not None:
        raise ValueError('--asset uses actual intrinsic width; omit --graphic/--asset-width')
    external = Path(asset_argument)
    if a.asset:
        external = external.resolve()
    else:
        external = (a.profile.resolve().parent/external).resolve() if not external.is_absolute() else external.resolve()
    header = external.read_bytes()[:24]
    if external.suffix.lower()!='.png' or header[:8]!=b'\x89PNG\r\n\x1a\n' or len(header)!=24:
        raise ValueError('A real PNG is required')
    width,height=struct.unpack('>II',header[16:24])
    if height!=32:
        raise ValueError('Current external PNG adapter requires32px height; horizontal attachment points at y16')
    cfg['asset_width']=width
    cfg['graphic']='external_png'
    changes['external_png_sha256']=hashlib.sha256(external.read_bytes()).hexdigest()
for key in ['graphic', 'asset_width', 'design_width', 'angular_rate', 'amplitude', 'decay_end', 'duration', 'mode']:
    value = getattr(a, key)
    if value is not None:
        changes[key] = value
        cfg[key] = value
if a.b_anchor_x is not None:
    cfg['b_anchor']=[a.b_anchor_x,20]
    changes['b_anchor']=cfg['b_anchor']
if not 0<=cfg.get('b_anchor',[0,20])[0]<=20:
    raise ValueError('B anchor must lie in the left half of the40px endpoint artwork')
if (not external and cfg['graphic'] not in {'coil', 'zigzag', 'ribbon', 'chain'}) or cfg['mode'] not in {'linear_decay', 'constant'}:
    raise ValueError('Unsupported connector or envelope')
if not all(math.isfinite(cfg[k]) for k in ['angular_rate', 'amplitude', 'decay_end', 'duration']):
    raise ValueError('Finite numerical parameters required')
if not (64 <= cfg['asset_width'] <= 256 and 260 <= cfg['design_width'] <= 640 and
        0 < cfg['angular_rate'] <= 18 and 0 < cfg['amplitude'] < cfg['asset_width'] and
        2 <= cfg['duration'] <= 12 and 0 < cfg['decay_end'] <= cfg['duration']):
    raise ValueError('Outside candidate bounds; amplitude must remain below intrinsic connector width')
if cfg['a_position'][0] + cfg['asset_width'] + cfg['amplitude'] + 40 > cfg['design_width']:
    raise ValueError('B artwork may leave frame: increase --design-width or reduce amplitude')
cfg.update(width=cfg['design_width']*4, height=400, fps=30, variant=bool(changes), overrides=changes)
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=False)
if external:
    (out/'assets').mkdir()
    shutil.copy2(external,out/'assets/connector.png')
    cfg['external_png']=(out/'assets/connector.png').as_posix()
    cfg['external_png_source']=str(external)
for name, data in [('request.json', cfg), ('plan.json', dict(
    skill='ae-advanced-expressions', branch='course23-horizontal-spring', status='candidate',
    steps=[('Copy caller PNG and read its intrinsic width' if external else 'Create self-authored editable connector artwork'), ('Import caller alpha PNG' if external else 'Export/import its actual alpha PNG'),
           'Bind spring position and normalize scale by intrinsic width',
           'Apply course sine and linear amplitude envelope to B',
           'Edit A/save/reopen/restore, inspect every native frame', 'Render and measure actual B motion'],
    source=cfg['source'], fidelity='Course expressions preserved; own artwork/layout inferred; review required'))]:
    (out/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
scripts = Path(__file__).parent
body = (scripts/'spring_connector.jsx').read_text(encoding='utf-8')
body = body.replace('__ENCODER__', (scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body = body.replace('__CONFIG__', json.dumps(cfg)).replace('__OUTPUT__', json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body, encoding='utf-8')
print(out/'build.jsx')
