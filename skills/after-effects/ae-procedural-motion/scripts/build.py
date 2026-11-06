"""Validate a declarative request and emit a standalone ExtendScript; does not claim AE ran."""
import argparse
import json
import math
import re
from pathlib import Path

DEFAULTS = dict(name='procedural-tunnel',width=1080,height=1080,fps=30,duration=5,
                count=24,delay_frames=2,z_spacing=180,size=840,stroke_width=5,
                color=[1,0.06,0.18],rotation_degrees=160,camera_zoom=1100,shape='square',asset=None)

def validate(raw):
    unknown=set(raw)-set(DEFAULTS)
    if unknown: raise ValueError(f'Unknown parameters: {sorted(unknown)}')
    cfg={**DEFAULTS,**raw}
    if not isinstance(cfg['name'],str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}',cfg['name']):
        raise ValueError('name must contain 1-64 ASCII letters, digits, underscores or hyphens')
    ranges={'width':(64,4096),'height':(64,4096),'fps':(1,120),'duration':(1,60),'count':(1,100),
            'delay_frames':(0,30),'z_spacing':(1,2000),'size':(10,6000),
            'stroke_width':(0.1,100),'rotation_degrees':(-2000,2000),'camera_zoom':(100,10000)}
    for key,(lo,hi) in ranges.items():
        value=cfg[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not lo<=value<=hi:
            raise ValueError(f'{key} must be a finite number in [{lo}, {hi}]')
    for key in ['width','height','count']:
        if int(cfg[key])!=cfg[key]: raise ValueError(f'{key} must be an integer')
        cfg[key]=int(cfg[key])
    if abs(cfg['duration']*cfg['fps']-round(cfg['duration']*cfg['fps']))>1e-6:
        raise ValueError('duration * fps must be an integer frame count')
    if cfg['delay_frames']*(cfg['count']-1)/cfg['fps']>=cfg['duration']-0.25:
        raise ValueError('last element starts too late; reduce count/delay or increase duration')
    color=cfg['color']
    if not isinstance(color,list) or len(color)!=3 or any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or not 0<=x<=1 for x in color):
        raise ValueError('color must be three finite RGB values in [0,1]')
    if cfg['shape'] not in ['square','triangle','hexagon']: raise ValueError('unsupported shape')
    if cfg['asset'] is not None:
        if not isinstance(cfg['asset'],str) or not Path(cfg['asset']).is_file(): raise ValueError('asset must be an existing file')
        cfg['asset']=Path(cfg['asset']).resolve().as_posix()
    return cfg

def build(raw,out):
    cfg=validate(raw);out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    # Refuse reuse so old receipts/renders cannot be mistaken for a new execution.
    if (out/'build.jsx').exists() or (out/'project.aep').exists():
        raise FileExistsError('Use a fresh output directory for every run')
    template=Path(__file__).with_name('template.jsx').read_text(encoding='utf-8')
    script=template.replace('__CONFIG__',json.dumps(cfg,ensure_ascii=True)).replace('__OUTPUT__',json.dumps(out.as_posix(),ensure_ascii=True))
    (out/'build.jsx').write_text(script,encoding='utf-8')
    (out/'request.json').write_text(json.dumps(cfg,indent=2,ensure_ascii=False),encoding='utf-8')
    return out/'build.jsx'

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('config',type=Path);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();print(build(json.loads(a.config.read_text(encoding='utf-8-sig')),a.out))
