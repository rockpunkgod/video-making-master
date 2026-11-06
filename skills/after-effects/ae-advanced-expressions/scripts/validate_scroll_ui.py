"""Read actual movie knob pixels independently of native expression traces."""
import argparse,json,subprocess,hashlib
from pathlib import Path
def validate(root,video=None,output='scroll-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';vertical=cfg['axis']=='vertical';size=320*240*3
    run=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-vf','scale=320:240:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120);data=run.stdout;frames=len(data)//size;measurements=[];errors=[];max_error=0
    if len(native.get('trace',[]))!=180:raise ValueError('Full native input trace required')
    for f in range(frames):
        raw=data[f*size:(f+1)*size];active=[]
        for axis in range(240 if vertical else 320):
            count=0
            for q in range(-5,6):
                x,y=(299+q,axis) if vertical else (axis,223+q);i=(y*320+x)*3;r,g,b=raw[i:i+3]
                if 75<=min(r,g,b) and max(r,g,b)<=125 and max(r,g,b)-min(r,g,b)<=5:count+=1
            if count>=8:active.append(axis)
        groups=[]
        for n in active:
            if not groups or n-groups[-1][-1]>2:groups.append([n])
            else:groups[-1].append(n)
        groups=[g for g in groups if len(g)>=3 or g[0]==0 or g[-1]==(239 if vertical else 319)]
        inp=native['trace'][min(f,179)]['raw'];value=inp[1] if vertical else max(cfg['range'][0],min(cfg['range'][1],inp[0]));limit=240 if vertical else 320;visible=value+10>0 and value-10<limit
        if visible:
            expected=(max(0,value-10)+min(limit,value+10))/2
            if len(groups)!=1:errors.append(dict(frame=f,error='Expected one visible knob',groups=len(groups)));continue
            actual=(groups[0][0]+groups[0][-1])/2;error=abs(actual-expected);max_error=max(max_error,error);measurements.append(dict(frame=f,expected_center=expected,actual_center=actual,error=error))
        else:
            if groups:errors.append(dict(frame=f,error='Unexpected knob pixels outside viewport'))
            measurements.append(dict(frame=f,expected_center=None,actual_center=None,error=0))
    observed=[x['actual_center'] for x in measurements if x['actual_center'] is not None];span=max(observed)-min(observed) if observed else 0
    checks=dict(native_reopened=native.get('project_reopened') is True,native_frames=native.get('native_frames_checked')==180,native_knob_formula=native.get('max_knob_error',99)<.001,native_content_formula=native.get('max_content_error',99)<.001,no_expression_errors=not native.get('expression_errors'),media=not any(x['missing'] for x in native.get('media',[])),full_movie=run.returncode==0 and len(data)==180*size,all_knob_frames=len(measurements)==180 and not errors,rendered_knob_trajectory=max_error<=1.5,rendered_motion=span>5)
    result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),max_knob_error_design_pixels=max_error,pixel_tolerance=1.5,measured_frames=len(measurements),knob_span_design_pixels=span,measurements=measurements,errors=errors,course_fidelity='not_evaluated',scope='Movie knob pixels compared with independently bounded raw native input; native content formula checked separately, source artwork/timing not accepted')
    (root/output).write_text(json.dumps(result,indent=2),encoding='utf-8');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='scroll-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['measurements']},indent=2));raise SystemExit(r['status']!='passed')
