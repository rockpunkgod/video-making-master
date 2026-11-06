"""Independent time-sampled pixel checks of native Write-on accumulation; no aesthetics claim."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def validate(root,video=None,output='spiral-quality.json'):
 root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';w,h=720,576;size=w*h;n=round(cfg['duration']*25)
 threshold=42
 if cfg['asset']:
  material=subprocess.run(['ffmpeg','-v','error','-i',str(cfg['asset']),'-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
  if len(material)!=size or min(material)<64:raise ValueError('Current image check requires opaque720x576 material with minimum luma64')
  threshold=42*min(material)/255
 process=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-pix_fmt','gray','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);rows=[];failures=[];previous=0
 def point(t):
  f=t*25;extra=50 if cfg['ellipse']=='fixed' else (0 if f<=50 else 80 if f>=125 else (f-50)/75*80) if cfg['ellipse']=='animated' else 0
  return 360+t*(cfg['growth']+extra)*math.cos(t*cfg['angular']),288+t*cfg['growth']*math.sin(t*cfg['angular'])
 for f in range(n):
  raw=process.stdout.read(size)
  if len(raw)!=size:break
  t=f/25;visible=found=0
  if f>0:
   # Several OLD points must remain while the newest part grows; a moving dot cannot pass.
   for j in range(1,17):
    x,y=point(t*j/16)
    if not(4<=x<w-4 and 4<=y<h-4):continue
    visible+=1;peak=0
    # The nearest discrete birth time differs from a continuous target by <= one brush interval.
    # Follow the analytic tangent in TIME; do not use a large arbitrary spatial tolerance.
    for sub in range(-4,5):
     sx,sy=point(max(0,min(t,t*j/16+sub*.00100708007812/4)));xi,yi=round(sx),round(sy)
     if 3<=xi<w-3 and 3<=yi<h-3:
      peak=max(peak,max(raw[yy*w+xx] for yy in range(yi-2,yi+3) for xx in range(xi-2,xi+3)))
    if peak>threshold:found+=1
   if visible and found/visible<.875:failures.append({'frame':f,'history_found':found,'history_visible':visible})
  count=sum(v>threshold for v in raw);rows.append({'frame':f,'visible_history_points':visible,'found_history_points':found,'bright_pixels':count})
  if f>5 and count<previous*.97:failures.append({'frame':f,'brightness_support_decreased':count,'previous':previous})
  previous=count
 remaining=process.stdout.read();stderr=process.stderr.read();code=process.wait(timeout=120)
 fields={p['index']:p['value'] for p in native.get('fields',[])}
 checks=dict(full_movie=code==0 and not stderr.strip() and len(rows)==n and not remaining,history_retained=not failures,nontrivial_growth=len(rows)==n and rows[-1]['bright_pixels']>rows[min(25,n-1)]['bright_pixels']*2,native_reopened=native.get('project_reopened') is True,native_formula=native.get('max_formula_error',999)<.001 and native.get('native_frames_checked')==n,no_expression_errors=not native.get('expression_errors'),native_edit_restored=native.get('native_edit',{}).get('brush_size_changed')==3 and native.get('native_edit',{}).get('restored')==2,paint_style=fields.get(10)==cfg['paint_style'],unlimited_stroke=fields.get(6)==0,spacing_native_minimum=abs(fields.get(7,999)-.00100708007812)<1e-8,media=not any(x['missing'] for x in native.get('media',[])))
 result=dict(luma_threshold=threshold,status='passed' if all(checks.values()) else 'failed',checks=checks,frames=len(rows),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),measurements=rows,failures=failures,pixel_tolerance='5x5 sample window along analytic time offsets within one native brush spacing, luma threshold42 scaled by minimum source luma for image variants, at least14/16 historical points when all visible. Allows native subframe spacing and compression, not arbitrary pixel identity.',limits=['Not a source pixel match or aesthetic acceptance','Sparse16history points per frame; native receipt separately checks brush formula every frame','Material colors only tested with three supplied bright opaque720x576RGB images','Painted output freezes/clips near late frames as source passes outside canvas; not a failure if accumulated history remains'])
 (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='spiral-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['measurements','failures']},indent=2));raise SystemExit(r['status']!='passed')
