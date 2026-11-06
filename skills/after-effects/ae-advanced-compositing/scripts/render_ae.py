"""Render a successful native build and package its PNG sequence; never simulate Adobe output."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from validate_video import validate

def check_output(root,cfg):
    report=validate(root/'final.mp4',cfg)
    if cfg.get('name') == 'COURSE_P17_LINE_STYLE':
        from validate_line_style import validate as validate_branch
    elif cfg.get('name') == 'COURSE_P17_STREAK_STYLE':
        from validate_streak_style import validate as validate_branch
    elif cfg.get('name') == 'COURSE_P17_TUNNEL_STYLE':
        from validate_tunnel_style import validate as validate_branch
    elif cfg.get('name') == 'COURSE_P15_ASSEMBLY':
        from validate_assembly import validate as validate_branch
    elif cfg.get('name') == 'COURSE_P16_STYLED_ASSEMBLY':
        from validate_styled_assembly import validate as validate_branch
    elif cfg.get('name') in {'P15_RADIAL', 'COURSE_P15_POLAR', 'COURSE_P15_STREAKS', 'COURSE_P16_CORE', 'COURSE_P16_NOISE_STYLE'}:
        from validate_radial import validate as validate_branch
    else:
        from validate_scene import validate as validate_branch
    scene=validate_branch(root);report['scene_quality']='scene-quality.json'
    if scene['status']!='passed':report['status']='failed'
    (root/'quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

def render(directory,executable,timeout,reuse=False):
    root=Path(directory).resolve();project=root/'project.aep';receipt=root/'receipt.json'
    if not project.is_file() or not receipt.is_file():raise FileNotFoundError('Native project and successful AE receipt required')
    data=json.loads(receipt.read_text(encoding='utf-8-sig'))
    if data.get('status')!='built' or not data.get('project_reopened') or data.get('expression_errors'):
        raise ValueError('Build did not pass native reopen and expression checks')
    if not data.get('selected_template'):raise ValueError('No supported output template found; inspect output_templates in the native receipt')
    if any((root/'render').glob('frame_*')) or (root/'final.mp4').exists():raise FileExistsError('Refusing stale render output')
    try:
        result=subprocess.run([str(Path(executable).resolve()),*(['-reuse'] if reuse else []),'-project',str(project)],capture_output=True,timeout=timeout)
        (root/'aerender.log').write_bytes(result.stdout+b'\n'+result.stderr)
    except subprocess.TimeoutExpired as e:
        (root/'aerender.log').write_bytes((e.stdout or b'')+b'\nTIMEOUT\n'+(e.stderr or b''));raise RuntimeError('Native render timed out; inspect running Adobe process before retry')
    if result.returncode:raise RuntimeError(f'aerender exited {result.returncode}; see aerender.log')
    cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
    if data.get('output_format')=='mp4':
        native=root/'native.mp4'
        if not native.is_file():raise RuntimeError('Native render output missing')
        native.replace(root/'final.mp4')
        return check_output(root,cfg)
    suffix='tif' if data.get('output_format')=='tiff' else 'png'
    frames=sorted((root/'render').glob('frame_*.'+suffix))
    numbers=[int(re.fullmatch(r'frame_(\d+)\.'+suffix,p.name).group(1)) for p in frames]
    cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
    if not numbers or len(numbers)!=round(cfg['duration']*cfg['fps']) or numbers!=list(range(numbers[0],numbers[0]+len(numbers))):
        raise RuntimeError('Missing, extra or noncontiguous native frames')
    digits=len(frames[0].stem.split('_')[-1])
    subprocess.run(['ffmpeg','-v','error','-n','-framerate',str(cfg['fps']),'-start_number',str(numbers[0]),'-i',str(root/'render'/f'frame_%0{digits}d.{suffix}'),
                    '-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'final.mp4')],check=True,timeout=timeout)
    return check_output(root,cfg)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory');ap.add_argument('--aerender',required=True);ap.add_argument('--timeout',type=int,default=1800);ap.add_argument('--reuse',action='store_true')
    a=ap.parse_args();r=render(a.directory,a.aerender,a.timeout,a.reuse);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='passed' else 1)
