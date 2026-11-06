"""Measure p10 row geometry in a labelled 640px+640px comparison, not text identity."""
import argparse,json,statistics
from pathlib import Path
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('image',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
im=Image.open(a.image).convert('L')
if im.size!=(1280,400):raise ValueError('Expected the bounded labelled p10 comparison geometry')
def measure(x):
 active=[];ink_x=[]
 for y in range(40,400):
  active.append(sum(im.getpixel((x+xx,y))<100 for xx in range(20,620))>10)
  if 60<y<349:ink_x.extend(xx for xx in range(640) if im.getpixel((x+xx,y))<100)
 bands=[];start=None
 for y,value in enumerate(active):
  if value and start is None:start=y
  if not value and start is not None:bands.append([start,y-1]);start=None
 if start is not None:bands.append([start,len(active)-1])
 return dict(bands=bands,x_bounds=[min(ink_x),max(ink_x)])
r=measure(0);c=measure(640)
if len(r['bands'])!=len(c['bands']):raise ValueError('Unequal line count, no automatic fitting')
errors=[abs(sum(rb)/2-sum(cb)/2) for rb,cb in zip(r['bands'],c['bands'])];horizontal=max(abs(u-v) for u,v in zip(r['x_bounds'],c['x_bounds']))
result=dict(status='passed_row_geometry_only' if max(errors)<=1 and horizontal<=2 else 'failed',reference=r,candidate=c,max_row_center_error_px=max(errors),median_row_center_error_px=statistics.median(errors),x_bound_difference_px=horizontal,thresholds=dict(row_center_px=1,x_bounds_px=2),not_validated=['digit identity','exact source AEP coordinates','source animation speed','unclipped full-canvas source layout'])
if a.out.exists():raise FileExistsError('Retain previous layout comparison evidence')
a.out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
