"""Compare native endpoint equations and actual rendered disk motion, using FFmpeg."""
import argparse
import json
import math
import subprocess
from pathlib import Path

def validate(root, video=None, output='spring-quality.json'):
    root=Path(root)
    cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
    native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    video=Path(video) if video else root/'final.mp4'
    w=cfg['design_width'];h=100;frames=round(cfg['duration']*30)
    decoded=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-vf',f'scale={w}:{h}:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120)
    raw=decoded.stdout;size=w*h*3;positions=[];errors=[]
    cy=cfg['a_position'][1]
    for f in range(len(raw)//size):
        frame=raw[f*size:(f+1)*size];active=[]
        for x in range(w):
            count=0
            # Disks are40px high; PNG connector is32px high. Their outer caps
            # remain observable even when a caller supplies a black connector.
            for y in [int(cy)+d for d in [-19,-18,-17,17,18,19]]:
                i=(y*w+x)*3
                if max(frame[i:i+3])<20:count+=1
            if count>=2:active.append(x)
        groups=[]
        for x in active:
            if not groups or x-groups[-1][-1]>3:groups.append([x])
            else:groups[-1].append(x)
        groups=[g for g in groups if g[-1]-g[0]>7]
        if len(groups)!=2:
            errors.append(f'frame{f}: expected two endpoint disks, got{len(groups)}');continue
        a,b=[(g[0]+g[-1])/2 for g in groups]
        t=f/30
        amp=cfg['amplitude']*(1 if cfg['mode']=='constant' else max(0,1-t/cfg['decay_end']))
        expected=cfg['a_position'][0]+cfg['asset_width']+math.sin(t*cfg['angular_rate'])*amp+20-cfg.get('b_anchor',[0,20])[0]
        positions.append(dict(frame=f,a_center=a,b_center=b,expected_b_center=expected,error=abs(b-expected)))
    rgba=subprocess.run(['ffmpeg','-v','error','-i',str(root/'assets/connector.png'),'-pix_fmt','rgba','-f','rawvideo','-'],capture_output=True,timeout=30)
    alphas=rgba.stdout[3::4]
    max_error=max((p['error'] for p in positions),default=float('inf'))
    checks=dict(native_reopened=native.get('project_reopened') is True,
                native_full_trace=native.get('native_frames_checked')==frames,
                native_equations=native.get('max_b_error',999)<.001 and native.get('max_connection_error',999)<.001,
                native_scale_y=native.get('max_scale_y_error',999)<.001,
                positive_scale=native.get('minimum_scale_x',0)>0,
                intrinsic_width=native.get('intrinsic_width')==cfg['asset_width'],
                no_expression_errors=not native.get('expression_errors'),
                actual_alpha_png=rgba.returncode==0 and bool(alphas) and min(alphas)==0 and max(alphas)==255,
                all_video_frames=decoded.returncode==0 and len(raw)==frames*size and len(positions)==frames and not errors,
                rendered_endpoint_trajectory=max_error<=1.5)
    result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,
                max_rendered_b_error_design_pixels=max_error,pixel_tolerance=1.5,
                measured_frames=len(positions),positions=positions,errors=errors,
                scope='Black endpoint disk cap centers outside the32px PNG bounds measured independently of native expression values; no aesthetic acceptance',
                course_fidelity='not_evaluated',source_art=('caller PNG, no claim of editable vector source' if cfg.get('external_png') else 'self-authored, not original course bitmaps'))
    (root/output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='spring-quality.json');a=p.parse_args()
    r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k!='positions'},indent=2));raise SystemExit(r['status']!='passed')
