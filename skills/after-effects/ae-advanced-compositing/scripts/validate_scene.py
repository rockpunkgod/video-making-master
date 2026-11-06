"""Check real decoded scene phases and native camera trace; no source fidelity claim."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def validate(root):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));receipt=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    sw,sh=160,90;size=sw*sh*3
    proc=subprocess.run(['ffmpeg','-v','error','-i',str(root/'final.mp4'),'-vf',f'scale={sw}:{sh}:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True,timeout=180)
    if len(proc.stdout)!=480*size:raise ValueError('Expected480 actual decoded scene frames')
    rows=[]
    for f in range(480):
        raw=proc.stdout[f*size:(f+1)*size];red=neutral=lit=0
        for i in range(0,len(raw),3):
            r,g,b=raw[i:i+3];lit+=max(r,g,b)>20
            red+=r>45 and r>1.5*max(g,b)
            neutral+=max(r,g,b)-min(r,g,b)<15 and r>35
        rows.append(dict(frame=f,lit=lit,red=red,neutral=neutral))
    requested_times=[v/24*cfg['camera_time_scale'] for v in cfg['camera_frames']]
    keys=receipt.get('native_camera_keys')
    if keys is None:keys=json.loads((root/'camera-keys.json').read_text(encoding='utf-8-sig'))['native_camera_keys']
    frames=[v['time'] for v in keys];zs=[v['value'][2] for v in keys]
    key_time_error=max(abs(a-b) for a,b in zip(requested_times,frames))
    key_value_error=max(abs(a-b) for a,b in zip(cfg['camera_z'],zs))
    def camera_at(t):
        if t<=frames[0]:return zs[0]
        for i in range(1,len(frames)):
            if t<=frames[i]:
                a=(t-frames[i-1])/(frames[i]-frames[i-1]);return zs[i-1]*(1-a)+zs[i]*a
        return zs[-1]
    trace=receipt['camera_samples'];camera_error=max(abs(v['z']-camera_at(v['frame']/24)) for v in trace)
    last_out=max(x['outPoint'] for x in receipt['role_records']);black=[r['frame'] for r in rows if r['lit']==0]
    # Course13 is a20s rough composition; its input layers end earlier. Keep and
    # report this unfinished tail instead of cropping it or claiming a finished film.
    tail_start=int(last_out*24+.999999)
    phase_times=[('core',0,.8,'neutral'),('noise',2.1,2.8,'neutral'),('contours',4.2,5.2,'red'),('lines',7,8.8,'red')]
    phases=[]
    for name,start,end,kind in phase_times:
        fs=[r for r in rows if start*cfg['camera_time_scale']<=r['frame']/24<=end*cfg['camera_time_scale']]
        peak=max((r[kind] for r in fs),default=0)
        phases.append(dict(name=name,channel=kind,peak_pixels=peak,passed=peak>=10))
    #0.05 world units is at most1/20px at the initial reference plane with
    #zoom=1866.67 and camera distance1866.67. Combined spatial-key interpolation
    #in this host differs from analytic linear interpolation by0.0155 units;
    #a1e-7 world-unit gate exceeds meaningful subpixel accuracy. Source timing
    #uncertainty is separate and is not excused by this tolerance.
    camera_tolerance=.05
    checks=dict(native_build=receipt['status']=='built',native480_camera_samples=len(trace)==480,
                requested_key_count=len(keys)==len(requested_times),
                native_key_times_within_half_subframe=key_time_error<=1/(24*2048)+1e-10,
                native_key_values_within_float_precision=key_value_error<=.002,
                camera_trace_matches_request=camera_error<=camera_tolerance,requested_roles=receipt['main_layers']==6,
                sampled_phase_presence=all(p['passed'] for p in phases),
                tail_matches_input_outpoints=all(r['lit']==0 for r in rows if r['frame']>=tail_start))
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,camera_max_error=camera_error,camera_world_unit_tolerance=camera_tolerance,
        key_time_error=key_time_error,key_time_quantization='Native keyTime readbacks round to1/1024 frame; compare requested keys separately from interpolation of stored keys',key_value_error=key_value_error,phase_presence=phases,
        unfinished_tail=dict(start_frame=tail_start,start_seconds=tail_start/24,duration_seconds=(480-tail_start)/24,
                             reason='Course13 rough layout inputs end here; later lessons still required. Not a render failure waiver or final movie completion.'),
        black_frame_count=len(black),frame_metrics=rows,video_sha256=hashlib.sha256((root/'final.mp4').read_bytes()).hexdigest(),
        limits=['Coarse phase pixels do not prove each layer separately visible','Estimated source timing remains unverified','Exact random patterns, source frame synchronization and aesthetics require separate review'])
    (root/'scene-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();r=validate(a.directory)
    print(json.dumps({k:v for k,v in r.items() if k!='frame_metrics'},indent=2));raise SystemExit(0 if r['status']=='passed' else 1)
