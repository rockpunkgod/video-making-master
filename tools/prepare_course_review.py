"""Make local source/candidate review media with existing FFmpeg; never infer frame sync."""
import argparse,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--start',type=float,required=True);ap.add_argument('--candidate-start',type=float,default=0);ap.add_argument('--duration',type=float,default=5);ap.add_argument('--crop',type=int,nargs=4,required=True);ap.add_argument('--candidate-crop',type=int,nargs=4);ap.add_argument('--preserve-aspect',action='store_true');ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args();out=a.out.resolve();out.relative_to(ROOT/'cache')
if not a.source.is_file() or not a.candidate.is_file():raise FileNotFoundError('Existing local source and real rendered candidate required')
if a.start<0 or a.candidate_start<0 or not 0<a.duration<=30 or min(a.crop)<0 or min(a.crop[2:])<1:raise ValueError('Invalid bounded review interval/crop')
if out.exists():raise FileExistsError('Fresh local-only review directory required')
out.mkdir(parents=True)
ffmpeg=shutil.which('ffmpeg') or str(ROOT/'.venv/Scripts/ffmpeg.exe')
def run(args):subprocess.run([ffmpeg,'-v','error','-n',*args],check=True,timeout=120)
run(['-ss',str(a.start),'-i',str(a.source.resolve()),'-t',str(a.duration),'-map','0:v:0','-map','0:a?','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(out/'original-course.mp4')])
x,y,w,h=a.crop
font=Path('C:/Windows/Fonts/arial.ttf')
if not font.is_file():raise FileNotFoundError('Installed Arial font required for review labels; no font installation attempted')
font_arg="fontfile='"+font.as_posix().replace(':',r'\:')+"'"
candidate_filter=''
if a.candidate_crop:
 cx,cy,cw,ch=a.candidate_crop
 if min(cx,cy)<0 or min(cw,ch)<1:raise ValueError('Invalid candidate viewport crop')
 candidate_filter=f'crop={cw}:{ch}:{cx}:{cy},'
scaler='scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2:color=black' if a.preserve_aspect else 'scale=640:360'
filters=(f'[0:v]crop={w}:{h}:{x}:{y},{scaler},setsar=1,fps=30,setpts=PTS-STARTPTS,pad=640:400:0:40:color=0x222222,'
         f"drawtext={font_arg}:text='ORIGINAL COURSE':fontcolor=white:fontsize=22:x=15:y=9[left];"
         f'[1:v]{candidate_filter}{scaler},setsar=1,fps=30,setpts=PTS-STARTPTS,pad=640:400:0:40:color=0x222222,'
         f"drawtext={font_arg}:text='CURRENT REPRODUCTION':fontcolor=white:fontsize=22:x=15:y=9[right];"
         '[left][right]hstack=inputs=2[v]')
run(['-i',str(out/'original-course.mp4'),'-ss',str(a.candidate_start),'-i',str(a.candidate.resolve()),'-filter_complex',filters,'-map','[v]','-t',str(a.duration),'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'comparison.mp4')])
run(['-i',str(out/'comparison.mp4'),'-frames:v','1',str(out/'comparison.png')])
record=dict(source=str(a.source.resolve()),source_start=a.start,duration=a.duration,candidate=str(a.candidate.resolve()),candidate_start=a.candidate_start,crop=a.crop,candidate_crop=a.candidate_crop,layout='left original course viewport; right real candidate render; optional candidate crop matches a clipped source viewport and must be disclosed',sync='approximate source playback juxtaposition only; exact composition frame synchronization unverified',distribution='local review only; tutorial excerpt remains in ignored cache')
(out/'review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'original-course.mp4');print(out/'comparison.mp4')
