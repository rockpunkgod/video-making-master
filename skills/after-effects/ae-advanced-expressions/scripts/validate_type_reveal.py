"""Measure actual decoded character displacement, fade and settled hold.

Stdlib + installed FFmpeg only. Does not certify exact course easing or seed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory.resolve()
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
receipt=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
w,h=cfg['width'],cfg['height'];size=w*h
frames=sorted(set([0,3,6,12,20,cfg['reveal_frames'],90,150]))
select='+'.join('eq(n\\,%d)'%f for f in frames)
run=subprocess.run(['ffmpeg','-v','error','-i',str(root/'final.mp4'),'-vf',f'select={select},format=gray','-fps_mode','passthrough','-f','rawvideo','-'],capture_output=True,timeout=120,check=True)
if len(run.stdout)!=size*len(frames):raise ValueError('Missing actual decoded samples')
images={f:run.stdout[i*size:(i+1)*size] for i,f in enumerate(frames)}
final=images[150]
columns=[any(final[y*w+x]>100 for y in range(h)) for x in range(w)]
bands=[];start=None
for x,on in enumerate(columns+[False]):
    if on and start is None:start=x
    if not on and start is not None:bands.append([start,x]);start=None
expected_chars=len(cfg['text'].replace(' ',''));checks={'expected_character_bands':len(bands)==expected_chars,'native_build':receipt.get('status')=='built','blank_start':max(images[0])<=3}
def measure(im,band):
    x0,x1=band;mass=moment=0
    for y in range(h):
        value=sum(max(0,v-4) for v in im[y*w+x0:y*w+x1]);mass+=value;moment+=value*y
    return (moment/mass if mass else None),mass
rows=[];covered=set();max_error=0
indices=[i+1 for i,c in enumerate(cfg['text']) if c!=' ']
if len(bands)==expected_chars:
    for i,band in enumerate(bands):
        cy,fullmass=measure(final,band);index=indices[i]
        for f in frames:
            if not 0<f<cfg['reveal_frames']:continue
            y,mass=measure(images[f],band)
            if mass<fullmass*.15:continue
            expected=receipt['samples'][f]['position_y']*(-1 if index%2 else 1)
            error=abs((y-cy)-expected);max_error=max(max_error,error);covered.add(index%2)
            rows.append(dict(frame=f,character_index=index,observed_dy=y-cy,expected_dy=expected,error=error,opacity_mass_ratio=mass/fullmass))
    checks['both_parities_actually_visible']=covered=={0,1}
    checks['actual_character_displacement']=bool(rows) and max_error<=1.25
    full=sum(final);sums=[sum(images[f]) for f in frames if f<cfg['reveal_frames']]
    checks['intermediate_reveal']=any(full*.02<value<full*.9 for value in sums)
hold=[sum(abs(x-y) for x,y in zip(images[f],final))/size for f in frames if f>=cfg['reveal_frames']]
checks['settled_hold']=bool(hold) and max(hold)<=.1
report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,frames=frames,bands=bands,max_centroid_error=max_error,
            max_hold_mean_difference=max(hold,default=None),character_measurements=rows,
            video_sha256=hashlib.sha256((root/'final.mp4').read_bytes()).hexdigest(),
            limits=['Character silhouette bands support bounded Latin inputs only','Fixed1.25px centroid tolerance covers rasterization and compression; not source timing acceptance','Exact course graph handles, source random seed and aesthetic fidelity unverified'])
(root/'type-reveal-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='character_measurements'},indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
