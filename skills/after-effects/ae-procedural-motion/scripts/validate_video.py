"""Decode every frame and check basic video invariants; no aesthetic or Adobe provenance claim."""
import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

def run(cmd):
    return subprocess.run(cmd,capture_output=True,timeout=300)

def validate(path,expected):
    path=Path(path).resolve()
    if not path.is_file(): return {'status':'failed','error':'video missing','path':str(path)}
    probe=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    if probe.returncode: return {'status':'failed','error':probe.stderr.decode(errors='replace')[-2000:]}
    metadata=json.loads(probe.stdout);streams=[s for s in metadata['streams'] if s['codec_type']=='video']
    if not streams:return {'status':'failed','error':'no video stream'}
    s=streams[0];fps=float(Fraction(s['avg_frame_rate']));duration=float(s.get('duration',metadata['format'].get('duration',0)))
    decode=run(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-f','null','-'])
    hashes=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-vf','scale=64:64','-f','framemd5','-'])
    rows=[r for r in hashes.stdout.decode().splitlines() if r and not r.startswith('#')]
    unique=len({r.rsplit(',',1)[-1].strip() for r in rows})
    # Average before differencing: fine texture reconstruction noise can exceed
    # the same full-resolution threshold even for byte-identical native stills.
    difference=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-vf','scale=64:64:flags=area,tblend=all_mode=difference,signalstats,metadata=print:file=-','-an','-f','null','-'])
    means=[float(line.split('=',1)[1]) for line in difference.stdout.decode().splitlines() if line.startswith('lavfi.signalstats.YAVG=')]
    temporal={'expectation':expected.get('motion_expectation','required'),'difference_measurement':'64x64 area-averaged luma; basic visible-motion presence only','decoded_difference_frames':len(means),'maximum_mean_luma_difference':max(means,default=0),'codec_noise_threshold':0.1}
    if temporal['expectation']=='static_layout':
        receipt=json.loads((path.parent/'receipt.json').read_text(encoding='utf-8-sig'))
        names=receipt.get('native_png_exports',[])
        png_hashes=[hashlib.sha256((path.parent/n).read_bytes()).hexdigest() for n in names if (path.parent/n).is_file()]
        temporal.update(native_png_sha256=png_hashes,native_samples=receipt.get('static_layout_validated_frames',0))
        temporal_pass=len(png_hashes)==5 and len(set(png_hashes))==1 and temporal['native_samples']==round(expected['duration']*expected['fps']) and receipt.get('max_position_error',999)<1e-8 and max(means,default=999)<=0.1
    elif temporal['expectation']=='required':temporal_pass=max(means,default=0)>0.1
    else:raise ValueError('Unknown temporal contract')
    checks={'full_decode':decode.returncode==0 and not decode.stderr.strip(),'frame_hash_decode':hashes.returncode==0,'difference_decode':difference.returncode==0 and len(means)==len(rows)-1,'expected_temporal_behavior':temporal_pass,
            'width':s['width']==expected['width'],'height':s['height']==expected['height'],
            'fps':abs(fps-expected['fps'])<0.001,'duration':abs(duration-expected['duration'])<=1/expected['fps']+0.001,
            'frame_count':len(rows)==round(expected['duration']*expected['fps'])}
    return {'status':'passed' if all(checks.values()) else 'failed','path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'checks':checks,'observed':{'width':s['width'],'height':s['height'],'fps':fps,'duration':duration,'decoded_frames':len(rows),'unique_thumbnail_frames':unique},
            'temporal_contract':temporal,'audio_sync':'not_applicable' if not any(x['codec_type']=='audio' for x in metadata['streams']) else 'not_reviewed',
            'visual_review':'not_reviewed','native_project_editability':'not_checked_by_this_tool','stderr':decode.stderr.decode(errors='replace')[-2000:]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--config',required=True,type=Path);ap.add_argument('--report',required=True,type=Path)
    a=ap.parse_args();result=validate(a.video,json.loads(a.config.read_text(encoding='utf-8-sig')))
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(0 if result['status']=='passed' else 1)
