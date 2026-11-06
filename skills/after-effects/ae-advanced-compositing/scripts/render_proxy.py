"""Render native ProRes, attach it in AE, then reuse the existing native final renderer."""
import argparse,json,subprocess,time
from fractions import Fraction
from pathlib import Path
from render_ae import render

p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--ae',type=Path,required=True);p.add_argument('--aerender',type=Path,required=True);p.add_argument('--timeout',type=int,default=1800)
a=p.parse_args();root=a.directory.resolve();cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));receipt=json.loads((root/'proxy-build.json').read_text(encoding='utf-8-sig'))
movie=root/'assets/proxy.mov'
if receipt['status']!='built' or movie.exists() or (root/'attached.json').exists():raise ValueError('Fresh successful native proxy preparation required')
began=time.monotonic()
r=subprocess.run([str(a.aerender.resolve()),'-reuse','-project',str(root/'project.aep')],capture_output=True,timeout=a.timeout)
(root/'aerender-proxy.log').write_bytes(r.stdout+b'\n'+r.stderr)
if r.returncode or not movie.is_file():raise RuntimeError('Native proxy render failed; inspect existing Adobe state before retry')
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)],capture_output=True,check=True)
data=json.loads(probe.stdout);s=next(x for x in data['streams'] if x['codec_type']=='video')
checks=dict(codec=s['codec_name']=='prores' and s['profile']=='4444',alpha=s['pix_fmt']=='yuva444p12le',width=s['width']==cfg['width'],height=s['height']==cfg['height'],fps=abs(float(Fraction(s['avg_frame_rate']))-cfg['fps'])<1e-6,frames=int(s['nb_frames'])==round(cfg['duration']*cfg['fps']))
decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-map','0:v:0','-f','null','-'],capture_output=True)
checks['full_decode']=decoded.returncode==0
result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,stream=s,native_bake_wall_seconds=time.monotonic()-began,bytes=movie.stat().st_size)
(root/'proxy-media.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if result['status']!='passed':raise RuntimeError('Native proxy codec/alpha/frame contract failed')
subprocess.Popen([str(a.ae.resolve()),'-r',str(root/'attach.jsx')],cwd=a.ae.resolve().parent)
until=time.monotonic()+a.timeout
while time.monotonic()<until:
    if (root/'attached.json').is_file():
        try:attached=json.loads((root/'attached.json').read_text(encoding='utf-8-sig'))
        except (ValueError,OSError):time.sleep(.25);continue
        if attached['status']!='attached':raise RuntimeError('Native proxy attach failed: '+str(attached))
        break
    time.sleep(.5)
else:raise TimeoutError('No fresh attach receipt; inspect the existing Adobe process before retry')
report=render(root,a.aerender,a.timeout,reuse=True);print(json.dumps(report,indent=2));raise SystemExit(report['status']!='passed')
