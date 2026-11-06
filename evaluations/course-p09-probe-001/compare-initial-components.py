"""Exclude measured viewport border components, without fitting geometry or crop."""
import json
from pathlib import Path
import cv2,numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[2];crop=(347,93,690,389);x,y,w,h=crop
ref=np.array(Image.open(root/'cache/watch/watch-ufk60lhj/frames/cue_0000.jpg').convert('RGB').crop((x,y,x+w,y+h)))
can=np.array(Image.open(root/'samples/course-reproduction-005/p09-initial-001/frame-zero.png').convert('RGB').resize((w,h),Image.Resampling.LANCZOS))
def mask(rgb):
 bg=np.median(rgb[:30,:30,:].reshape(-1,3),axis=0);raw=(np.max(np.abs(rgb.astype(float)-bg),axis=2)>10).astype('uint8')
 count,labels,stats,centroids=cv2.connectedComponentsWithStats(raw);chosen=[i for i in range(1,count) if stats[i,cv2.CC_STAT_AREA]>=1000]
 if len(chosen)!=3:raise ValueError('Expected three large source shapes; no automatic geometry fitting')
 return np.isin(labels,chosen),stats[chosen].tolist()
r,rs=mask(ref);c,cs=mask(can)
dr=cv2.distanceTransform((~r).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE);dc=cv2.distanceTransform((~c).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
d=np.concatenate([dr[c],dc[r]]);mean=float(d.mean());p95=float(np.percentile(d,95))
result=dict(status='passed_geometry_only' if mean<=2 and p95<=4 else 'failed',viewport_crop=crop,mask='contrast >10 from viewport background; keep three components area>=1000; excludes observed border slivers area<=775',source_components=rs,candidate_components=cs,mean_distance_px=mean,p95_distance_px=p95,thresholds=dict(mean=2,p95=4),previous_failure='initial-geometry.json retained',not_validated=['colors','native source dimensions readout','3D random sequence','final timing'])
(root/'evaluations/course-p09-probe-001/initial-components-geometry.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
