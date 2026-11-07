"""Independent distance/profile math, actual full-movie geometry or blur-energy QA."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageChops,ImageStat,ImageFilter

def controller(c,t):
 k=c['keyframes'];return np.array([np.interp(t,[x['time'] for x in k],[x['position'][d] for x in k]) for d in [0,1]])
def mapped(c,p,q):
 u=min(1,float(np.linalg.norm(np.array(p)-q))/c['radius']);return c['near_scale']+(c['far_scale']-c['near_scale'])*u if c['mode']=='scale' else c['near_blur']*(1-u)
def validate(root,video=None,output='distance-quality.json'):
 root=Path(root);c=json.loads((root/'request.json').read_text(encoding='utf-8'));r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';n=round(c['duration']*25);native_errors=[]
 for row in r.get('trace',[]):
  f=row['frame'];q=controller(c,f/25)
  if np.max(abs(q-row['controller'][:2]))>.001:native_errors.append([f,'controller'])
  for i,node in enumerate(row['nodes']):
   ex=mapped(c,c['positions'][i],q);val=node['output'];v=np.array(val[:2]) if c['mode']=='scale' else np.array(val)
   if np.max(abs(v-ex))>.001 or np.max(abs(np.array(node['position'][:2])-c['positions'][i]))>.001:native_errors.append([f,i])
 boundaries=[]
 for i in range(4):
  if c['assets']:
   alpha=Image.open(c['assets'][i]).convert('RGBA').getchannel('A');mask=np.array(alpha)>200;eroded=np.array(alpha.filter(ImageFilter.MinFilter(3)))>200;y,x=np.where(mask&~eroded);angle=np.arctan2(y-22,x-22);order=np.argsort(angle);pts=np.c_[x,y][order];pts=pts[np.linspace(0,len(pts)-1,min(32,len(pts))).astype(int)]-22;boundaries.append(pts)
  else:boundaries.append(np.array([[20*math.cos(k*2*math.pi/32),20*math.sin(k*2*math.pi/32)] for k in range(32)]))
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);rows=[];pixel_failures=[];energy=[[] for _ in range(4)];bg=np.array(c['background'])*255
 for f in range(n):
  raw=proc.stdout.read(320*240*3)
  if len(raw)!=320*240*3:break
  im=np.frombuffer(raw,dtype=np.uint8).reshape(240,320,3).astype(float);q=controller(c,f/25);visible=found=0
  for i,p in enumerate(c['positions']):
   value=mapped(c,p,q)
   if c['mode']=='scale':
    for point in boundaries[i]*value/100+np.array(p):
     if np.linalg.norm(point-q)<23:continue
     x,y=np.round(point).astype(int)
     if not(3<=x<317 and 3<=y<237):continue
     visible+=1;patch=im[y-2:y+3,x-2:x+3];found+=bool(np.max(abs(patch-bg))>18)
   else:
    x,y=p;patch=im[y-28:y+29,x-28:x+29].mean(2);gy,gx=np.gradient(patch);yy,xx=np.mgrid[y-28:y+29,x-28:x+29];mask=(xx-q[0])**2+(yy-q[1])**2>24**2
    energy[i].append(dict(frame=f,blur=value,gradient=float((abs(gx)+abs(gy))[mask].mean())))
  if c['mode']=='scale' and (visible<16 or found/visible<.9):pixel_failures.append(dict(frame=f,found=found,visible=visible))
  rows.append(dict(frame=f,found=found,visible=visible))
 extra=proc.stdout.read();stderr=proc.stderr.read();code=proc.wait(timeout=120);checkpoints=[]
 for f in [0,n//4,n//2,n*3//4,n-1]:
  raw=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf',rf'select=eq(n\,{f})','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout;im=Image.frombytes('RGB',(320,240),raw);orig=Image.open(root/f'native-still-{f}.png').convert('RGB');mae=sum(ImageStat.Stat(ImageChops.difference(im,orig)).mean)/3;checkpoints.append(dict(frame=f,rgb_mae=mae))
 on=Image.open(root/'native-control-mapping-on.png').convert('RGB');off=Image.open(root/'native-control-mapping-off.png').convert('RGB');delta=sum(ImageStat.Stat(ImageChops.difference(on,off)).mean)/3;ratios=[]
 if c['mode']=='blur':
  for i,series in enumerate(energy):
   near=[v['gradient'] for v in series if v['blur']>c['near_blur']*.5];far=[v['gradient'] for v in series if v['blur']<.01];ratio=float(np.mean(near)/np.mean(far)) if near and far else None;ratios.append(dict(target=i,near_frames=len(near),far_frames=len(far),near_to_far_gradient_ratio=ratio))
 structure=r.get('structure',[]);g=r.get('geometry',{});checks=dict(full_movie=code==0 and not stderr.strip() and not extra and len(rows)==n,native_math=len(r.get('trace',[]))==n and not native_errors and r.get('max_formula_error',999)<.001,native_errors=not r.get('expression_errors'),native_checkpoints=all(x['rgb_mae']<2 for x in checkpoints),actual_mapping_image_difference=delta>.1,actual_scale_boundaries=not pixel_failures if c['mode']=='scale' else True,actual_blur_energy=all(x['near_frames']>=2 and x['far_frames']>=2 and x['near_to_far_gradient_ratio']<.85 for x in ratios) if c['mode']=='blur' else True,reopen_edit=r.get('project_reopened') is True and r.get('native_edit',{}).get('edited')!=r.get('native_edit',{}).get('original'),target_structure=len(structure)==4 and all(not x['parented'] and not x['three_d'] and x['output_keys']==0 and x['position_keys']==0 for x in structure),native_fast_blur=all(x['blur_match_name']=='ADBE Fast Blur' and x['blur_dimensions']==1 and x['repeat_edges']==0 for x in structure) if c['mode']=='blur' else True,media=not any(x['missing'] or x['pixel_aspect']!=1 for x in r.get('media',[])),geometry=g.get('width')==320 and g.get('height')==240 and g.get('fps')==25 and g.get('pixel_aspect')==1,controller_keys=r.get('controller_keys')==len(c['keyframes']))
 result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,frames=len(rows),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),checkpoints=checkpoints,mapping_control_rgb_difference=delta,scale_visible_boundary_probes=sum(x['visible'] for x in rows),scale_found_boundary_probes=sum(x['found'] for x in rows),pixel_failures=pixel_failures,native_formula_failures=native_errors,blur_gradient_comparison=ratios,blur_gradient_samples=energy if c['mode']=='blur' else None,limits=['Inferred hand-drag replay and own artwork/matte/canvas/fps; not recovered source identity','5x5 boundary support may include overlapping art; controller region excluded','Blur gradient comparison measures actual smoothing with visible controller disk excluded; not exact sourceFastBlur kernel identity','Native technical pass does not confer human course-fidelity acceptance'])
 (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='distance-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['blur_gradient_samples','pixel_failures']},indent=2));raise SystemExit(r['status']!='passed')
