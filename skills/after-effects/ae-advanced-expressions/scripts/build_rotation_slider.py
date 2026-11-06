"""Prepare course28 original conditional/rotation method with explicit inferred artwork/camera."""
import argparse,json,math
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--out',type=Path,required=True)
ap.add_argument('--labels',default='aewest')
ap.add_argument('--end-frame',type=int,default=41)
ap.add_argument('--fixture',choices=['circles','hexagons','tags','stars'],default='circles')
ap.add_argument('--repair-boundary',action='store_true')
ap.add_argument('--boundary-demo',action='store_true')
a=ap.parse_args()
if len(a.labels)!=6 or not a.labels.isascii() or not a.labels.isalnum():raise ValueError('Current calibrated fixture supports six ASCII letters/digits')
if not 12<=a.end_frame<=80:raise ValueError('End frame must be12–80 within90frame example')
cfg=dict(name='COURSE_ROTATION_SLIDER',animation='rotation-slider',motion_expectation='required',width=960,height=720,native_width=320,native_height=240,fps=30,duration=3,labels=a.labels,fixture=a.fixture,end_frame=a.end_frame,repair_boundary=a.repair_boundary,keys=[[0,[15.8,290.1]],[a.end_frame/30,[334.8,292.1]]],camera=dict(position=[160,500,-500],point_of_interest=[160,100,0],zoom=600),artwork=dict(position=[330,50,0],anchor=[400,0,0],size=[400,400],radius=25),inferred=['Native320x240 from viewport;30fps from timeline','Final41frame endpoint derived from five rounded UI positions, not direct key-time readout','Own editable precomposition replaces pre-existing Illustrator vector artwork; camera and artwork geometry are inferred','Motion blur180degree shutter is an implementation choice, original shutter unread'],variant=a.labels!='aewest' or a.end_frame!=41 or a.fixture!='circles' or a.repair_boundary)
geometry=json.loads((Path(__file__).resolve().parents[1]/'examples/course-rotation-geometry.json').read_text(encoding='utf-8'))
cfg['boundary_demo']=a.boundary_demo;cfg['blur_control_frame']=5 if a.boundary_demo else 20
if a.boundary_demo:cfg['keys']=[[0,[60,290.1]],[.5,[300,292.1]],[1.5,[300,292.1]],[2,[334.8,292.1]]];cfg['variant']=True
cfg['camera']=geometry['camera'];cfg['artwork']=geometry['artwork'];cfg['screen_observations']=geometry['screen_observations'];cfg['projection_tolerance']=geometry['native_projection_tolerance']
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
for name,obj in [('request.json',cfg),('plan.json',dict(status='candidate',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=28',steps=['Create own editable vector fixture','Original2D Null drives exact conditional knob position and3D layer ZRotation','Use two source-value keys and derived final41frame timing','Native boundary samples,90frame traces, edit/save/reopen/restore','Native blur on/off stills and actual render'],course_fidelity='Exact original expressions; own artwork and inferred camera must pass visual review separately',repair_boundary=a.repair_boundary))]:
    (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=Path(__file__).resolve().parent
body=(s/'rotation_slider.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
