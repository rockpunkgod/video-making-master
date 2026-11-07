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
    motion_expectation=expected.get('motion_expectation','required')
    if motion_expectation not in {'required','static'}:raise ValueError('Unknown motion expectation')
    # Static is an explicit requested behavior, not a waiver for a failed animation.
    static_result=None
    if motion_expectation=='static':
        diff=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-vf','tblend=all_mode=difference,signalstats,metadata=print:file=-','-an','-f','null','-'])
        values=[float(line.split('=',1)[1]) for line in diff.stdout.decode().splitlines() if line.startswith('lavfi.signalstats.YAVG=')]
        stills=[path.parent/'native-stability'/f'frame-{i}.png' for i in range(5)]
        still_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in stills if p.is_file()]
        native_receipt=json.loads((path.parent/'receipt.json').read_text(encoding='utf-8-sig'))
        native_text_stable=bool(native_receipt.get('text_layers')) and all(x['unique_frame_strings']==1 and x['consecutive_changes']==0 for x in native_receipt['text_layers'])
        native_transform_stable=False
        if expected.get('animation')=='index-array' and native_receipt.get('static_evidence',{}).get('kind')=='index-array-transform':
            # A non-text static source must prove its own actual native transforms,
            # zero authored animation keys, and five independently exported PNGs.
            frames=round(expected['duration']*expected['fps']);indices=[0,frames//4,frames//2,frames*3//4,frames-1]
            stills=[path.parent/f'native-still-{i}.png' for i in indices]
            still_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in stills if p.is_file()]
            trace=native_receipt.get('trace',[])
            signatures={json.dumps(dict(values=x['values'],target=x['target'],nodes=x['nodes']),sort_keys=True) for x in trace}
            native_transform_stable=(len(trace)==frames and native_receipt.get('native_frames_checked')==frames and native_receipt.get('motion_keyframes')==0 and len(signatures)==1 and native_receipt.get('static_evidence',{}).get('frames')==indices)
        native_png_stable=len(still_hashes)==5 and len(set(still_hashes))==1
        static_result={'comparison_frames':len(values),'max_mean_luma_difference':max(values) if values else None,'max_allowed_mean_luma_difference':0.1,'native_png_sha256':still_hashes,'native_pngs_identical':native_png_stable,'native_text_all150_frames_identical':native_text_stable,'native_index_array_all_frames_identical':native_transform_stable,'codec_tolerance_reason':'The gate requires five byte-identical native PNGs AND either the original identical-native-text evidence or the explicitly scoped index-array native-transform/zero-key evidence. The0.1 video-codec tolerance was calibrated on independent byte-identical native exports; it cannot pass without that evidence.'}
        temporal_pass=diff.returncode==0 and len(values)==len(rows)-1 and max(values,default=999)<=0.1 and native_png_stable and (native_text_stable or native_transform_stable)
    else:temporal_pass=unique>1
    checks={'full_decode':decode.returncode==0 and not decode.stderr.strip(),'frame_hash_decode':hashes.returncode==0,'expected_temporal_behavior':temporal_pass,
            'width':s['width']==expected['width'],'height':s['height']==expected['height'],
            'fps':abs(fps-expected['fps'])<0.001,'duration':abs(duration-expected['duration'])<=1/expected['fps']+0.001,
            'frame_count':len(rows)==round(expected['duration']*expected['fps'])}
    return {'status':'passed' if all(checks.values()) else 'failed','path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'checks':checks,'observed':{'width':s['width'],'height':s['height'],'fps':fps,'duration':duration,'decoded_frames':len(rows),'unique_thumbnail_frames':unique},
            'motion_expectation':motion_expectation,'static_pixel_check':static_result,
            'audio_sync':'not_applicable' if not any(x['codec_type']=='audio' for x in metadata['streams']) else 'not_reviewed',
            'visual_review':'not_reviewed','native_project_editability':'not_checked_by_this_tool','stderr':decode.stderr.decode(errors='replace')[-2000:]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--config',required=True,type=Path);ap.add_argument('--report',required=True,type=Path)
    a=ap.parse_args();result=validate(a.video,json.loads(a.config.read_text(encoding='utf-8-sig')))
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(0 if result['status']=='passed' else 1)
