"""Decode real number-rig video and check all text line bands; not an OCR system."""
import argparse,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));rows_per_block=(cfg['num']+cfg['columns']-1)//cfg['columns'];expected=rows_per_block*2
r=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(root/'final.mp4'),'-vf','scale=540:540,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=120)
stride=540*540
if len(r.stdout)!=150*stride:raise ValueError('Unexpected frame count')
failures=[];observed=[];min_ink=10**9
for f in range(150):
 frame=r.stdout[f*stride:(f+1)*stride];active=[];ink=0
 for y in range(540):
  count=sum(v<80 for v in frame[y*540:(y+1)*540]);ink+=count
  active.append(count>=1)
 bands=sum(value and (i==0 or not active[i-1]) for i,value in enumerate(active));observed.append(bands);min_ink=min(min_ink,ink)
 if bands!=expected:failures.append(dict(frame=f,expected_line_bands=expected,observed_line_bands=bands))
 if any(v<80 for v in frame[:540*50]) or any(v<80 for v in frame[540*500:]):failures.append(dict(frame=f,error='Unexpected ink outside course text margins'))
report=dict(status='passed' if not failures else 'failed',frames=150,expected_line_bands=expected,observed_band_counts=sorted(set(observed)),minimum_black_pixels=min_ink,failure_count=len(failures),failures=failures[:20],scope='Every decoded frame has both unclipped number blocks with expected line counts; digits/alphabet independently checked in native AE, not OCR here')
(root/'number-pixel-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(bool(failures))
