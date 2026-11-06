"""Measure reference/native foreground extent; never infer aesthetic acceptance."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def measure(path,kind,crop=None):
    im=Image.open(path).convert('RGB')
    if crop:im=im.crop(crop)
    a=np.asarray(im).astype(np.int16);hi=a.max(2);lo=a.min(2)
    mask=(lo>165)&((hi-lo)<35) if kind=='contour' else (hi>80)&((hi-lo)>35)
    ys,xs=np.where(mask)
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),width=im.width,height=im.height,pixel_fraction=float(mask.mean()),bbox=None if not len(xs) else [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],extent=None if not len(xs) else [float((xs.max()+1-xs.min())/im.width),float((ys.max()+1-ys.min())/im.height)])
rows=[]
ref=ROOT/'cache/final-fit-20261107/reference-frames'
for name,kind,source,old,new in [('tunnel10','contour','frame_025.jpg',252,248),('tunnel11','contour','frame_026.jpg',252,264),('ending22','lines','frame_037.jpg',540,540),('ending24','lines','frame_038.jpg',599,594)]:
    rows.append(dict(name=name,reference=measure(ref/source,kind,(555,173,1520,716)),prior002=measure(ROOT/f'samples/course-reproduction-022/final-reconstruction-005/inputs/extent-baseline/native-still-{old}.png',kind),current005=measure(ROOT/f'samples/course-reproduction-022/final-reconstruction-005/native-still-{new}.png',kind)))
result=dict(status='measured_not_acceptance',method='Contour: minRGB>165 and channel spread<35. Lines: maxRGB>80 and spread>35. Bounding boxes in each image normalized to its own size.',limitations=['Preview can lag behind source UI clock; samples are stage-envelope comparisons, not exact matched frames','Random path identities differ; extent alone cannot validate geometry, timing, color or aesthetics','A cropped outer contour can touch frame boundaries; no claim that larger is always better'],pairs=rows)
(ROOT/'evaluations/course-final-reconstruction-002/extent-measurements.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps({row['name']:{k:row[k]['extent'] for k in ['reference','prior002','current005']} for row in rows},indent=2))
