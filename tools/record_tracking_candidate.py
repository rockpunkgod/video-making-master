import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];run=ROOT/'samples/tracking-fixture-001'
native=json.loads((run/'native-camera-result.json').read_text(encoding='utf-8-sig'))
assert native['camera_count']==1 and native['position_key_count']==96 and native['status']=='camera_created_validation_pending'
record={'skill':'ae-camera-tracking','status':'candidate','verified':False,'native_result':native,
        'input':'samples/tracking-fixture-001/source.mp4','input_scene':'samples/tracking-fixture-001/source-scene.aep','project':'samples/tracking-fixture-001/tracking-attempt.aep',
        'evidence':['samples/tracking-fixture-001/tracker-current-state.txt','samples/tracking-fixture-001/native-camera-result.json'],
        'tests':{'native_solve':'passed_one_input','camera_creation':'passed_one_input','basic_composite':'not_run','parameter_variation':'not_run','three_input_generalization':'not_run','visual_drift_check':'not_run'},
        'next_actions':['Create a tracked reference plane from actual native track points','Composite an independent overlay and render','Measure plane drift across the shot','Repeat with two distinct inputs and parameter changes'],
        'known_limits':['Native camera exists but scene/composite accuracy is not yet validated','Custom tracker values are exposed only through dynamic property names','GUI create-camera action worked; track-point context-menu action is unresolved']}
(ROOT/'evaluations/tracking-candidate.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
registry=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'))
new={'name':'ae-camera-tracking','version':'0.1.0','status':'candidate','execution_status':'partial_native_success','path':'skills/after-effects/ae-camera-tracking','dependencies':['Adobe After Effects native 3D Camera Tracker','FFmpeg','Python 3.10+'],'plugins':[], 'scenarios':['solve a camera from a rigid scene video','tracked 3D compositing'],'sources':[{'id':'wiISCTB4s1Y'}],'evidence':'evaluations/tracking-candidate.json','verified_artifacts':[]}
registry['skills']=[s for s in registry['skills'] if s['name']!=new['name']]+[new]
(ROOT/'registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False),encoding='utf-8')
print('Tracking candidate recorded; one native solve/camera does not satisfy verification.')
