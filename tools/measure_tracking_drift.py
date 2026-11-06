"""Independent local-feature validation of an AE-projected anchor, using only the flattened source video."""
import argparse
import hashlib
import json
from pathlib import Path
import cv2
import numpy as np

def measure(source,trace_path,report_path,radius=48):
    source=Path(source);trace=json.loads(Path(trace_path).read_text(encoding='utf-8-sig'))
    projected=np.asarray(trace['points'],dtype=np.float64)
    native_corners=np.asarray(trace['corners'],dtype=np.float64) if 'corners' in trace else None
    if projected.ndim!=2 or projected.shape[1]!=2 or not np.isfinite(projected).all():raise ValueError('Invalid native projection trace')
    if native_corners is not None and (native_corners.shape!=(len(projected),4,2) or not np.isfinite(native_corners).all()):raise ValueError('Invalid native plane corner trace')
    cap=cv2.VideoCapture(str(source));ok,frame=cap.read()
    if not ok:raise ValueError('Cannot decode source')
    h,w=frame.shape[:2];gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY);mask=np.zeros_like(gray)
    x,y=projected[0];x0=max(0,int(x-radius));y0=max(0,int(y-radius));x1=min(w,int(x+radius));y1=min(h,int(y+radius));mask[y0:y1,x0:x1]=255
    initial=cv2.goodFeaturesToTrack(gray,maxCorners=120,qualityLevel=.015,minDistance=4,mask=mask,blockSize=5)
    if initial is None or len(initial)<12:raise ValueError('Insufficient independent local features')
    initial=initial.reshape(-1,2);current=initial.copy();origin=initial.copy();previous=gray
    # A small anchor neighborhood cannot certify a large overlay by extrapolation.
    # Require the tested quadrilateral to be supported by tracked features throughout.
    support=[]
    def supported(points,quad):
        hull=cv2.convexHull(points.astype(np.float32))
        return all(cv2.pointPolygonTest(hull,(float(p[0]),float(p[1])),False)>=0 for p in quad)
    if native_corners is not None:support.append(supported(initial,native_corners[0]))
    errors=[0.0];reference=[projected[0].tolist()];counts=[len(initial)];inliers=[];corner_errors=[[0.0]*4] if native_corners is not None else [];cv2.setRNGSeed(1234)
    index=1
    while True:
        ok,frame=cap.read()
        if not ok:break
        if index>=len(projected):raise ValueError('Video has more frames than native trace')
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        nxt,status,lkerr=cv2.calcOpticalFlowPyrLK(previous,gray,current.reshape(-1,1,2),None,winSize=(21,21),maxLevel=3,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,30,.01))
        back,backstatus,_=cv2.calcOpticalFlowPyrLK(gray,previous,nxt,None,winSize=(21,21),maxLevel=3)
        nextpts=nxt.reshape(-1,2);backpts=back.reshape(-1,2)
        good=(status.ravel()==1)&(backstatus.ravel()==1)&(lkerr.ravel()<25)&(np.linalg.norm(backpts-current,axis=1)<.6)
        current=nextpts[good];origin=origin[good]
        if len(current)<12:raise ValueError(f'Independent tracking lost too many features at frame {index}')
        homography,flags=cv2.findHomography(origin,current,cv2.RANSAC,1.5)
        if homography is None or int(flags.sum())<10:raise ValueError(f'Independent plane fit failed at frame {index}')
        expected=cv2.perspectiveTransform(projected[0].astype(np.float32).reshape(1,1,2),homography).reshape(2).astype(float)
        reference.append(expected.tolist());errors.append(float(np.linalg.norm(expected-projected[index])));counts.append(len(current));inliers.append(int(flags.sum()))
        if native_corners is not None:
            expected_corners=cv2.perspectiveTransform(native_corners[0].astype(np.float32).reshape(1,4,2),homography).reshape(4,2)
            corner_errors.append(np.linalg.norm(expected_corners-native_corners[index],axis=1).tolist())
            support.append(supported(current,expected_corners))
        previous=gray;index+=1
    cap.release()
    if len(errors)!=len(projected):raise ValueError('Native trace/video frame count mismatch')
    arr=np.asarray(errors);thresholds={'rmse_max_pixels':1.0,'maximum_error_pixels':2.0}
    rmse=float(np.sqrt(np.mean(arr*arr)));maximum=float(arr.max())
    plane_report={'status':'not_available'}
    if native_corners is not None:
        ce=np.asarray(corner_errors);cr=float(np.sqrt(np.mean(ce*ce)));cm=float(ce.max());plane_report={'status':'passed' if cr<=1.0 and cm<=2.0 else 'failed','rmse_pixels':cr,'maximum_pixels':cm,'per_frame_corner_errors':corner_errors}
    good=rmse<=1.0 and maximum<=2.0 and plane_report['status']!='failed'
    coverage=all(support) if support else False
    report={'status':('passed' if good else 'failed') if coverage else 'inconclusive','scope':'one local planar neighborhood; not whole-scene or arbitrary-input verification',
            'method':'independent Shi-Tomasi features, forward/backward Lucas-Kanade flow, local RANSAC homography; AE trace used only to define frame-zero anchor and compare outputs',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':len(errors),'initial_features':len(initial),'minimum_surviving_features':min(counts),'minimum_inliers':min(inliers),
            'roi':[x0,y0,x1,y1],'roi_radius':radius,'reference_support':{'all_corners_inside_feature_hull_every_frame':coverage,'supported_frames':sum(support),'required_frames':len(projected),'warning':'ROI must also be visually checked to contain one rigid plane'},'rmse_pixels':rmse,'maximum_pixels':maximum,'p95_pixels':float(np.percentile(arr,95)),'thresholds':thresholds,
            'plane_corner_check':plane_report,
            'threshold_rationale':'experimental acceptance for this 960x540 fixture, not a universal tracking threshold',
            'native_projection':projected.tolist(),'independent_reference':reference,'per_frame_error_pixels':errors,'opencv':cv2.__version__,'numpy':np.__version__}
    Path(report_path).write_text(json.dumps(report,indent=2),encoding='utf-8')
    result={k:report[k] for k in ['status','frames','initial_features','minimum_surviving_features','rmse_pixels','maximum_pixels','p95_pixels']}
    result['plane_corner_check']={k:v for k,v in plane_report.items() if k!='per_frame_corner_errors'}
    result['reference_support']=report['reference_support']
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--trace',required=True);ap.add_argument('--report',required=True);ap.add_argument('--radius',type=int,default=48);a=ap.parse_args()
    if not 16<=a.radius<=1024:ap.error('radius must be in [16,1024]')
    if Path(a.report).exists():raise FileExistsError('Use a fresh report path; retain earlier measurements')
    result=measure(a.source,a.trace,a.report,a.radius);print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='passed' else 1)
