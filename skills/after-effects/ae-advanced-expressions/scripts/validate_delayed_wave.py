"""Actual movie probes of recursive3D waves; held-out native projective calibration."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageChops,ImageStat

def position(c,i,t):return np.array([360+(i-1)*c['spacing'],288,c['amplitude']*math.cos(c['rate']*(t-(i-1)*c['delay']))])
def world(c,i,t,fraction):
 p=position(c,i,t);p[1]+=460.8*(fraction-.5);return np.r_[p,1]
def project(matrix,p):
 q=matrix@p;return q[:2]/q[2]
def physical_projection(cam,p,par):
 scale=np.array([par,1,1]);center=np.array(cam['position']);fw=(np.array(cam['point_of_interest'])-center)*scale;fw/=np.linalg.norm(fw);right=np.cross([0,1,0],fw);right/=np.linalg.norm(right);down=np.cross(fw,right);roll=cam['roll']*math.pi/180
 axes=np.array([right*math.cos(roll)+down*math.sin(roll),down*math.cos(roll)-right*math.sin(roll),fw]);q=axes@((p[:3]-center)*scale);return q[:2]/q[2]*[cam['zoom']/par,cam['zoom']]+[360,288]
def calibrate(c,r):
 rows=[]
 for ob in r['projection']:
  for name,fraction in [('top',0),('center',.5),('bottom',1)]:rows.append((world(c,ob['index'],ob['frame']/25,fraction),np.array(ob[name])))
 train=[x for i,x in enumerate(rows) if i%4];held=[x for i,x in enumerate(rows) if not i%4];design=[]
 for p,q in train:design.extend([np.r_[p,np.zeros(4),-q[0]*p],np.r_[np.zeros(4),p,-q[1]*p]])
 _,_,v=np.linalg.svd(np.array(design),full_matrices=False);matrix=v[-1].reshape(3,4)
 return matrix,dict(training_points=len(train),heldout_points=len(held),max_training_error=max(float(np.linalg.norm(project(matrix,p)-q)) for p,q in train),max_heldout_error=max(float(np.linalg.norm(project(matrix,p)-q)) for p,q in held),matrix=matrix.tolist(),scope='Actual AE toComp camera calibration, independently computed world positions. Not source camera recovery.')
def validate(root,video=None,output='delayed-wave-quality.json'):
 root=Path(root);c=json.loads((root/'request.json').read_text(encoding='utf-8'));r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));v=Path(video) if video else root/'final.mp4';n=round(c['duration']*25);matrix,cal=calibrate(c,r)
 physical_errors=[float(np.linalg.norm(physical_projection(r['camera'],world(c,ob['index'],ob['frame']/25,fraction),128/117)-ob[name])) for ob in r['projection'] for name,fraction in [('top',0),('center',.5),('bottom',1)]]
 cal['max_independent_pal_camera_error']=max(physical_errors)
 camera_request_error=max([float(np.max(abs(np.array(c['camera'][key])-r['camera'][key]))) for key in ['position','point_of_interest','zoom']]+[abs(c['camera']['roll_degrees']-r['camera']['roll'])])
 errors=[]
 for row in r.get('trace',[]):
  for ob in row['nodes']:
   ex=position(c,ob['index'],row['frame']/25)
   if np.max(abs(ex-np.array(ob['position'])))>.001 or abs(ob['opacity']-(100-(ob['index']-1)*3))>.001:errors.append([row['frame'],ob['index']])
 process=subprocess.Popen(['ffmpeg','-v','error','-i',str(v),'-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);rows=[];failures=[];size=720*576*3
 for f in range(n):
  raw=process.stdout.read(size)
  if len(raw)!=size:break
  im=np.frombuffer(raw,dtype=np.uint8).reshape(576,720,3);visible=found=0
  for i in range(1,c['count']+1):
   threshold=max(14,(100-(i-1)*3)*1.2)
   for u in [.1,.3,.5,.7,.9]:
    x,y=project(matrix,world(c,i,f/25,u));x,y=round(float(x)),round(float(y))
    if not (3<=x<717 and 3<=y<573):continue
    visible+=1
    if im[y-2:y+3,x-2:x+3].max()>threshold:found+=1
  if not visible or found/visible<.95:failures.append(dict(frame=f,found=found,visible=visible))
  rows.append(dict(frame=f,found_points=found,visible_points=visible))
 remaining=process.stdout.read();stderr=process.stderr.read();code=process.wait(timeout=120);checkpoints=[]
 for f in [0,n//4,n//2,n*3//4,n-1]:
  data=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf',rf'select=eq(n\,{f})','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout
  image=Image.frombytes('RGB',(720,576),data);original=Image.open(root/f'native-still-{f}.png').convert('RGB');mae=sum(ImageStat.Stat(ImageChops.difference(image,original)).mean)/3;checkpoints.append(dict(frame=f,rgb_mae=mae))
 on=Image.open(root/'native-control-wave-on.png').convert('RGB');off=Image.open(root/'native-control-wave-off.png').convert('RGB');delta=sum(ImageStat.Stat(ImageChops.difference(on,off)).mean)/3
 dof_on=Image.open(root/'native-control-dof-on.png').convert('RGB');dof_off=Image.open(root/'native-control-dof-off.png').convert('RGB');dof_delta=sum(ImageStat.Stat(ImageChops.difference(dof_on,dof_off)).mean)/3
 info=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=sample_aspect_ratio','-of','json',str(v)],capture_output=True,check=True).stdout);sar=info['streams'][0]['sample_aspect_ratio']
 structure=r.get('structure',[]);g=r.get('geometry',{});edit=r.get('native_edit',{});source_errors=[float(np.linalg.norm(np.array(x['actual'])-x['observation']['source_native_xy'])) for x in r.get('source_projection',[])];held=r.get('source_heldout',{});held_error=float(np.linalg.norm(np.array(held['actual'])-held['source_native_xy']))
 checks=dict(native_dof_enabled=r['camera'].get('depth_of_field')==1,focus_linked_to_zoom=abs(r['camera'].get('focus_distance',-1)-r['camera']['zoom'])<.001 and r['camera'].get('focus_expression')=='cameraOption.zoom',native_aperture_5mm=abs(r['camera'].get('aperture',-1)-5*72/25.4)<.001,native_blur_100=r['camera'].get('blur_level')==100,actual_dof_control_difference=dof_delta>.01,request_camera_readback=camera_request_error<.001,independent_pal_camera=cal['max_independent_pal_camera_error']<.001,full_movie=code==0 and not stderr.strip() and not remaining and len(rows)==n,native_recursive_formula=len(r.get('trace',[]))==n and not errors and r.get('max_formula_error',999)<.001,native_expression_errors=not r.get('expression_errors'),native_projective_heldout=cal['max_heldout_error']<.01,native_projective_training=cal['max_training_error']<.01,actual_movie_wave_probes=not failures,native_checkpoints=all(x['rgb_mae']<2 for x in checkpoints),actual_wave_control_difference=delta>1,reopened_edit=r.get('project_reopened') is True and edit.get('kind')==('amplitude' if c['mode']=='controller' else 'base_x'),native3d_unparented_index=len(structure)==c['count'] and all(x['index']==i+1 and x['three_d'] and not x['parented'] and x['scale']==[1,80,100] and x['position_keys']==0 for i,x in enumerate(structure)),camera_below_bars=r.get('camera',{}).get('index')==c['count']+(2 if c['mode']=='controller' else 1),control_below_bars=r.get('control_index')==(c['count']+1 if c['mode']=='controller' else None),pal_geometry=g.get('width')==720 and g.get('height')==576 and g.get('fps')==25 and abs(g.get('pixel_aspect',0)-128/117)<1e-8,actual_movie_sar=sar=='128:117',media=not any(x['missing'] or abs(x['pixel_aspect']-128/117)>1e-8 for x in r.get('media',[])))
 result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,frames=len(rows),video_sha256=hashlib.sha256(v.read_bytes()).hexdigest(),calibration=cal,checkpoints=checkpoints,wave_control_mean_rgb_difference=delta,dof_control_mean_rgb_difference=dof_delta,source_camera_measurement=dict(calibration_points=len(source_errors),max_native_error=max(source_errors,default=None),heldout_native_error=held_error,status='measurement_only_not_aesthetic_acceptance'),visible_movie_probes=sum(x['visible_points'] for x in rows),found_movie_probes=sum(x['found_points'] for x in rows),measurements=rows,failures=failures,native_trace_failures=errors,limits=['Native camera calibration does not establish source camera identity','5centerline probes per bar per frame,5x5pixels,>=95% found; overlapping bars can share support','Source end points measured under UI handles; count/color/camera uncertainties retained','Technical pass does not confer human course-fidelity acceptance'])
 if not(c['amplitude']==40 and c['rate']==3 and c['spacing']==10 and c['delay']==.2 and c['camera'].get('status')!='explicit_mirrored_camera_variant'):
  result['source_camera_measurement']=dict(status='not_applicable_variant_inputs',reason='Source endpoints belong fixed40/3/10/0.2 scene; current inputs/camera differ, so current BAR projection errors are not source camera accuracy')
 (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='delayed-wave-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['measurements','failures']},indent=2));raise SystemExit(r['status']!='passed')
