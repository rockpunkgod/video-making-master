"""Verify a declared native flare VARIANT, never OpticalFlares/source visual identity."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def rgba(path):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-frames:v','1','-pix_fmt','rgba','-f','rawvideo','-'],capture_output=True,check=True,timeout=60)
 if len(r.stdout)!=720*576*4:raise ValueError('Unexpected native PNG dimensions')
 return r.stdout

def validate(root,video=None,output='cloud-quality.json'):
 root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';trace=native.get('trace',[]);samples=[];pixel_errors=[];max_alpha_error=0
 for image in sorted(root.glob('native-control-cloud-alpha-*.png')):
  f=int(image.stem.rsplit('-',1)[1]);point=trace[f]['point'];data=rgba(image);x,y=point;left,right=x-2+.5,x+2+.5;top,bottom=y-2+.5,y+2+.5;total=weight=0
  # Integrate the4x4rectangle with AE pixel-center convention (+.5 in bitmap box coordinates), including fractional edges.
  for yy in range(math.floor(top),math.ceil(bottom)):
   for xx in range(math.floor(left),math.ceil(right)):
    w=max(0,min(right,xx+1)-max(left,xx))*max(0,min(bottom,yy+1)-max(top,yy))
    if 0<=xx<720 and 0<=yy<576:total+=data[(yy*720+xx)*4+3]/255*w
    weight+=w
  measured=total/weight if weight else 0;expected=trace[f]['alpha'];error=abs(expected-measured);max_alpha_error=max(max_alpha_error,error);samples.append(dict(frame=f,point=point,native_sample=expected,rendered_alpha_mean=measured,error=error))
  if error>.005:pixel_errors.append(dict(frame=f,alpha_error=error))
 control=native['feedback_control'];on=rgba(root/'native-control-feedback-on.png');off=rgba(root/'native-control-feedback-off.png');cx,cy=trace[control['frame']]['point'];total=count=0;peak=0
 for y in range(max(0,round(cy)-64),min(576,round(cy)+64)):
  for x in range(max(0,round(cx)-64),min(720,round(cx)+64)):
   i=(y*720+x)*4
   for k in range(3):d=abs(on[i+k]-off[i+k]);total+=d;count+=1;peak=max(peak,d)
 feedback_mean=total/count if count else 0
 n=round(cfg['duration']*25)
 all_alpha=[];alpha_dir=root/'render/alpha';alpha_available=alpha_dir.is_dir() and len(list(alpha_dir.glob('frame_*.png')))==n
 if alpha_available:
  ar=subprocess.run(['ffmpeg','-v','error','-framerate','25','-start_number','0','-i',str(alpha_dir/'frame_%05d.png'),'-vf','alphaextract','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,timeout=120)
  if ar.returncode or ar.stderr.strip() or len(ar.stdout)!=n*720*576:raise ValueError('Complete native alpha sequence decode failed')
  for f,row in enumerate(trace):
   x,y=row['point'];left,right=x-2+.5,x+2+.5;top,bottom=y-2+.5,y+2+.5;total=weight=0
   for yy in range(math.floor(top),math.ceil(bottom)):
    for xx in range(math.floor(left),math.ceil(right)):
     w=max(0,min(right,xx+1)-max(left,xx))*max(0,min(bottom,yy+1)-max(top,yy))
     if 0<=xx<720 and 0<=yy<576:total+=ar.stdout[f*720*576+yy*720+xx]/255*w
     weight+=w
   measured=total/weight;error=abs(row['alpha']-measured);max_alpha_error=max(max_alpha_error,error);all_alpha.append(dict(frame=f,native_sample=row['alpha'],rendered_alpha_mean=measured,error=error))
   if error>.005:pixel_errors.append(dict(frame=f,alpha_error=error,coverage='all_native_alpha_frames'))
 decoded=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120);size=720*576*3;movie_checks=[]
 if decoded.returncode==0 and len(decoded.stdout)==n*size:
  for image in root.glob('native-still-*.png'):
   f=int(image.stem.rsplit('-',1)[1]);reference=rgba(image);actual=decoded.stdout[f*size:(f+1)*size];mae=sum(abs(actual[i*3+k]-reference[i*4+k]) for i in range(720*576) for k in range(3))/size;movie_checks.append(dict(frame=f,rgb_mae=mae))
 checks=dict(course_blending=native.get('cloud_screen') is True and native.get('sun_screen') is True,full_movie=decoded.returncode==0 and not decoded.stderr.strip() and len(decoded.stdout)==n*size,native_checkpoint_rgb=bool(movie_checks) and all(x['rgb_mae']<=3 for x in movie_checks),rendered_alpha_vs_sample=bool(samples) and not pixel_errors,alpha_varies=native.get('alpha_range',[0,0])[1]-native.get('alpha_range',[0,0])[0]>.05,native_mapping=native.get('max_formula_error',999)<.001 and native.get('native_frames_checked')==n,native_materialization=native.get('native_export_complete') is True and native.get('native_frames_rendered')==n and native.get('native_render_method')=='CompItem.saveFrameToPng',no_expression_errors=not native.get('expression_errors'),luma_matte=native.get('matte',{}).get('type_luma') is True and native['matte']['source_enabled'] is False,actual_feedback_pixel_effect=feedback_mean>.1 and peak>3,point_edit_saved=native.get('project_reopened') is True and abs(native['native_edit']['edited_point'][0]-native['native_edit']['original_point'][0]-12)<.001,media=not any(x['missing'] for x in native.get('media',[])),explicit_variant=native.get('original_course_status')=='blocked_OpticalFlares_missing' and cfg.get('implementation')=='native-lens-flare')
 r=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),frames=n,max_alpha_error=max_alpha_error,alpha_measurements=samples,all_frame_alpha_measurements=all_alpha,all_frame_alpha_checked=len(all_alpha),movie_checkpoint_rgb=movie_checks,feedback_roi_mean_rgb_difference=feedback_mean,feedback_roi_peak_difference=peak,errors=pixel_errors,scope='Native LensFlare VARIANT only; OpticalFlares original and GoldenSun preset NOT reproduced',limitations=['When render/alpha exists, every native frame alpha sampled; after intermediate cleanup only retained checkpoints can be rechecked. The JSON preserves the all-frame measurements; this is not whole-image visual fidelity.','Per-frame native trace read only after actual AE PNG rendering to materialize sampleImage','Movie checkpoint comparison against own native exports is technical encoding QA, not course fidelity','Appearance and optional PNG sweep are explicit adaptations'])
 (root/output).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');return r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='cloud-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['errors','alpha_measurements','movie_checkpoint_rgb','all_frame_alpha_measurements']},indent=2));raise SystemExit(r['status']!='passed')
