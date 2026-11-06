"""Optional QA using already installed Pillow/NumPy; not required by the runnable skill."""
import json
from pathlib import Path
from PIL import Image
import numpy as np
root=Path(__file__).resolve().parents[2];r=root/'samples/course2-spiral-001';results=[]
for name in ['grid-003','type-002','map-002']:
 cfg=json.loads((r/name/'request.json').read_text(encoding='utf-8'));source=np.asarray(Image.open(cfg['asset']).convert('RGB'),dtype=float);rows=[]
 for f in [0,25,50,75,100,125,150,175,200]:
  b=np.asarray(Image.open(r/'baseline-001'/f'native-still-{f}.png').convert('RGBA'),dtype=float);a=np.asarray(Image.open(r/name/f'native-still-{f}.png').convert('RGBA'),dtype=float);mask=b[:,:,3]>32
  # AE saveFrameToPng in this host stores premultiplied black RGB, independently measured.
  expected=source*b[:,:,3,None]/255;diff=np.abs(a[:,:,:3]-expected)
  rows.append(dict(frame=f,alpha_max_error=float(np.abs(a[:,:,3]-b[:,:,3]).max()),premultiplied_rgb_mean_error=float(diff[mask].mean()),premultiplied_rgb_max_error=float(diff[mask].max()),pixels=int(mask.sum())))
 receipt=json.loads((r/name/'receipt.json').read_text(encoding='utf-8-sig'));results.append(dict(case=name,imported_pixel_aspect=receipt['imported_pixel_aspect'],reopened_pixel_aspect=receipt['material_pixel_aspect'],rows=rows))
checks=dict(same_native_history=all(x['alpha_max_error']==0 for r in results for x in r['rows']),material_rgb_rounding=all(x['premultiplied_rgb_max_error']<=.501 for r in results for x in r['rows']),saved_square_pixels=all(r['reopened_pixel_aspect']==1 for r in results))
out=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,results=results,scope='27 native PNG samples only, not every video pixel or tutorial identity',rgb_model='Source RGB times baseline native alpha, quantized to8bits; premultiplied-black native PNG observed, not straight RGB')
(root/'evaluations/course2-p30-spiral-001/material-native-pixel-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(status=out['status'],checks=checks),indent=2));raise SystemExit(out['status']!='passed')
