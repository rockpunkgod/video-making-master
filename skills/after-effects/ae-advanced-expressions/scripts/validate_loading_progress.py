"""Movie bar extent, fixed spatial gradient, title pulse and native numeral checkpoints."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def raw(path,crop,pix='rgb24'):
 return subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf','format=rgb24,'+crop,'-pix_fmt',pix,'-f','rawvideo','-'],capture_output=True,timeout=120)
def validate(root,video=None,output='progress-quality.json'):
 root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));native=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';n=round(cfg['duration']*25)
 bar=raw(video,'crop=720:1:0:448');header=raw(video,'crop=580:90:70:210','gray');digits=raw(video,'crop=180:85:250:310');rows=[];errors=[];max_width_error=max_opacity_error=0;color_samples={x:[] for x in [120,250,400,600]};base_mass=None;digit_errors=[]
 sizes=[720*3,580*90,180*85*3];full=all(r.returncode==0 and not r.stderr.strip() and len(r.stdout)==n*size for r,size in zip([bar,header,digits],sizes))
 if full:
  for f in range(n):
   t=f/25;value=min(100,t*100/cfg['complete']);expected_right=cfg['bar_position'][0]+550*value/100;row=bar.stdout[f*sizes[0]:(f+1)*sizes[0]];active=[x for x in range(720) if max(row[x*3:x*3+3])>24]
   if value==0:
    if active:errors.append(dict(frame=f,error='Bar nonempty atzero'))
   elif not active:errors.append(dict(frame=f,error='Bar missing'))
   else:
    e=max(abs(active[0]-cfg['bar_position'][0]),abs(active[-1]+1-expected_right));max_width_error=max(max_width_error,e)
    if e>2:errors.append(dict(frame=f,error='Bar extent',measured=[active[0],active[-1]+1],expected=[cfg['bar_position'][0],expected_right]))
   for x in color_samples:
    if x+12<expected_right:color_samples[x].append([sum(row[(xx)*3+k] for xx in range(x-2,x+3))/5 for k in range(3)])
   title=header.stdout[f*sizes[1]:(f+1)*sizes[1]];black=min(title[:580]);mass=sum(v-black for v in title)
   if base_mass is None:base_mass=mass
   pulse=f%(2*cfg['pulse_frames']);expected_opacity=100-50*min(pulse,2*cfg['pulse_frames']-pulse)/cfg['pulse_frames'];measured_opacity=100*mass/base_mass if base_mass else 0;max_opacity_error=max(max_opacity_error,abs(measured_opacity-expected_opacity));rows.append(dict(frame=f,number_value=value,bar_right=active[-1]+1 if active else None,opacity_measured=measured_opacity,opacity_expected=expected_opacity))
  for image in root.glob('native-still-*.png'):
   f=int(image.stem.rsplit('-',1)[1])
   if f>=n:continue
   ref=raw(image,'crop=180:85:250:310');actual=digits.stdout[f*sizes[2]:(f+1)*sizes[2]]
   if ref.returncode or len(ref.stdout)!=sizes[2]:digit_errors.append(dict(frame=f,error='native numeral PNG decode failed'));continue
   mae=sum(abs(x-y) for x,y in zip(ref.stdout,actual))/sizes[2];digit_errors.append(dict(frame=f,rgb_mae=mae))
 color_drift={str(x):max(max(v[k] for v in values)-min(v[k] for v in values) for k in range(3)) if values else None for x,values in color_samples.items()}
 checks=dict(full_movie=full,bar_geometry=full and not errors,title_pulse=full and base_mass and max_opacity_error<=3,fixed_spatial_gradient=all(v is not None and v<=8 for v in color_drift.values()),native_numeral_checkpoints=bool(digit_errors) and all(x.get('rgb_mae',999)<=3 for x in digit_errors),native_reopened=native.get('project_reopened') is True,native_formula=native.get('max_formula_error',999)<.001 and native.get('native_frames_checked')==n,no_expression_errors=not native.get('expression_errors'),rawvalue_link_edited=native.get('native_edit',{}).get('after_complete_number')==70 and native.get('native_edit',{}).get('raw_restored')==100,left_anchor=native['bar']['anchor'][:2]==[0,25],title_font_compensation=bool(cfg['title_asset']) or native.get('title_scale',[])[:2]==cfg.get('font_compensation',[100,100]),separate_adjustment=native['adjustment']['is_adjustment'] is True and native['adjustment']['enabled'] is True,media=not any(x['missing'] for x in native.get('media',[])))
 result=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),frames=n if full else None,max_bar_error_pixels=max_width_error,max_title_opacity_error_percent=max_opacity_error,fixed_point_rgb_drift=color_drift,native_numeral_checkpoints=digit_errors,errors=errors,measurements=rows,limits=['Not original font identity or aesthetic acceptance','Native Numeral PNG comparison only at exported checkpoints; native numeric parameter separately checked everyframe','Fixed point color invariance is checked after the point is12pixels inside the growing bar','Movie uses raw720x576pixels with square SAR; native PAL pixel aspect retained in editable AEP'])
 (root/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='progress-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['errors','measurements','native_numeral_checkpoints']},indent=2));raise SystemExit(r['status']!='passed')
