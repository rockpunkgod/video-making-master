"""Compare every native output frame with the caller's original picture edit."""
import argparse,json,re,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('case',type=Path);a=ap.parse_args();root=a.case.resolve()
plan=json.loads((root/'compiled-plan.json').read_text(encoding='utf-8'));pictures=plan['picture_clips']
if any(c.get('in',0)!=0 for c in pictures):raise ValueError('Nonzero picture source in-point not calibrated')
stats=root/'picture-frame-ssim.txt'
if stats.exists():raise FileExistsError('Preserve prior comparison; use a fresh case')
cmd=['ffmpeg','-v','error','-i',str(root/'final.mp4')]
for c in pictures:cmd+=['-i',c['path']]
filters=[]
for i,c in enumerate(pictures):filters.append(f'[{i+1}:v]trim=duration={c["duration"]},setpts=PTS-STARTPTS,format=yuv420p[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(len(pictures)))+f'concat=n={len(pictures)}:v=1:a=0[ref]')
# Relative stats filename avoids Windows drive-colon escaping in filter syntax.
filters.append('[0:v]format=yuv420p[out];[out][ref]ssim=stats_file=picture-frame-ssim.txt[checked]')
cmd+=['-filter_complex',';'.join(filters),'-map','[checked]','-an','-f','null','-']
r=subprocess.run(cmd,cwd=root,capture_output=True)
if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-2000:])
scores=[float(x) for x in re.findall(r'All:([0-9.]+)',stats.read_text())];expected=round(plan['duration']*plan['fps'])
checks={'all_expected_frames_compared':len(scores)==expected,'minimum_frame_ssim':bool(scores) and min(scores)>=.90,'mean_frame_ssim':bool(scores) and sum(scores)/len(scores)>=.97}
result={'status':'passed' if all(checks.values()) else 'failed','checks':checks,'frames':len(scores),'expected_frames':expected,'minimum_ssim':min(scores) if scores else None,'mean_ssim':sum(scores)/len(scores) if scores else None,'thresholds':{'minimum_frame_ssim':.90,'mean_ssim':.97},'scope':'Full-frame fidelity of sequential source-only picture edit; does not judge storytelling or audio aesthetics'}
(root/'picture-quality.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='passed' else 1)
