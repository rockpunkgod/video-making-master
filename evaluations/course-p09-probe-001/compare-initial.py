"""Course initial viewport geometry only; don't fit later random positions to a reference."""
import json
from pathlib import Path
import cv2,numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[2]
reference=root/'cache/watch/watch-ufk60lhj/frames/cue_0000.jpg'
candidate=root/'samples/course-reproduction-005/p09-initial-001/frame-zero.png'
crop=(347,93,690,389);x,y,w,h=crop
ref=np.array(Image.open(reference).convert('RGB').crop((x,y,x+w,y+h)))
can=np.array(Image.open(candidate).convert('RGB').resize((w,h),Image.Resampling.LANCZOS))
def mask(rgb):
 bg=np.median(rgb[:30,:30,:].reshape(-1,3),axis=0)
 return np.max(np.abs(rgb.astype(float)-bg),axis=2)>10
r=mask(ref);c=mask(can)
dr=cv2.distanceTransform((~r).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE);dc=cv2.distanceTransform((~c).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
d=np.concatenate([dr[c],dc[r]]);mean=float(d.mean());p95=float(np.percentile(d,95))
result=dict(status='passed_geometry_only' if mean<=2 and p95<=4 else 'failed',reference=str(reference),candidate=str(candidate),viewport_crop=crop,mean_distance_px=mean,p95_distance_px=p95,thresholds=dict(mean=2,p95=4),not_validated=['exact colors','source layer construction','random pattern','final 3D motion'])
output=root/'evaluations/course-p09-probe-001/initial-geometry.json';output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
