"""Objective native-path, saved-control, actual-video and packaged-audio checks."""
import argparse
import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path
import cv2
import numpy as np

p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);a=p.parse_args();d=a.directory.resolve()
if (d/'line-quality.json').exists():raise FileExistsError('Preserve prior evidence')
c=json.loads((d/'request.json').read_text(encoding='utf-8'));r=json.loads((d/'receipt.json').read_text(encoding='utf-8-sig'))
def smooth(a,b,v):
    q=max(0,min(1,(v-a)/(b-a)));return q*q*(3-2*q)
def expected(t,x):
    u=(x-260)/1400;edge=max(0,math.sin(math.pi*u))**1.3;blend=smooth(9,13,t)
    local=0
    for start,speed,gain in [(1.1,190,1),(5.4,175,.8),(8.3,160,.65)]:
        age=t-start
        if age>0:
            dx=x-430-speed*age
            local+=gain*smooth(0,.22,age)*math.exp(-age/4.2-(dx/190)**2)*math.sin(dx/70)
    standing=.62*math.sin(2*math.pi*.55*t)*math.sin(3*math.pi*u)
    return 690-c['amplitude']*edge*((1-blend)*local+blend*standing)*(1-.97*smooth(17,20,t))
native=np.array([row['vertices'] for row in r['trace']]);pred=np.array([[expected(row['frame']/30,x) for x in np.linspace(260,1660,121)] for row in r['trace']])
max_error=float(np.max(abs(native[:,:,1]-pred)))
edit=r['native_edit'];before=np.array(edit['before']);half=np.array(edit['half']);restored=np.array(edit['restored'])
half_error=float(np.max(abs((before[:,1]-690)*.5-(half[:,1]-690))))
restore_error=float(np.max(abs(before-restored)))
velocity=float(np.max(abs(np.diff(native[:,:,1],axis=0))))
cap=cv2.VideoCapture(str(d/'final.mp4'));counts=[];color_samples=[];frames=0
while True:
    ok,frame=cap.read()
    if not ok:break
    roi=frame[560:810,250:1670];mask=np.max(roi,axis=2)<190;counts.append(int(mask.sum()))
    color_samples.append(float(np.min(np.mean(roi,axis=2))))
    frames+=1
cap.release()
with wave.open(str(d/'assets/score.wav'),'rb') as w:
    source=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
decoded=subprocess.run(['ffmpeg','-v','error','-i',str(d/'final.mp4'),'-map','0:a:0','-f','f32le','-ac','2','-ar','48000','-'],check=True,capture_output=True)
observed=np.frombuffer(decoded.stdout,dtype='<f4');n=min(len(source),len(observed));source=source[:n];observed=observed[:n]
correlation=float(np.corrcoef(source,observed)[0,1]);peak=float(np.max(abs(observed)))
checks=dict(native_expression_errors_absent=not r['expression_errors'],path_formula_all_frames=max_error<.0002,
            actual_edit_survives_save_reopen=half_error<.0002 and restore_error<.0002,
            native_color_matches_brief=np.max(abs(np.array(r.get('native_color',[999]))-np.array([36/255,37/255,34/255,1])))<.00001,
            no_large_framewise_path_jump=velocity<10,actual_video_frame_count=frames==c['duration']*30,
            dark_line_present_every_frame=bool(counts) and min(counts)>1500,
            final_audio_matches_authored_score=correlation>.999,decoded_audio_not_clipped=peak<.99)
report=dict(status='passed' if all(checks.values()) else 'failed',checks={k:bool(v) for k,v in checks.items()},
            video_sha256=hashlib.sha256((d/'final.mp4').read_bytes()).hexdigest(),native_frames=len(native),actual_decoded_video_frames=frames,
            max_path_error_pixels=max_error,max_half_amplitude_error_pixels=half_error,max_restoration_error_pixels=restore_error,
            maximum_vertex_step_pixels_per_frame=velocity,minimum_detected_line_pixels=min(counts) if counts else 0,
            audio_correlation=correlation,decoded_audio_peak=peak,static_frame_review='separate',
            continuous_motion_experience='pending',actual_listening='pending',independent_artistic_review='pending',
            scope='Objective rendering/control checks only. Sampling every frame does not prove normal-speed viewing, listening or aesthetic success.')
(d/'line-quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2));raise SystemExit(report['status']!='passed')
