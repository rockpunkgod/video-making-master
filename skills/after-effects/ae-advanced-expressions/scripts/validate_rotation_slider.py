"""Check the actual movie UI pixels, native 3D projection and blur control images."""
import argparse,json,subprocess,hashlib
from pathlib import Path

def gray(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf','scale=320:240:flags=area','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,timeout=120)
    if p.returncode:raise RuntimeError('Image decode failed')
    return p.stdout

def validate(root,video=None,output='rotation-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));n=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4'
    run=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf','scale=320:240:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120);data=run.stdout;size=320*240*3;frames=len(data)//size;measurements=[];errors=[]
    for f in range(frames):
        pixels=data[f*size:(f+1)*size];active=[]
        for x in range(320):
            count=0
            for y in range(221,230):
                i=(y*320+x)*3;r,g,b=pixels[i:i+3]
                if 75<=min(r,g,b) and max(r,g,b)<=125 and max(r,g,b)-min(r,g,b)<=5:count+=1
            if count>=7:active.append(x)
        groups=[]
        for x in active:
            if not groups or x-groups[-1][-1]>2:groups.append([x])
            else:groups[-1].append(x)
        groups=[g for g in groups if len(g)>=3]
        raw=n['trace'][min(f,89)]['raw'][0]
        expected=raw if 20<raw<300 else (300 if (raw>=300 if cfg['repair_boundary'] else raw>300) else 20)
        if len(groups)!=1:errors.append({'frame':f,'error':'Expected one gray knob group','groups':len(groups)});continue
        actual=(groups[0][0]+groups[0][-1])/2
        measurements.append({'frame':f,'actual':actual,'expected':expected,'error':abs(actual-expected)})
    on=gray(root/'native-control-blur-on.png');off=gray(root/'native-control-blur-off.png')
    if len(on)!=320*240 or len(off)!=320*240:raise ValueError('Unexpected native blur control dimensions')
    def sharp(a):return sum(abs(a[y*320+x]-a[y*320+x-1])+abs(a[y*320+x]-a[(y-1)*320+x]) for y in range(1,205) for x in range(1,320))
    sharp_on=sharp(on);sharp_off=sharp(off);blur_difference=sum(abs(a-b) for a,b in zip(on[:320*205],off[:320*205]))/(320*205)
    span=max((r['actual'] for r in measurements),default=0)-min((r['actual'] for r in measurements),default=0)
    error=max((r['error'] for r in measurements),default=999)
    checks={'full_movie':run.returncode==0 and len(data)==90*size,'all_knob_frames':len(measurements)==90 and not errors,'rendered_knob_trajectory':error<=1.5,'rendered_knob_motion':span>100,'native_reopened':n.get('project_reopened') is True,'native_expression_errors':not n.get('expression_errors'),'native_formula_trace':n.get('max_knob_error',99)<.001 and n.get('max_rotation_error',99)<.001,'native_boundary_samples':len(n.get('boundary',[]))==8,'native_3d_camera':n['native_structure']['camera'] and n['native_structure']['three_d'],'native_projection_observations':len(n.get('projection_samples',[]))==18 and n.get('max_projection_error',999)<=cfg['projection_tolerance'],'native_blur_enabled':n['native_motion_blur']['composition'] and n['native_motion_blur']['layer'],'actual_blur_control_differs':blur_difference>.1 and sharp_on<sharp_off*.98}
    result={'status':'passed' if all(checks.values()) else 'failed','checks':checks,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':frames,'max_knob_error_design_pixels':error,'knob_span':span,'blur_control':{'on_edge_energy':sharp_on,'off_edge_energy':sharp_off,'mean_luma_difference':blur_difference},'measurements':measurements,'errors':errors,'course_fidelity':'Not accepted; calibration observations are not held-out validation, source shutter unread','scope':'Movie knob pixels and real native blur controls; 3D formulas/projection use native property and toComp evidence, not pixel proof for every glyph'}
    (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--video',type=Path);ap.add_argument('--output',default='rotation-quality.json');a=ap.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k!='measurements'},indent=2));raise SystemExit(r['status']!='passed')
