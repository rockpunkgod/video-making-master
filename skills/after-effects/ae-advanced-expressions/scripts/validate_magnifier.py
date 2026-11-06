"""Compare real native optical control renders; no substitute for visual acceptance."""
import argparse,json,subprocess,hashlib,math
from pathlib import Path
def decode(path,filters=None):
    cmd=['ffmpeg','-v','error','-i',str(path),'-map','0:v:0']
    if filters:cmd+=['-vf',filters]
    p=subprocess.run(cmd+['-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
    return p.stdout
def validate(root,video=None,output='magnifier-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4'
    w,h=cfg['width'],cfg['height'];size=w*h*3
    normal=decode(root/'native-control-normal.png');no_blur=decode(root/'native-control-no-blur.png');no_bulge=decode(root/'native-control-no-bulge.png')
    if not all(len(p)==size for p in [normal,no_blur,no_bulge]):raise ValueError('Control dimensions mismatch')
    cx,cy=cfg['positions'][0][1:];inside_blur=[];outside_blur=[];inside_bulge=[];far_bulge=[]
    for y in range(2,h,4):
        for x in range(2,w,4):
            dist=math.hypot(x-cx,y-cy);i=(y*w+x)*3
            db=sum(abs(normal[i+k]-no_blur[i+k]) for k in range(3))/3
            du=sum(abs(normal[i+k]-no_bulge[i+k]) for k in range(3))/3
            if dist<60:inside_blur.append(db);inside_bulge.append(du)
            if dist>260:outside_blur.append(db);far_bulge.append(du)
    avg=lambda a:sum(a)/len(a) if a else None
    metrics=dict(inside_blur_mae=avg(inside_blur),outside_blur_mae=avg(outside_blur),inside_bulge_mae=avg(inside_bulge),far_bulge_mae=avg(far_bulge))
    thumb=decode(video,'scale=128:106:flags=area');ts=128*106*3;frames=[thumb[i:i+ts] for i in range(0,len(thumb),ts)];complete=len(frames)==150 and all(len(f)==ts for f in frames)
    motion=max((sum(abs(x-y) for x,y in zip(frames[0],f))/ts for f in frames),default=0) if complete else 0
    checks=dict(native_reopened=native.get('project_reopened') is True,native_frames=native.get('native_frames_checked')==150,native_center_link=native.get('max_center_error',99)<.001,adjustment_coverage=native.get('adjustment_covers_frame') is True,no_expression_errors=not native.get('expression_errors'),controls_rendered=native.get('optical_controls')==['native-control-normal.png','native-control-no-blur.png','native-control-no-bulge.png'],inside_clear=metrics['inside_blur_mae']<1,outside_blurred=metrics['outside_blur_mae']>1,inside_bulged=metrics['inside_bulge_mae']>.5,bulge_localized=metrics['far_bulge_mae']<.5,full_video_decode=complete,rendered_motion=motion>1)
    result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,optical_control_metrics=metrics,decoded_frames=len(frames),max_thumbnail_mae_from_first=motion,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),course_fidelity='not_evaluated',scope='Independent native effect-on/off pixel controls and actual video motion; does not accept source artwork, manual replay timing or inferred dimensions')
    (root/output).write_text(json.dumps(result,indent=2),encoding='utf-8');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='magnifier-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps(r,indent=2));raise SystemExit(r['status']!='passed')
