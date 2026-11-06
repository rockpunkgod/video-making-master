"""Native course30 Write-on history, never a Particular replacement."""
import argparse,json,math,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--growth',type=float,default=50);p.add_argument('--angular',type=float,default=30);p.add_argument('--duration',type=float,default=8.04);p.add_argument('--ellipse',choices=['none','fixed','animated'],default='none');p.add_argument('--asset',type=Path);a=p.parse_args()
if not all(math.isfinite(v) for v in [a.growth,a.angular,a.duration]):raise ValueError('Finite inputs required')
if not 10<=a.growth<=80 or not 5<=abs(a.angular)<=40 or not 2<=a.duration<=8.04:raise ValueError('Supported growth10..80, angular magnitude5..40, duration2..8.04')
if abs(a.duration*25-round(a.duration*25))>1e-6:raise ValueError('Duration must be whole25fps frames')
if a.ellipse=='animated' and a.duration<5.04:raise ValueError('Animated course controller requires at least126frames')
if a.asset and (not a.asset.is_file() or a.asset.suffix.lower() not in ['.png','.jpg','.jpeg']):raise ValueError('Existing PNG/JPG required')
if a.asset:
 meta=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(a.asset)],capture_output=True,check=True).stdout)['streams'][0]
 if [meta['width'],meta['height']]!=[720,576]:raise ValueError('Current image adapter requires720x576')
 rgba=subprocess.run(['ffmpeg','-v','error','-i',str(a.asset),'-frames:v','1','-pix_fmt','rgba','-f','rawvideo','-'],capture_output=True,check=True).stdout
 gray=subprocess.run(['ffmpeg','-v','error','-i',str(a.asset),'-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
 if len(rgba)!=720*576*4 or min(rgba[3::4])!=255 or len(gray)!=720*576 or min(gray)<64:raise ValueError('Current material tests require opaque images with minimum luma64')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
cfg=dict(name='COURSE_SPIRAL_WRITEON',animation='spiral-writeon',motion_expectation='required',width=720,height=576,fps=25,duration=a.duration,growth=a.growth,angular=a.angular,ellipse=a.ellipse,asset=None,paint_style=3 if a.asset else 2,brush_size=2,hardness=.79,stroke_length=0,requested_spacing=.001,particular='blocked_missing_effect',inferred=['Square pixel adaptation: original PAL DV pixel aspect not directly read','Duration201frames inferred from source layer Info00201; output may be shortened by caller','Solid color is own cyan and irrelevant in OnTransparent mode'],variant=bool(a.asset) or a.growth!=50 or a.angular!=30 or a.duration!=8.04)
if a.asset:
 (out/'assets').mkdir();dest=out/'assets'/('material'+a.asset.suffix.lower());shutil.copy2(a.asset,dest);cfg['asset']=dest.as_posix()
(out/'request.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'plan.json').write_text(json.dumps(dict(status='candidate',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=30',scope='Write-on branch only; source08:48 onward and ellipse13:40..15:15',adaptation='RevealOriginalImage with own material is a new variant, not course baseline' if a.asset else None),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=Path(__file__).resolve().parent
body=(s/'spiral_writeon.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
