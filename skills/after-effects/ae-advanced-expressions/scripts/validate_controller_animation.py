"""Check the rendered control demo: four intended updates, no intervening jitter."""
import argparse,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory.resolve()
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
if cfg.get('animation')!='controls-demo':raise ValueError('This check applies to the explicit controller demo')
native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
run=subprocess.run(['ffmpeg','-v','error','-i',str(root/'final.mp4'),'-vf','tblend=all_mode=difference,signalstats,metadata=print:file=-','-an','-f','null','-'],capture_output=True,check=True,timeout=120)
diff=[float(s.split('=',1)[1]) for s in run.stdout.decode().splitlines() if s.startswith('lavfi.signalstats.YAVG=')]
expected={30,60,105,150};observed={i+1 for i,v in enumerate(diff) if v>0.1}
raw=subprocess.run(['ffmpeg','-v','error','-i',str(root/'final.mp4'),'-vf','scale=540:540,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=120).stdout
stride=540*540;failures=[];counts=[]
for f in range(240):
 frame=raw[f*stride:(f+1)*stride];active=[sum(v>200 for v in frame[y*540:(y+1)*540])>=4 for y in range(540)]
 bands=sum(v and (i==0 or not active[i-1]) for i,v in enumerate(active));counts.append(bands)
 wanted=20 if f<105 else 17
 if bands!=wanted:failures.append(dict(frame=f,expected=wanted,observed=bands))
report=dict(status='passed' if len(diff)==239 and len(raw)==240*stride and observed==expected and not failures and all(x['unexpected_changes_with_same_controls']==0 for x in native['text_layers']) else 'failed',
 frames=240,intended_change_frames=sorted(expected),observed_change_frames=sorted(observed),maximum_between_keyframe_mean_luma_difference=max(v for i,v in enumerate(diff) if i+1 not in expected),
 codec_noise_threshold=0.1,row_band_counts=sorted(set(counts)),row_failures=failures[:20],native_string_counts=[x['unique_frame_strings'] for x in native['text_layers']],
 scope='Real video changes only at the four added controller keys; no aesthetic or exact tutorial timing claim')
(root/'controller-animation-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
