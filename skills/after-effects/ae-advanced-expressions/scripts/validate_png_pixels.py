"""Compare actual per-cell video pixels to the caller PNG composited on black.

Pillow is reused for the independent image reference, not for producing the video.
"""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));receipt=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
if not cfg.get('asset'):raise ValueError('PNG branch required')
im=Image.open(cfg['asset']).convert('RGBA');fit=100/max(im.size);size=tuple(max(1,round(v*fit)) for v in im.size)
im=im.resize(size,Image.Resampling.BICUBIC);canvas=Image.new('RGBA',(100,100),(0,0,0,255));canvas.alpha_composite(im,((100-size[0])//2,(100-size[1])//2));template=canvas.convert('L').resize((20,20),Image.Resampling.LANCZOS);pixels=list(template.tobytes());energy=sum(pixels)/400
if energy<1:raise ValueError('Input too dark for this pixel detector; do not call it passed')
visible_gate=min(12,energy*.25)  # A blank frame must fail even for thin typography.
r=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(root/'final.mp4'),'-vf','scale=216:216,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=120)
stride=216*216
if len(r.stdout)!=150*stride:raise ValueError('Wrong decoded frame count')
failures=[];maximum=0
for f in range(150):
 for cell in range(25):
  row,col=divmod(cell,5);x=48+30*col-10;y=48+30*row-10;visible=receipt['expected_opacity_frames'][f][cell]==100
  values=[r.stdout[f*stride+(y+dy)*216+x+dx] for dy in range(20) for dx in range(20)]
  error=sum(abs(v-(pixels[i] if visible else 0)) for i,v in enumerate(values))/400;maximum=max(maximum,error)
  # Allow resampling/codec differences; hidden cells must remain black.
  if error>(visible_gate if visible else 1):failures.append(dict(frame=f,cell=cell,expected_visible=visible,mean_absolute_error=error))
report=dict(status='passed' if not failures else 'failed',compared_cells=3750,decoded_frames=150,input_mean_gray=energy,maximum_mean_absolute_error=maximum,thresholds=dict(visible_mae=visible_gate,hidden_mae=1),blank_visible_cell_would_fail=energy>visible_gate,failure_count=len(failures),failures=failures[:25],scope='Original PNG alpha/shape/content and per-cell temporal visibility; not typography readability or aesthetics')
(root/'png-pixel-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(bool(failures))
