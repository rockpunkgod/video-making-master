"""Course21 solid-mask index array and four-slider variant; optional course33 composition."""
import argparse,json,math,shutil
from pathlib import Path
from PIL import Image,ImageChops

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--layout',choices=['fixed','controller'],default='controller');p.add_argument('--columns',type=int,default=5);p.add_argument('--count',type=int,default=25);p.add_argument('--duration',type=float,default=10);p.add_argument('--values',type=float,nargs=4,default=[54,28,57,34]);p.add_argument('--controller-profile',type=Path);p.add_argument('--asset',type=Path);p.add_argument('--point-profile',type=Path);p.add_argument('--heading-offset',type=float);a=p.parse_args();s=Path(__file__).resolve().parent
if not 2<=a.columns<=7 or not 1<=a.count<=49:raise ValueError('2..7columns and1..49duplicates')
if a.layout=='fixed' and (a.controller_profile or a.point_profile):raise ValueError('Fixed source branch has no controller or target')
duration=a.duration;controls=None;pointing=None
if a.controller_profile:
    controls=json.loads(a.controller_profile.read_text(encoding='utf-8'));duration=controls['duration']
if a.point_profile:
    if not a.asset or a.heading_offset is None:raise ValueError('Composed pointing needs a caller PNG and explicit --heading-offset; upward fixtures use -90')
    pointing=json.loads(a.point_profile.read_text(encoding='utf-8'))
    if abs(pointing['duration']-duration)>.0001:raise ValueError('Controller and point profile duration must match requested duration')
if not isinstance(duration,(int,float)) or not math.isfinite(duration) or not 4<=duration<=10 or abs(duration*25-round(duration*25))>1e-6:raise ValueError('4..10seconds on complete25fps frames')
def values(v):
    if len(v)!=4 or not all(isinstance(x,(int,float)) and math.isfinite(x) and -100<=x<=160 for x in v):raise ValueError('Four finite controller values -100..160 required')
values(a.values)
for profile,field in [(controls,'values'),(pointing,'target')]:
    if profile:
        previous=-1
        if not profile.get('keyframes'):raise ValueError('Nonempty profile keyframes required')
        for row in profile['keyframes']:
            t=row['time']
            if not isinstance(t,(int,float)) or not math.isfinite(t) or not previous<t<duration or t<0:raise ValueError('Ascending finite profile times within duration')
            previous=t
            if field=='values':values(row[field])
            elif len(row[field])!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) for x in row[field]) or not 0<=row[field][0]<=320 or not 0<=row[field][1]<=240:raise ValueError('Target points must be within320x240')
        if profile['keyframes'][0]['time']>0:profile['keyframes'].insert(0,dict(profile['keyframes'][0],time=0))
if a.heading_offset is not None and (not math.isfinite(a.heading_offset) or not -360<=a.heading_offset<=360):raise ValueError('Heading offset -360..360')
art=None
if a.asset:
    if a.asset.suffix.lower()!='.png' or not a.asset.is_file():raise ValueError('Existing own transparent PNG required')
    im=Image.open(a.asset).convert('RGBA');w,h=im.size
    if not 16<=w<=2048 or not 16<=h<=2048:raise ValueError('PNG dimensions16..2048')
    rgb=im.convert('RGB');r,g,b=rgb.split();bright=ImageChops.lighter(ImageChops.lighter(r,g),b);support=ImageChops.multiply(bright,im.getchannel('A'));box=support.point(lambda x:255 if x>128 else 0).getbbox()
    if not box:raise ValueError('No visible foreground against black background')
    candidates=[]
    for y in range(h):
        for x in range(w):
            if support.getpixel((x,y))>220:candidates.append(((x+.5-w/2)**2+(y+.5-h/2)**2,x+.5,y+.5))
    if not candidates:raise ValueError('PNG needs an opaque bright probe area for pixel QA')
    _,px,py=min(candidates);sc=25/max(w,h);art=dict(source_width=w,source_height=h,support_box=[(box[0]-w/2)*sc,(box[1]-h/2)*sc,(box[2]-w/2)*sc,(box[3]-h/2)*sc],probe=[(px-w/2)*sc,(py-h/2)*sc])
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
cfg=dict(name='COURSE_INDEX_ARRAY',animation='index-array',width=640,height=480,native_width=320,native_height=240,fps=25,duration=duration,layout=a.layout,columns=a.columns,count=a.count,values=a.values,controller_profile=controls,point_profile=pointing,heading_offset=a.heading_offset or 0,asset=None,art=art,circle_diameter=25,color=[1,0,0],motion_expectation='required' if controls or pointing else 'static',source='https://www.bilibili.com/video/BV1c7GTzMEh5/?p=21',inferred=['Final circle diameter25 inferred from400percent preview, precise source mask vertices/size unread','Pure red approximates source red; exact final picker RGB unread','640x480continuous output wrapper is display adaptation; native320x240square25fps10sec explicitly shown','Controller/target keyframes are explicit manual replay or new variation, not course-authored timeline keys','Localized Slider uses stable property slot1; source English Slider display spelling is not assumed on Chinese host'])
if a.asset:
    (out/'assets').mkdir();dest=out/'assets/input.png';shutil.copy2(a.asset,dest);cfg['asset']=dest.as_posix()
if a.controller_profile or a.point_profile:
    (out/'inputs').mkdir()
    for name,src in [('controller-profile.json',a.controller_profile),('point-profile.json',a.point_profile)]:
        if src:shutil.copy2(src,out/'inputs'/name)
for name,obj in [('request.json',cfg),('plan.json',dict(status='candidate',source=cfg['source'],method='hang=ceil(index/5),lie=index-(hang-1)*5; directgrid or lie*xDistance-xInitial,hang*yDistance-yInitial',native='Full320x240solid with centered circular ADD mask, native duplicate, disabled bottomNull and four sliders',adaptation='PNG input replaces source circle; optional point profile composes explicit course33atan2 method',unclamped=True))]:
    (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=(s/'index_array.jsx').read_text(encoding='utf-8').replace('__ENCODER__',(s/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CONFIG__',json.dumps(cfg)).replace('__OUTPUT__',json.dumps(out.as_posix()));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
