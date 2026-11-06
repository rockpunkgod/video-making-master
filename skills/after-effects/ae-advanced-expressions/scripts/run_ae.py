"""Execute only a reviewed lab JSX; wait for an AE receipt instead of trusting launcher exit code."""
import argparse
import json
import subprocess
import time
from pathlib import Path
from launch_adobe import launch

def execute(executable,jsx,timeout=120):
    executable=Path(executable).resolve();jsx=Path(jsx).resolve()
    if not executable.is_file() or not jsx.is_file():raise FileNotFoundError('AE executable or reviewed JSX missing')
    receipt=jsx.parent/'receipt.json';target=jsx.parent/'project.aep'
    if receipt.exists() or target.exists():raise FileExistsError('Use a fresh run directory; do not trust stale receipts')
    p,launch_info=launch(executable,['-r',str(jsx)])
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if receipt.is_file():
            try: result=json.loads(receipt.read_text(encoding='utf-8-sig'))
            except (ValueError,OSError):time.sleep(0.25);continue
            if result.get('status')=='built' and not target.is_file():result={'status':'failed','error':'receipt exists but AEP missing'}
            return result
        time.sleep(0.5)
    result={'status':'blocked','reason':'No AE execution receipt before timeout; inspect startup dialogs','launcher_pid':p.pid,'launcher_exit':p.poll(),'project_exists':target.exists()}
    (jsx.parent/'execution.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('jsx');ap.add_argument('--ae',required=True);ap.add_argument('--timeout',type=int,default=120)
    a=ap.parse_args();r=execute(a.ae,a.jsx,a.timeout);print(json.dumps(r,indent=2));raise SystemExit(0 if r.get('status')=='built' else 2)
