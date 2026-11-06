"""Independent rendered motion/period checks plus actual native loop/edit evidence."""
import argparse,json,subprocess,hashlib
from pathlib import Path
def validate(root,video=None,output='butterfly-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    video=Path(video) if video else root/'final.mp4'
    run=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-vf','scale=158:127:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120)
    size=158*127*3;frames=[run.stdout[i:i+size] for i in range(0,len(run.stdout),size)]
    full=len(frames)==200 and all(len(f)==size for f in frames)
    mad=lambda a,b:sum(abs(x-y) for x,y in zip(a,b))/size
    motions=[mad(frames[0],f) for f in frames] if full else []
    period=round(2*cfg['key_frames'][-1]/cfg['speed'])
    integral=abs(period-2*cfg['key_frames'][-1]/cfg['speed'])<1e-6
    repeats=[mad(frames[i],frames[i+period]) for i in range(len(frames)-period)] if full and cfg['mode']=='flap' and integral else []
    checks=dict(native_reopened=native.get('project_reopened') is True,native_frames=native.get('native_frames_checked')==200,native_loop=native.get('max_loop_error',99)<.001,native_opposite=native.get('max_opposite_error',99)<.001,native_expressions=not native.get('expression_errors'),controller_2d=native.get('controller_is_2d') is True,media=bool(native.get('media')) and not any(x['missing'] for x in native.get('media',[])),full_decode=run.returncode==0 and full,rendered_motion=bool(motions) and max(motions)>1)
    if cfg['mode']=='flap' and integral:checks['rendered_pingpong_period']=bool(repeats) and max(repeats)<1.5
    result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),decoded_frames=len(frames),max_mean_rgb_difference_from_first=max(motions,default=0),rendered_repeat_period_frames=period if repeats else None,max_repeat_mean_rgb_error=max(repeats,default=None),repeat_rgb_tolerance=1.5,course_fidelity='not_evaluated',scope='Actual rendered motion and periodicity, not source timing/artwork/camera identity or aesthetic acceptance')
    (root/output).write_text(json.dumps(result,indent=2),encoding='utf-8');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='butterfly-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps(r,indent=2));raise SystemExit(r['status']!='passed')
