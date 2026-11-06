"""Audit one common UI/render frame offset; never alter reproduction parameters."""
import json,sys
from pathlib import Path
import cv2,numpy as np
from PIL import Image
root=Path('E:/自媒体/video-skills-lab')
refs=[(17,'cache/watch/watch-dr91f3wz/frames/cue_0010.jpg'),(28,'cache/watch/watch-qsohnuni/frames/cue_0000.jpg'),(32,'cache/watch/watch-qsohnuni/frames/cue_0001.jpg')]
def mask(p):
    p=p.astype(float);return (p[:,:,0]>18)&(p[:,:,0]>2*p[:,:,1]+8)&(p[:,:,0]>1.5*p[:,:,2]+8)
def dist(m):return cv2.distanceTransform((~m).astype('uint8'),cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
reference=[]
for frame,path in refs:
    r=mask(np.asarray(Image.open(root/path).convert('RGB').crop((437,82,762,407))));reference.append((frame,r,dist(r)))
video=cv2.VideoCapture(str(root/'samples/course-reproduction-002/p06-final-001/final.mp4'));candidates={};idx=0
while idx<=35:
    ok,bgr=video.read()
    if not ok:raise RuntimeError('Native video decode ended early')
    if any(abs(idx-n)<=3 for n,_ in refs):
        image=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)).resize((325,325),Image.Resampling.LANCZOS);m=mask(np.asarray(image));candidates[idx]=(m,dist(m))
    idx+=1
video.release();offsets=[]
for offset in range(-3,4):
    rows=[]
    for n,r,dr in reference:
        c,dc=candidates[n+offset];d=np.concatenate([dr[c],dc[r]])
        rows.append({'reference_ui_frame':n,'candidate_frame':n+offset,'mean_distance_px':float(d.mean()),'p95_distance_px':float(np.percentile(d,95))})
    offsets.append({'shared_offset_frames':offset,'rows':rows,'all_pass':all(r['mean_distance_px']<=2 and r['p95_distance_px']<=4 for r in rows)})
report={'status':'common_capture_offset_found' if any(r['all_pass'] for r in offsets) else 'no_common_passing_offset','scope':'diagnosis only; no animation, camera, shape, color, threshold or geometry parameters changed','tested_shared_offsets':offsets}
(root/'evaluations/course-p06-final-001/capture-alignment.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'offsets':[(r['shared_offset_frames'],r['all_pass'],[round(x['mean_distance_px'],3) for x in r['rows']]) for r in offsets]},indent=2))
