"""Course33 two-dimensional unparented atan2 pointing, with explicit manual replay."""
import argparse,json,math,shutil,subprocess
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['letter','grid'],default='grid');p.add_argument('--profile',type=Path);p.add_argument('--asset',type=Path);p.add_argument('--offset',type=float);p.add_argument('--columns',type=int,default=5);p.add_argument('--rows',type=int,default=5);p.add_argument('--mirror-x',action='store_true');a=p.parse_args()
s=Path(__file__).resolve().parent;profile=a.profile or s.parent/'examples'/('p33-'+a.mode+'-replay.json');motion=json.loads(profile.read_text(encoding='utf-8'));w,h=(160,120) if a.mode=='letter' else (320,240)
duration=motion['duration'];keys=motion['keyframes']
if not isinstance(duration,(int,float)) or not math.isfinite(duration) or not 4<=duration<=12 or abs(duration*30-round(duration*30))>1e-7:raise ValueError('Profile duration4..12s on30fps frames')
if not 2<=a.columns<=7 or not 2<=a.rows<=5:raise ValueError('Grid2..7columns,2..5rows; keep40pixel artwork within each cell')
if a.mode=='letter' and (a.columns!=5 or a.rows!=5):raise ValueError('Grid count does not apply to letter mode')
previous=-1
for row in keys:
    t=row['time']
    if not isinstance(t,(int,float)) or not math.isfinite(t) or not previous<t<duration or t<0:raise ValueError('Strictly ascending finite times in profile')
    previous=t
    for name in ['target']+(['follower'] if a.mode=='letter' else []):
        xy=row[name]
        if len(xy)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) for x in xy) or not 0<=xy[0]<=w or not 0<=xy[1]<=h:raise ValueError('Profile requires valid unparented canvas coordinates')
        if a.mirror_x:row[name]=[w-xy[0],xy[1]]
if len(keys)<2:raise ValueError('At least two profile observations required')
if a.asset:
    if a.offset is None:raise ValueError('Caller PNG requires explicit --offset for its local artwork heading; upward fixtures use -90')
    if not a.asset.is_file() or a.asset.suffix.lower()!='.png':raise ValueError('Existing own transparent PNG required')
    meta=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(a.asset)],capture_output=True,check=True).stdout)['streams'][0]
    if not 16<=meta['width']<=2048 or not 16<=meta['height']<=2048:raise ValueError('PNG dimensions16..2048')
    from validate_free_pointing import artwork
    measured=artwork(a.asset)
    if measured['bright_fraction']<.95 or measured['anisotropy']<2 or measured['max_radius']>measured['extent']/2+1:raise ValueError('Current movie-axis adapter requires bright yellow/white elongated PNG inside its centered circular extent; see reference')
offset=a.offset if a.offset is not None else (-90 if a.mode=='letter' else 0)
if not math.isfinite(offset) or not -360<=offset<=360:raise ValueError('Finite offset -360..360')
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False);(out/'inputs').mkdir();shutil.copy2(profile,out/'inputs/motion-profile.json')
if keys[0]['time']>0:keys.insert(0,dict(keys[0],time=0))
cfg=dict(name='COURSE_FREE_POINTING',animation='free-pointing',motion_expectation='required',width=640,height=480,native_width=w,native_height=h,fps=30,duration=duration,mode=a.mode,columns=a.columns,rows=a.rows,offset=offset,mirror_x=a.mirror_x,keyframes=keys,asset=None,background=[0,.2,.145],yellow=[1,1,.6],target_diameter=20 if a.mode=='letter' else 40,target_opacity=30,source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=33',inferred=['160x120 letter and320x240 grid inferred from visible positions/preview ratios, no source composition dialog','30fps and6s replay/640x480 delivery wrapper; source manual dragging at fixed comp time, not original animation keys','Own a badge/font and target geometry reconstructed, original a.ai unavailable; background RGB approximated','Only accepted visible disk centers replayed linearly; ghosted source frames excluded; source anchors/exact repaint timing unverified'])
if a.asset:
    (out/'assets').mkdir();dest=out/'assets/follower.png';shutil.copy2(a.asset,dest);cfg['asset']=dest.as_posix();cfg['inferred'].append('Caller PNG and explicit local heading offset are material adaptation')
for name,obj in [('request.json',cfg),('plan.json',dict(status='candidate',source=cfg['source'],method='point1=transform.position;point2=target.position;chazhi=sub(point1,point2);angle=Math.atan2(chazhi[1],chazhi[0]);radiansToDegrees(angle)+explicitOffset',grid='row=Math.ceil(index/5);column=index-(row-1)*5;x=column*64-32;y=row*48-24;[x,y]',scope='2D unparented layers only; no lookAt/AutoOrient/smoothing substitution',replay='Explicit measured manual UI replay, not course-authored animation'))]:
    (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=(s/'free_pointing.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
