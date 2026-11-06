"""Independent movie projection-dot checks; split-disc center and phase when applicable."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def validate(root,video=None,output='orbit-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';size=400*400*3
    p=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf','scale=400:400:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120);frames=len(p.stdout)//size;rows=[];errors=[];max_error=0;glyph_error=0;phase_error=0
    for f in range(frames):
        raw=p.stdout[f*size:(f+1)*size];a=f/cfg['fps']*cfg['speed'];cx,cy=cfg['center'];ox=cx+cfg['radius']*math.cos(a);oy=cy+cfg['radius']*math.sin(a);found=[]
        for vertical in [False,True]:
            active=[]
            for axis in range(400):
                count=0
                for d in range(-4,5):
                    x,y=(cx+150+d,axis) if vertical else (axis,cy+150+d);i=(int(y)*400+int(x))*3;r,g,b=raw[i:i+3]
                    if min(r,g)>215 and 85<b<210:count+=1
                if count>=6:active.append(axis)
            groups=[]
            for x in active:
                if not groups or x-groups[-1][-1]>2:groups.append([x])
                else:groups[-1].append(x)
            groups=[g for g in groups if len(g)>5]
            if len(groups)!=1:errors.append({'frame':f,'projection':'y' if vertical else 'x','groups':len(groups)});found.append(None)
            else:
                value=(groups[0][0]+groups[0][-1])/2;expected=oy if vertical else ox;max_error=max(max_error,abs(value-expected));found.append(value)
        if cfg['asset'] is None:
            purple=[]
            for y in range(max(0,int(oy)-23),min(400,int(oy)+24)):
                for x in range(max(0,int(ox)-23),min(400,int(ox)+24)):
                    i=(y*400+x)*3;r,g,b=raw[i:i+3]
                    if 80<r<210 and 70<g<195 and b>210 and b-max(r,g)>30:purple.append((x,y))
            if len(purple)<200:errors.append({'frame':f,'error':'Split-disc purple pixels missing'})
            else:
                px=sum(x for x,y in purple)/len(purple);py=sum(y for x,y in purple)/len(purple);theta=a if cfg['spin'] else 0;offset=80/(3*math.pi)
                measured=[px+math.sin(theta)*offset,py-math.cos(theta)*offset];glyph_error=max(glyph_error,math.hypot(measured[0]-ox,measured[1]-oy));actual=math.atan2(py-oy,px-ox)-math.pi/2;phase_error=max(phase_error,abs(math.atan2(math.sin(actual-theta),math.cos(actual-theta)))*180/math.pi)
        rows.append({'frame':f,'x':found[0],'y':found[1],'expected_orbit':[ox,oy]})
    checks={'full_movie':p.returncode==0 and len(p.stdout)==300*size,'all_projection_frames':len(rows)==300 and not errors,'movie_projection_trajectory':max_error<=1.5,'native_reopened':native.get('project_reopened') is True,'native_formulas':native.get('max_formula_error',999)<.001 and native.get('native_frames_checked')==300,'zero_motion_keys':native.get('motion_keyframes')==0,'no_expression_errors':not native.get('expression_errors'),'media':not any(x['missing'] for x in native.get('media',[])),'guide_parentage':native['guides']['x_parent']=='x_控制' and native['guides']['y_parent']=='y_控制','split_disc_center':cfg['asset'] is not None or glyph_error<=1.5,'split_disc_phase':cfg['asset'] is not None or phase_error<=10}
    skipped=[]
    if cfg['asset'] is not None:
        skipped=['split_disc_center','split_disc_phase']
        for key in skipped:checks.pop(key)
    result={'skipped_checks':skipped,'status':'passed' if all(checks.values()) else 'failed','checks':checks,'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':frames,'max_projection_error_design_pixels':max_error,'split_disc_max_center_error_design_pixels':None if cfg['asset'] else glyph_error,'split_disc_max_phase_error_degrees':None if cfg['asset'] else phase_error,'measurements':rows,'errors':errors,'glyph_pixel_scope':'Purple half-disc centroid/phase measured in own split-disc cases; arbitrary image glyph pixels not automatically measured','course_fidelity':'Not human accepted; own materials and inferred palette/guide extent remain explicit'}
    (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--video',type=Path);ap.add_argument('--output',default='orbit-quality.json');a=ap.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['measurements','errors']},indent=2));raise SystemExit(r['status']!='passed')
