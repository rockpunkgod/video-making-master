"""Independent PCM reference vs actual native Premiere render, plus full video QA."""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path
import numpy as np
from validate_video import validate

def decode(path):
    r=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-vn','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,dtype='<f4').reshape(-1,2).astype(np.float64)

def check(directory):
    root=Path(directory);plan=json.loads((root/'compiled-plan.json').read_text(encoding='utf-8'));build=json.loads((root/'native-build.json').read_text(encoding='utf-8-sig'))
    path=root/'final.mp4';quality=validate(path,plan);(root/'quality.json').write_text(json.dumps(quality,indent=2),encoding='utf-8')
    sr=48000;n=round(plan['duration']*sr);reference=np.zeros((n,2));cache={};by_role={}
    for clip in plan['audio_clips']:
        source=clip['path']
        if source not in cache:cache[source]=decode(source)
        start=round(clip['start']*sr);count=round(clip['duration']*sr);offset=round(clip['source_in']*sr)
        data=cache[source][offset:offset+count]
        if len(data)<count:
            if count-len(data)>1:raise ValueError('Planned source audio shorter than declared duration')
            data=np.pad(data,((0,count-len(data)),(0,0)))
        keys=np.asarray(clip['gain_keys']);gain=np.interp(np.arange(count)/sr,keys[:,0],keys[:,1]);piece=data*gain[:,None]
        end=min(n,start+count);reference[start:end]+=piece[:end-start]
        if clip['role'] not in by_role:by_role[clip['role']]=np.zeros((n,2))
        by_role[clip['role']][start:end]+=piece[:end-start]
    actual=decode(path);available=min(n,len(actual));a=actual[:available].mean(axis=1);b=reference[:available].mean(axis=1)
    fft_size=1<<(2*available-1).bit_length();correlation=np.fft.irfft(np.fft.rfft(a,fft_size)*np.conj(np.fft.rfft(b,fft_size)),fft_size)
    lags=np.arange(-2400,2401);values=correlation[lags%fft_size];lag=int(lags[int(np.argmax(values))])
    if lag>=0:x=actual[lag:available];y=reference[:available-lag]
    else:x=actual[:available+lag];y=reference[-lag:available]
    rms_error=float(np.sqrt(np.mean((x-y)**2)));reference_rms=float(np.sqrt(np.mean(y*y)));snr=float(20*np.log10(max(reference_rms,1e-15)/max(rms_error,1e-15)))
    window_errors=[]
    for start in range(0,len(x)-4800+1,4800):
        ar=float(np.sqrt(np.mean(x[start:start+4800]**2)));rr=float(np.sqrt(np.mean(y[start:start+4800]**2)))
        if rr>1e-4:window_errors.append(float(20*np.log10(max(ar,1e-15)/rr)))
    analysis=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,check=True)
    text=analysis.stderr.decode(errors='replace');blocks=re.findall(r'\{[^{}]+"input_i"[^{}]+\}',text,re.S)
    loudness=json.loads(blocks[-1]) if blocks else None
    if not loudness:raise ValueError('No native-output loudness analysis')
    true_peak=float(loudness['input_tp']);integrated=float(loudness['input_i'])
    threshold={'max_alignment_ms':1.0,'minimum_reference_snr_db':22.0,'maximum_100ms_rms_error_db':1.0,'maximum_true_peak_dbtp':-1.0,'loudness_observation_range_lufs':[-35,-10]}
    checks={'video_decode_and_properties':quality['status']=='passed','native_eight_tracks':build['audio_tracks']==8,'native_audio_clip_count':len(build['audio_clips'])==len(plan['audio_clips']),
            'audio_length':len(actual)>=n and len(actual)-n<=1024,'alignment':abs(lag)/sr*1000<=threshold['max_alignment_ms'],'independent_mix_snr':snr>=threshold['minimum_reference_snr_db'],
            'window_level_match':bool(window_errors) and max(abs(v) for v in window_errors)<=threshold['maximum_100ms_rms_error_db'],'true_peak':true_peak<=-1,
            'audible_loudness':-35<=integrated<=-10,'finite_samples':bool(np.isfinite(actual).all())}
    report={'status':'passed' if all(checks.values()) else 'failed','checks':checks,'thresholds':threshold,'sample_rate':sr,'native_output_samples':len(actual),'reference_samples':n,
            'alignment_samples':lag,'alignment_ms':lag/sr*1000,'reference_snr_db':snr,'maximum_100ms_level_error_db':max(abs(v) for v in window_errors),'reference_rms':reference_rms,'rms_error':rms_error,
            'integrated_lufs':integrated,'true_peak_dbtp':true_peak,'loudness_range_lu':float(loudness['input_lra']),
            'method':'independent input PCM summation with planned gain curves and timeline offsets; compare decoded native H264/AAC output, not parameter readback',
            'subjective_audio_review':'not_performed_by_numeric_checker','visual_review':'not_performed_by_numeric_checker','loudness_target_note':'broad lab liveness range, not a delivery loudness standard',
            'per_100ms_level_error_db':window_errors}
    (root/'audio-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    # Lossless reference is a diagnostic, not a replacement for native production output.
    if not (root/'independent-reference.wav').exists():
        ref32=reference.astype('<f4');subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(sr),'-ac','2','-i','-','-c:a','pcm_s24le',str(root/'independent-reference.wav')],input=ref32.tobytes(),capture_output=True,check=True)
    return {k:v for k,v in report.items() if k!='per_100ms_level_error_db'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory');a=ap.parse_args();report=check(a.directory);print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
