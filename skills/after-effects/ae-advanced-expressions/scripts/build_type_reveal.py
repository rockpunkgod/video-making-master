"""Course14 odd/even position selector with randomized opacity range reveal.

Final graph handle values are viewport estimates, explicitly not exact source keys.
"""
import argparse
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--out',type=Path,required=True)
p.add_argument('--text',default='SUBPRIME')
p.add_argument('--font-size',type=float,default=160)
p.add_argument('--x',type=float,default=258)
p.add_argument('--y',type=float,default=420)
p.add_argument('--offset-y',type=float,default=-79)
p.add_argument('--reveal-frames',type=int,default=29)
p.add_argument('--seed',type=int,default=0)
a=p.parse_args()
if not 1<=len(a.text)<=24 or not a.text.isascii() or not all(c.isalnum() or c==' ' for c in a.text) or a.text.isspace():
    raise ValueError('Bounded candidate supports 1–24 ASCII letters/digits/spaces; no font fallback')
if not 30<=a.font_size<=180 or not 8<=a.reveal_frames<=90 or not -150<=a.offset_y<=-20 or not 0<=a.seed<=10000:
    raise ValueError('Outside tested candidate input bounds')
if not 0<=a.x<=1100 or not 150<=a.y<=550:raise ValueError('Position outside candidate bounds')
out=a.out.resolve()
if out.exists():raise FileExistsError('Use a fresh output directory')
out.mkdir(parents=True)
cfg=dict(name='COURSE_P14_TYPE_REVEAL',width=1280,height=720,fps=30,duration=151/30,
         text=a.text,font_size=a.font_size,position=[a.x,a.y],offset_y=a.offset_y,
         reveal_frames=a.reveal_frames,random_seed=a.seed,animation='type-reveal',motion_expectation='required',
         course_observed='DM Sans Bold160; baseline shift4; Position258/420; odd:-100/even:100; Opacity0; randomized range End100 to0',
         timing_evidence='05:10 cursor00:00:00:29 overlaps both final keys; first keys at0; comp panel05:01 at30fps',
         inferred='Position influences14.5/36.2 estimated from graph; End9/45 fitted against final06:00 speed curve using native valueAtTime derivatives; seed0 is native default, source seed unread',
         fidelity='candidate; final handle estimates are not exact source keyframe values')
(out/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
(out/'plan.json').write_text(json.dumps(dict(skill='ae-advanced-expressions',branch='course14-type-reveal',
    status='candidate',steps=['Check existing native course font','Build editable position and opacity animators',
    'Save and reopen','Change text and reopen then restore','Render native video','Measure actual character motion and settled hold'],
    source='https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=14',
    review='Show original06:03–06:08 playback and comparison; exact frame synchronization remains unverified'),indent=2),encoding='utf-8')
scripts=Path(__file__).parent
body=(scripts/'type_reveal.jsx').read_text(encoding='utf-8')
body=body.replace('__ENCODER__',(scripts/'json_encode_adobe.jsx').read_text(encoding='utf-8'))
body=body.replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8')
print(out/'build.jsx')
