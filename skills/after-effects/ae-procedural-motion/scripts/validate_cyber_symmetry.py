"""Inspect a real rendered cyber-line frame with existing Pillow/NumPy; no OCR."""
import argparse,io,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('media',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
if a.report.exists():raise FileExistsError('Preserve prior image checks')
raw=subprocess.run(['ffmpeg','-v','error','-i',str(a.media),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True,timeout=90).stdout
im=np.asarray(Image.open(io.BytesIO(raw)).convert('RGB')).astype(np.int16)
if im.shape[:2]!=(1080,1080):raise ValueError('This check requires the tested1080 square, Mirror center[540,540] and angle0')
r,g,b=im[:,:,0],im[:,:,1],im[:,:,2];red_mask=(r>120)&(r-g>40)&(r-b>40)
gray=subprocess.run(['ffmpeg','-v','error','-i',str(a.media),'-frames:v','1','-vf','format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=90).stdout
full_mask=np.frombuffer(gray,np.uint8).reshape((1080,1080))<150
# Actual Mirror uses x'=2*540-x. A whole-image flip instead reflects about539.5.
# Compare the valid x1..1079 intersection; do not search for a best-fitting axis.
mask=full_mask[:,1:];flipped=mask[:,::-1];union=int((mask|flipped).sum());iou=float((mask&flipped).sum()/union) if union else 0;ink=int(red_mask.sum())
result=dict(status='passed_first_frame_symmetry_only' if ink>=100 and iou>=.93 else 'failed',media=str(a.media.resolve()),foreground_pixels=ink,silhouette_pixels=int(full_mask.sum()),horizontal_mirror_mask_iou=iou,pixel_reflection_rule='x_prime=1080-x, fixed by native Mirror center540; valid columns1..1079, no axis fitting',measurement='Full-resolution luma silhouette; thin red RGB edges are affected by4:2:0 chroma subsampling',thresholds=dict(min_foreground=100,min_iou=.93),scope='First decoded frame only; native150-frame geometry and five identical native PNGs separately prove static-layout behavior, not animation or human aesthetics')
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));raise SystemExit(0 if result['status'].startswith('passed') else 1)
