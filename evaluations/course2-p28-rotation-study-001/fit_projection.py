"""Infer a camera/plane substitute from reviewed course circle centers; not original parameters.

Uses existing SciPy, NumPy and OpenCV, with local-only previously extracted images.
The source does not teach this calibration. Native AE must validate its output.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

root=Path(__file__).resolve().parents[2]
rows=json.loads((root/'evaluations/course2-p28-rotation-study-001/source-circle-detection.json').read_text())
# Maps detected component IDs to manually reviewed a,e,w,e,s,t identities.
# Clipped or split circles are excluded; geometric box centers reduce white-letter bias.
mapping={0:{3:3,4:4,5:5},1:{0:5,1:4,2:3},2:{0:0,1:1},3:{5:0,4:1,3:2,2:5},4:{2:0,4:4,5:5},5:{5:0,3:1,4:5}}
angles=[0,90,90-180*(241.5-20)/280,90-180*(93.7-20)/280,90-180*(132.6-20)/280,90-180*(109.2-20)/280]
samples=[]
for row in rows:
    cue=row['cue']
    for component,index in mapping[cue].items():
        x,y,w,h=row['components'][component]['box']
        samples.append((angles[cue],index,[(x+w/2)/.95,(y+h/2)/.95]))

def project(par,theta,index):
    # Gauge: camera x=0, z=-500; plane z=0. Other equivalent solutions exist.
    ey,roll,zoom,px,py=par[:5];points=par[5:].reshape(6,2)
    v=np.array([0.,-ey,500.]);forward=v/np.linalg.norm(v)
    right=np.array([1.,0.,0.]);down=np.cross(forward,right)
    a=np.deg2rad(roll);r=np.cos(a)*right+np.sin(a)*down;d=-np.sin(a)*right+np.cos(a)*down
    a=np.deg2rad(theta);x,y=points[index];world=np.array([px+np.cos(a)*x-np.sin(a)*y,py+np.sin(a)*x+np.cos(a)*y,0.])
    delta=world-np.array([0.,ey,-500.]);depth=np.dot(delta,forward)
    return np.array([160.,120.])+zoom*np.array([np.dot(delta,r),np.dot(delta,d)])/depth

def residual(par):
    return np.concatenate([project(par,theta,i)-xy for theta,i,xy in samples])

initial=np.array([1000.,0.,800.,330.,50.]+sum(([-340+55*i,30+30*i] for i in range(6)),[]))
low=np.array([100.,-80.,100.,-1000.,-1000.]+[-900.,0.]*6)
high=np.array([3000.,80.,4000.,1000.,1000.]+[-1.,900.]*6)
solutions=[]
for ey in [500.,1000.,1800.]:
    start=initial.copy();start[0]=ey
    fit=least_squares(residual,start,bounds=(low,high),loss='soft_l1',f_scale=2,max_nfev=4000)
    solutions.append(fit)
fit=min(solutions,key=lambda f:np.sum(residual(f.x)**2));par=fit.x
errors=[float(np.linalg.norm(project(par,theta,i)-xy)) for theta,i,xy in samples]
result={'status':'inferred_projection_fit_native_validation_required','samples':len(samples),'rms_design_pixels':float(np.sqrt(np.mean(np.square(errors)))),'max_design_pixels':max(errors),'camera':{'position':[0,float(par[0]),-500],'point_of_interest':[0,0,0],'zoom':float(par[2]),'roll_degrees':float(par[1])},'artwork_position':[float(par[3]),float(par[4]),0],'local_points':par[5:].reshape(6,2).tolist(),'sample_records':[{'theta':t,'glyph':i,'target':xy,'fit':project(par,t,i).tolist(),'error':e} for (t,i,xy),e in zip(samples,errors)],'limitations':['Source screenshot compression, motion blur and rounded UI positions introduce measurement error','Source viewport scale.95 and origins are inferred','Not unique source camera, layer or asset recovery','No held-out test yet; fit is not visual acceptance','Underlying Illustrator artwork replaced only after explicit native validation']}
(root/'evaluations/course2-p28-rotation-study-001/projection-fit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['sample_records','local_points']}))
