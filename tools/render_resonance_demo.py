"""Bounded native full-HD rendering and lossless-stem score packaging."""
import argparse,json,subprocess,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/after-effects/ae-advanced-expressions/scripts'))
from launch_adobe import child_environment
from validate_video import validate
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--aerender',type=Path,required=True);p.add_argument('--package-only',action='store_true');a=p.parse_args();d=a.directory.resolve();c=json.loads((d/'request.json').read_text(encoding='utf-8'));r=json.loads((d/'receipt.json').read_text(encoding='utf-8-sig'))
assert r['status']=='built' and r['project_reopened'] and not r['expression_errors']
expected=round(c['duration']*c['fps'])
if (d/'final.mp4').exists() or (not a.package_only and list((d/'render').glob('frame_*'))):raise FileExistsError('Fresh native output directory required')
if a.package_only:
 proof=json.loads((d/'native-render.json').read_text());assert proof['aerender_exit']==0 and proof['frames']==expected and len(list((d/'render').glob('frame_*.tif')))==expected
else:
 env,_=child_environment();cmd=[str(a.aerender.resolve()),'-project',str(d/'project.aep'),'-mfr','OFF','100','-mem_usage','10','50']
 with (d/'aerender.log').open('wb') as log:result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=2400)
 files=sorted((d/'render').glob('frame_*.tif'));numbers=[int(re.fullmatch(r'frame_(\d+)\.tif',f.name).group(1)) for f in files]
 proof=dict(aerender_exit=result.returncode,frames=len(files),expected=expected,mfr='OFF',cache_percent=10,memory_percent=50,full_resolution=True,project_bit_depth=16,native_output_codec='tiff',native_output_pixel_format='rgba',native_output_channel_bits=8)
 (d/'native-render.json').write_text(json.dumps(proof,indent=2)+'\n')
 if result.returncode or len(files)!=expected or numbers!=list(range(expected)):raise RuntimeError('Native render incomplete; inspect actual log/process before retry')
subprocess.run(['ffmpeg','-v','error','-n','-threads','2','-filter_threads','1','-framerate',str(c['fps']),'-i',str(d/'render/frame_%05d.tif'),'-i',str(d/'assets/score.wav'),'-c:v','libx264','-threads','2','-crf','17','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(d/'final.mp4')],check=True,timeout=600)
q=validate(d/'final.mp4',c);(d/'quality.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(dict(status=q['status'],observed=q['observed'],native_render=proof),indent=2));raise SystemExit(q['status']!='passed')
