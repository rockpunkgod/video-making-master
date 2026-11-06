"""Small request-to-plan-to-Adobe entry point for capabilities actually in the registry."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from run_ae import execute
from render_ae import render

ROOT=Path(__file__).resolve().parents[1]

def select(brief,registry):
    words=brief.lower()
    unsupported=['mocha','跟踪','tracking','projection','投影重建','调色','声音设计','sound design','spring','弹簧']
    if any(w in words for w in unsupported):raise ValueError('This unattended CLI covers procedural arrays only. Read the registry and matching SKILL for agent-driven workflows such as observed camera-tracker GUI actions; other capabilities still require learning/verification.')
    matches=[]
    for skill in registry['skills']:
        if skill['status']=='verified' and skill['name']=='ae-procedural-motion' and any(w in words for w in ['隧道','延迟阵列','轮廓阵列','逐层淡入','程序化重复','tunnel','delayed array','contour array','step repetition']):matches.append(skill)
    if len(matches)!=1:raise ValueError('No unambiguous verified skill matches the brief; an agent must clarify or distill the missing capability')
    return matches[0]

def make(request,out,ae,aerender):
    if set(request)-{'brief','parameters'}:raise ValueError('Only brief and parameters are supported')
    brief=request.get('brief')
    if not isinstance(brief,str) or not brief.strip():raise ValueError('brief is required')
    registry=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'));skill=select(brief,registry)
    parameters=request.get('parameters',{})
    if not isinstance(parameters,dict) or set(parameters)-{'stage','delay_frames','asset'}:raise ValueError('The course-verified profile accepts stage, delay_frames and optional PNG asset. Older custom framing/curves belong to the explicit unverified variant; do not silently substitute them.')
    stage=parameters.get('stage','opacity' if parameters.get('asset') else 'trim-final');delay=parameters.get('delay_frames',2)
    out=Path(out).resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    builder=ROOT/skill['path']/'scripts/build_course_stage.py'
    command=[sys.executable,str(builder),'--stage',str(stage),'--delay-frames',str(delay),'--out',str(out)]
    if parameters.get('asset'):command+=['--asset',str(Path(parameters['asset']).resolve())]
    compiled=subprocess.run(command,capture_output=True)
    if compiled.returncode:raise ValueError(compiled.stderr.decode('utf-8',errors='replace')[-1800:])
    cfg=json.loads((out/'request.json').read_text(encoding='utf-8'))
    assets=[{'file':'assets/input.png','sha256':cfg['asset_sha256']}] if cfg.get('asset') else []
    plan={'brief':brief,'selected_skill':skill['name'],'skill_version':skill['version'],'skill_status':skill['status'],
          'parameters':cfg,'assets':assets,'workflow':['course p5/p6 index-based expressions','native Easy Ease In for final vector stage','native AE build','save and reopen native project','actual parameter edit and restore','framewise parameter validation','aerender native output','full-frame technical quality checks'],
          'requires_final_visual_review':True,'scope':'tested course profile: 1080 square, 30fps, 7 seconds; PNG opacity branch has no Trim Paths; exact recording frame alignment unverified'}
    (out/'input-request.json').write_text(json.dumps(request,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
    receipt=execute(ae,out/'build.jsx')
    if receipt.get('status')!='built':return {'status':'failed','stage':'native_build','details':receipt}
    report=render(out,aerender,600,reuse=True)
    result={'status':'technical_pass_visual_review_pending' if report['status']=='passed' else 'failed','plan':'plan.json','project':'project.aep','video':'final.mp4','quality':'quality.json'}
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8');return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('request',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--ae',required=True);ap.add_argument('--aerender',required=True)
    a=ap.parse_args();print(json.dumps(make(json.loads(a.request.read_text(encoding='utf-8-sig')),a.out,a.ae,a.aerender),indent=2))
