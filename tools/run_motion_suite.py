"""Run a real, sequential AE build/render suite. Never upgrades skill status by itself."""
import importlib.util
import json
from pathlib import Path
from datetime import datetime
from run_ae import execute
from render_ae import render

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('motion_build',ROOT/'skills/after-effects/ae-procedural-motion/scripts/build.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
AE=Path('E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe')
RENDER=AE.with_name('aerender.exe')
configs=[ROOT/'skills/after-effects/ae-procedural-motion/examples'/f'{n}.json' for n in ['square','triangle','hexagon']]+[ROOT/'samples/fixtures'/f'{n}.json' for n in ['geometry','typography','texture']]
suite=ROOT/'samples/runs'/('suite-'+datetime.now().strftime('%Y%m%d-%H%M%S'));suite.mkdir()
results=[]
for path in configs:
    cfg=json.loads(path.read_text(encoding='utf-8'));out=suite/cfg['name']
    print('BUILD '+cfg['name'],flush=True)
    jsx=builder.build(cfg,out);receipt=execute(AE,jsx,120)
    record={'config':path.relative_to(ROOT).as_posix(),'run':out.relative_to(ROOT).as_posix(),'build':receipt}
    if receipt.get('status')=='built':
        print('RENDER '+cfg['name'],flush=True)
        try:record['quality']=render(out,RENDER,600,reuse=True)
        except Exception as e:record['render_error']=str(e)
    results.append(record)
    (suite/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'name':cfg['name'],'build':receipt.get('status'),'quality':record.get('quality',{}).get('status'),'error':record.get('render_error')}),flush=True)
    if receipt.get('status')!='built' or record.get('render_error'):break
print(suite,flush=True)
