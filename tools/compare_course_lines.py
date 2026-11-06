"""Compare red contour geometry after an explicitly documented viewport crop.

The crop maps the recording viewport, not geometry or animation parameters.
This does not validate color, easing, or unobserved lesson stages.
"""
import argparse,json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--crop',type=int,nargs=4,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
x,y,w,h=a.crop
reference=np.array(Image.open(a.reference).convert('RGB').crop((x,y,x+w,y+h)))
candidate=np.array(Image.open(a.candidate).convert('RGB').resize((w,h),Image.Resampling.LANCZOS))
def mask(rgb):
    p=rgb.astype(float);return (p[:,:,0]>18)&(p[:,:,0]>2*p[:,:,1]+8)&(p[:,:,0]>1.5*p[:,:,2]+8)
r=mask(reference);c=mask(candidate)
if min(r.sum(),c.sum())<50:raise ValueError('Insufficient contour evidence')
dr=cv2.distanceTransform((~r).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
dc=cv2.distanceTransform((~c).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
distances=np.concatenate([dr[c],dc[r]])
mean=float(distances.mean());p95=float(np.percentile(distances,95))
result={'status':'passed_geometry_only' if mean<=2 and p95<=4 else 'failed','reference':str(a.reference),'candidate':str(a.candidate),'reference_viewport_crop':a.crop,'crop_note':'Viewport bounds inferred from displayed square composition; no source-motion or shape fitting performed','reference_red_pixels':int(r.sum()),'candidate_red_pixels':int(c.sum()),'bidirectional_mean_distance_viewport_px':mean,'p95_distance_viewport_px':p95,'thresholds':{'mean_px':2,'p95_px':4},'not_validated':['exact RGB','full motion timing','easing','later Trim Paths stage','enabled camera stage']}
a.out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
