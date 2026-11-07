"""Measure actual Write-on movies against independent historical analytic points."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def point(c,t):
 a=math.sin(t*c['rate_a'])*c['amplitude_a'];b=math.sin(t*c['rate_b'])*c['amplitude_b'];mode=c['mode']
 if mode=='sum':y=a+b
 elif mode=='product':y=a*b
 elif mode=='decay':y=a*max(0,1-t/c['duration'])
 elif mode=='slider':
  r=c['slider_profile'];am=r[-1]['value']
  for x,z in zip(r,r[1:]):
   if t<=z['time']:am=x['value']+(z['value']-x['value'])*max(0,min(1,(t-x['time'])/(z['time']-x['time'])));break
  y=math.sin(t*c['rate_a'])*am
 else:y=a
 return t*c['speed'],288+y

def validate(root,video=None,output='wave-quality.json'):
 root=Path(root);c=json.loads((root/'request.json').read_text(encoding='utf-8'));r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));v=Path(video) if video else root/'final.mp4';n=round(c['duration']*25);w,h=720,576;size=w*h
 fields={x['index']:x['value'] for x in r.get('fields',[])};spacing=fields.get(7,.01);rows=[];failures=[];trace_errors=[]
 for row in r.get('trace',[]):
  expected=point(c,row['frame']/25)
  if max(abs(x-y) for x,y in zip(expected,row['brush']))>.001:trace_errors.append(row['frame'])
 process=subprocess.Popen(['ffmpeg','-v','error','-i',str(v),'-pix_fmt','gray','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for f in range(n):
  raw=process.stdout.read(size)
  if len(raw)!=size:break
  found=visible=0;t=f/25
  if f:
   # Follow nearby analytic birth TIMES within one real native spacing, not a large spatial search.
   for j in range(1,25):
    birth=t*j/24;x,y=point(c,birth)
    if not(4<=x<w-4 and 4<=y<h-4):continue
    visible+=1;peak=0
    for k in range(-8,9):
     sx,sy=point(c,max(0,min(t,birth+k*spacing/8)));xi,yi=round(sx),round(sy)
     if 3<=xi<w-3 and 3<=yi<h-3:peak=max(peak,max(raw[yy*w+xx] for yy in range(yi-2,yi+3) for xx in range(xi-2,xi+3)))
    if peak>145:found+=1
   if visible and found/visible<.875:failures.append({'frame':f,'visible':visible,'found':found})
  rows.append({'frame':f,'visible_history_points':visible,'found_history_points':found,'bright_pixels':sum(x>145 for x in raw)})
 remaining=process.stdout.read();err=process.stderr.read();code=process.wait(timeout=120)
 from PIL import Image,ImageChops,ImageStat
 checkpoints=[]
 for f in [0,n//4,n//2,n*3//4,n-1]:
  actual=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf',rf'select=eq(n\,{f})','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout
  native=Image.open(root/f'native-still-{f}.png').convert('RGB');im=Image.frombytes('RGB',(w,h),actual);mae=sum(ImageStat.Stat(ImageChops.difference(native,im)).mean)/3;checkpoints.append({'frame':f,'rgb_mae':mae})
 off=Image.open(root/'native-control-effect-off.png').convert('RGB');on=Image.open(root/'native-control-effect-on.png').convert('RGB');effect_diff=ImageChops.difference(off,on).getbbox()
 g=r.get('geometry',{});checks=dict(full_movie=code==0 and not err.strip() and len(rows)==n and not remaining,retained_wave_history=not failures,native_formula=len(r.get('trace',[]))==n and not trace_errors and r.get('max_formula_error',999)<.001,no_expression_errors=not r.get('expression_errors'),reopen_edit_restore=r.get('project_reopened') is True and r.get('native_edit')==dict(brush_size_changed=3,restored=2),course_geometry=g==dict(width=720,height=576,pixel_aspect=1,fps=25,duration=c['duration'],layer_count=1,parented=False,three_d=False,position_keys=0),native_paint=fields.get(3)==2 and abs(fields.get(4,0)-.79)<.001 and fields.get(6)==0 and fields.get(10)==1,native_checkpoints=all(x['rgb_mae']<2 for x in checkpoints),actual_effect_pixel_change=effect_diff is not None,media=not any(x['missing'] or x['pixel_aspect']!=1 for x in r.get('media',[])),growing_history=len(rows)==n and rows[-1]['bright_pixels']>rows[min(25,n-1)]['bright_pixels']*1.5)
 result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,frames=len(rows),video_sha256=hashlib.sha256(v.read_bytes()).hexdigest(),native_spacing=spacing,pixel_threshold=145,checkpoints=checkpoints,effect_difference_bbox=effect_diff,measurements=rows,failures=failures,native_trace_failures=trace_errors,limits=['Sparse24history points per frame, at least87.5% visible points; 5x5windows along one actual brush spacing','Does not prove full-source pixel identity, source timing or aesthetic acceptance','Opaque dark720x576PNG only; point-stamp pattern from course product mode is preserved'])
 (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='wave-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['measurements','failures']},indent=2));raise SystemExit(r['status']!='passed')
