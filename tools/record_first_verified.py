"""Record a reviewed milestone only when native/render evidence covers all required cases."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];suite=ROOT/'samples/runs/suite-20261106-091450';review=ROOT/'evaluations/motion-suite-001'
results=json.loads((suite/'results.json').read_text(encoding='utf-8'));audits=json.loads((review/'native-editability.json').read_text(encoding='utf-8-sig'))
expected={'square-baseline','triangle-variation','hexagon-portrait','asset-geometry','asset-typography','asset-texture'}
assert {r['build']['comp'] for r in results}==expected
assert {a['name'] for a in audits}==expected and all(a['status']=='passed' for a in audits)
assert (review/'visual-review.md').is_file()
artifacts=[]
for r in results:
    p=ROOT/r['run'];receipt=json.loads((p/'receipt.json').read_text(encoding='utf-8-sig'));quality=json.loads((p/'quality.json').read_text(encoding='utf-8'))
    assert receipt['status']=='built' and receipt['project_reopened'] and not receipt['expression_errors']
    assert receipt['max_rotation_error']<=0.001 and receipt['max_z_error']<=0.001
    assert quality['status']=='passed' and all(quality['checks'].values())
    if receipt['comp']=='square-baseline':assert set(receipt['shape_vertices'])=={4}
    if receipt['comp']=='triangle-variation':assert set(receipt['shape_vertices'])=={3}
    if receipt['comp']=='hexagon-portrait':assert set(receipt['shape_vertices'])=={6}
    assert (p/'project.aep').is_file() and (p/'final.mp4').is_file()
    assert hashlib.sha256((p/'final.mp4').read_bytes()).hexdigest()==quality['sha256']
    artifacts.append({'case':receipt['comp'],'project':(p/'project.aep').relative_to(ROOT).as_posix(),'video':(p/'final.mp4').relative_to(ROOT).as_posix(),'quality':(p/'quality.json').relative_to(ROOT).as_posix(),'video_sha256':quality['sha256']})
report={'skill':'ae-procedural-motion','version':'0.2.0','status':'verified','verified':True,'host':'After Effects 26.0x67 Windows',
        'scope':'3D delayed procedural contour arrays and imported still-image arrays; no tracking, projection reconstruction, sound or PR capability',
        'tests':{'basic_reproduction':{'status':'passed','case':'square-baseline','comparison':'mechanism and visual structure, not pixel-identical'},
                 'parameter_variation':{'status':'passed','cases':['triangle-variation','hexagon-portrait']},
                 'cross_asset_generalization':{'status':'passed','cases':['asset-geometry','asset-typography','asset-texture']},
                 'visual_and_technical':{'status':'passed','native_audit':'evaluations/motion-suite-001/native-editability.json','visual_review':'evaluations/motion-suite-001/visual-review.md','audio_sync':'not_applicable'}},
        'artifacts':artifacts,'limitations':['Long text can overlap; this is not verified kinetic typography','Exact tutorial easing parameters were not established','Video input, other AE versions and arbitrary plugins are untested'],
        'superseded_failures':['square-001 startup blocked','square-002 wrong camera property name','square-004 clean-project guard','square-005 and first suite nested conditional shape error'],
        'template_sha256':hashlib.sha256((ROOT/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_bytes()).hexdigest()}
(ROOT/'evaluations/first-skill.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
registry=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'));skill=registry['skills'][0]
skill.update(version='0.2.0',status='verified',execution_status='passed',blockers=[],verified_artifacts=artifacts,verified_host='After Effects 26.0x67 Windows')
(ROOT/'registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False),encoding='utf-8')
print('Verified first bounded skill against 6 native projects, renders, parameter edits and visual review. Overall goal remains incomplete.')
