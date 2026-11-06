"""Independent decoded-video check against native per-cell visibility; circle baseline only."""
import argparse,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
if cfg.get('asset'):raise ValueError('Circle center detector cannot validate arbitrary PNG alpha/content')
receipt=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
expected=receipt['expected_opacity_frames']
r=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(root/'final.mp4'),'-vf','scale=108:108,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=120)
stride=108*108
if len(r.stdout)!=150*stride:raise ValueError('Wrong decoded frame count')
failures=[];bright=[];dark=[]
for f in range(150):
 for cell in range(25):
  row,col=divmod(cell,5);x=24+15*col;y=24+15*row
  value=sum(r.stdout[f*stride+(y+dy)*108+x+dx] for dy in [-1,0,1] for dx in [-1,0,1])/9
  visible=expected[f][cell]==100
  (bright if visible else dark).append(value)
  if (visible and value<220) or (not visible and value>10):failures.append(dict(frame=f,cell=cell,expected=expected[f][cell],decoded_center_mean=value))
report=dict(status='passed' if not failures else 'failed',compared_cells=3750,decoded_frames=150,minimum_visible_center=min(bright),maximum_hidden_center=max(dark),failures=failures,
 scope='Decoded video centers match same-identity native opacity results; not aesthetics or exact tutorial random layout')
(root/'circle-pixel-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(bool(failures))
