"""Calibration of the quality checker with FFmpeg fixtures, not AE-produced demonstrations."""
import json
import subprocess
from pathlib import Path
from validate_video import validate

ROOT=Path(__file__).resolve().parents[1];out=ROOT/'cache/quality-selftest';out.mkdir(parents=True,exist_ok=True)
expected={'width':128,'height':128,'fps':12,'duration':1}
results={}
for name,source in [('moving','testsrc2=size=128x128:rate=12:duration=1'),('static','color=c=black:size=128x128:rate=12:duration=1')]:
    target=out/f'{name}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',source,'-c:v','libx264','-pix_fmt','yuv420p',str(target)],check=True)
    results[name]=validate(target,expected)
results['missing']=validate(out/'missing.mp4',expected)
results['wrong_dimensions']=validate(out/'moving.mp4',{**expected,'width':256})
assert results['moving']['status']=='passed',results['moving']
assert results['static']['status']=='failed' and not results['static']['checks']['has_motion']
assert results['missing']['status']=='failed'
assert results['wrong_dimensions']['status']=='failed' and not results['wrong_dimensions']['checks']['width']
report={'scope':'quality checker calibration only, not native AE testing','status':'passed','cases':results}
(ROOT/'evaluations/quality-checker-selftest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('4 quality checker calibration cases passed; no AE rendering is claimed.')
