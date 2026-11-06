"""Bounded fixed-viewport silhouette comparison; no automatic spatial fitting."""
import argparse,io,json,subprocess
from pathlib import Path
import cv2,numpy as np
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--video',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
if a.out.exists():raise FileExistsError('Preserve prior comparison evidence')
reference=Image.open(a.reference).convert('RGB').crop((571,101,812,342))
render=subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True)
candidate=Image.open(io.BytesIO(render.stdout)).convert('RGB').resize((241,241),Image.Resampling.LANCZOS)
ref=cv2.cvtColor(np.array(reference),cv2.COLOR_RGB2GRAY)<150;mask=cv2.cvtColor(np.array(candidate),cv2.COLOR_RGB2GRAY)<150
dr=cv2.distanceTransform((~ref).astype('uint8'),cv2.DIST_L2,5);dc=cv2.distanceTransform((~mask).astype('uint8'),cv2.DIST_L2,5);distances=np.concatenate([dr[mask],dc[ref]])
iou=float(np.logical_and(ref,mask).sum()/np.logical_or(ref,mask).sum());mean=float(distances.mean());p95=float(np.percentile(distances,95))
report=dict(status='passed_static_silhouette_only' if iou>=.9 and mean<=.15 and p95<=1 else 'failed',reference_crop=[571,101,241,241],reference=str(a.reference),candidate_video=str(a.video),iou=iou,symmetric_mask_distance_mean=mean,symmetric_mask_distance_p95=p95,thresholds=dict(iou_min=.9,mean_max=.15,p95_max=1),alignment='Fixed crop and resize, no spatial fitting',not_validated=['Exact source layer count','Original AEP values for inferred colors','Animation or temporal reference alignment','Human aesthetics'])
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
