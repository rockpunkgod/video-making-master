"""Check real rendered update times against the declared measured profile."""
import argparse,json,subprocess,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();folder=a.directory.resolve();cfg=json.loads((folder/'request.json').read_text(encoding='utf-8'));receipt=json.loads((folder/'receipt.json').read_text(encoding='utf-8-sig'))
if cfg.get('animation')!='reference-sampled':raise ValueError('Reference-sampled number rig required')
run=subprocess.run(['ffmpeg','-v','error','-i',str(folder/'final.mp4'),'-vf','crop=646:380:215:140,scale=216:128:flags=area,tblend=all_mode=difference,signalstats,metadata=print:file=-','-an','-f','null','-'],capture_output=True,check=True,timeout=120)
diff=[float(s.split('=',1)[1]) for s in run.stdout.decode().splitlines() if s.startswith('lavfi.signalstats.YAVG=')];observed=[i+1 for i,v in enumerate(diff) if v>.1];expected=cfg['expected_native_update_frames'];native=receipt['native_change_frames']
report=dict(status='passed_measured_update_contract_only' if len(diff)==round(cfg['duration']*cfg['fps'])-1 and observed==expected==native and not receipt['unexpected_change_frames'] and receipt['binary_hidden'] else 'failed',decoded_difference_frames=len(diff),expected_update_frames=expected,observed_rendered_update_frames=observed,native_text_update_frames=native,unexpected_native_frames=receipt['unexpected_change_frames'],max_between_keyframe_mean_difference=max(v for i,v in enumerate(diff) if i+1 not in expected),codec_threshold=.1,
 reference_timing='Observed25fps source events mapped to30fps native samples with up to one native frame of quantization',
 not_validated=['Absolute source seed values; replay uses inferred event IDs','Exact digit identity','Human visual acceptance','Arbitrary inputs or three-material generalization'])
(folder/'sampled-animation-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(0 if report['status'].startswith('passed') else 1)
