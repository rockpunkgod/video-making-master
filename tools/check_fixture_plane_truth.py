"""Evaluate native solved projections against the original fixture plane, never feed truth into a solve."""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np

def evaluate(truth_path, trace_path, flow_path, output):
    truth=json.loads(Path(truth_path).read_text(encoding='utf-8-sig'))
    trace=json.loads(Path(trace_path).read_text(encoding='utf-8-sig'))
    flow=json.loads(Path(flow_path).read_text(encoding='utf-8-sig'))
    plane=np.asarray(truth['corners'],np.float32)
    anchors=np.asarray(trace['points'],np.float64)
    corners=np.asarray(trace['corners'],np.float64)
    if len(plane)!=len(anchors) or corners.shape!=(len(plane),4,2):raise ValueError('Frame/shape mismatch')
    initial=np.vstack([anchors[0],corners[0]]).astype(np.float32)
    expected=[]
    for quad in plane:
        h=cv2.getPerspectiveTransform(plane[0],quad)
        expected.append(cv2.perspectiveTransform(initial.reshape(1,5,2),h).reshape(5,2))
    expected=np.asarray(expected)
    anchor_errors=np.linalg.norm(expected[:,0]-anchors,axis=1)
    corner_errors=np.linalg.norm(expected[:,1:]-corners,axis=2)
    def summary(errors):
        rmse=float(np.sqrt(np.mean(errors**2)));maximum=float(errors.max())
        return {'status':'passed' if rmse<=1 and maximum<=2 else 'failed','rmse_pixels':rmse,'maximum_pixels':maximum}
    report={'scope':'original synthetic fixture only; exact source-plane motion for evaluation, not solver input',
            'truth':str(truth_path),'native_trace':str(trace_path),'frames':len(plane),
            'anchor':summary(anchor_errors),'plane_corners':summary(corner_errors),
            'flow_anchor_reference_error':summary(np.linalg.norm(np.asarray(flow['independent_reference'])-expected[:,0],axis=1)),
            'thresholds':{'rmse_max_pixels':1,'maximum_error_pixels':2},
            'per_frame_anchor_error':anchor_errors.tolist(),'per_frame_corner_error':corner_errors.tolist()}
    report['status']='passed' if report['anchor']['status']==report['plane_corners']['status']=='passed' else 'failed'
    Path(output).write_text(json.dumps(report,indent=2),encoding='utf-8')
    return {k:v for k,v in report.items() if not k.startswith('per_frame')}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--truth',required=True);ap.add_argument('--trace',required=True);ap.add_argument('--flow',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    result=evaluate(a.truth,a.trace,a.flow,a.out);print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='passed' else 1)
