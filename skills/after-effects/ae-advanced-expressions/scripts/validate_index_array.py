"""Pillow pixel envelopes/probes plus saved native index/control evidence; no source-identity claim."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

def native_rgb(path):
    im=Image.open(path).convert('RGBA');return Image.alpha_composite(Image.new('RGBA',im.size,(0,0,0,255)),im).convert('RGB')

def profile_at(profile,t,field,default):
    if not profile:return default
    keys=profile['keyframes']
    if t<=keys[0]['time']:return keys[0][field]
    for a,b in zip(keys,keys[1:]):
        if t<=b['time']:
            u=(t-a['time'])/(b['time']-a['time']);return [x+(y-x)*u for x,y in zip(a[field],b[field])]
    return keys[-1][field]

def validate(root,video=None,output='array-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';n=round(cfg['duration']*25);w,h=640,480;trace=r['trace'];native_error=profile_error=rotation_error=0;observed_outside=0
    for row in trace:
        t=row['frame']/25;v=profile_at(cfg['controller_profile'],t,'values',cfg['values']) if cfg['layout']=='controller' else [64,32,48,24];profile_error=max(profile_error,*[abs(a-b) for a,b in zip(v,row['values'])])
        if cfg['point_profile']:
            target=profile_at(cfg['point_profile'],t,'target',None);profile_error=max(profile_error,*[abs(target[j]-row['target'][j]) for j in range(2)])
        for node in row['nodes']:
            index=node['index'];rr=math.ceil(index/cfg['columns']);col=index-(rr-1)*cfg['columns'];ex=[col*v[0]-v[1],rr*v[2]-v[3]];p=node['position'];native_error=max(native_error,*[abs(a-b) for a,b in zip(ex,p[:2])]);observed_outside+=int(not 0<=p[0]<320 or not 0<=p[1]<240)
            if row['target']:
                a=math.degrees(math.atan2(p[1]-row['target'][1],p[0]-row['target'][0]))+cfg['heading_offset'];rotation_error=max(rotation_error,abs(a-node['rotation']))
    support_points=None
    if cfg['asset']:
        art=Image.open(cfg['asset']).convert('RGBA');aw,ah=art.size;sc=25/max(aw,ah);support_points=[((x+.5-aw/2)*sc,(y+.5-ah/2)*sc) for y in range(ah) for x in range(aw) if art.getpixel((x,y))[3]>128];local_probe=cfg['art']['probe']
    else:local_probe=[0,0]
    movie=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=180);size=w*h*3;full=movie.returncode==0 and not movie.stderr.strip() and len(movie.stdout)==n*size;pixels=[];failures=[];max_bbox_error=0;probe_checked=0;max_axis_error=0;axis_count=0;checkpoints=[]
    if cfg['point_profile']:
        from validate_free_pointing import artwork,axis,angle_error
        local_axis=artwork(cfg['asset'])['axis']
    if full:
        for row in trace:
            f=row['frame'];im=Image.frombytes('RGB',(w,h),movie.stdout[f*size:(f+1)*size]);red,green,blue=im.split();mask=ImageChops.lighter(ImageChops.lighter(red,green),blue).point(lambda v:255 if v>40 else 0);bbox=mask.getbbox();extents=[];missed=0;visible_probes=0
            for node in row['nodes']:
                p=node['position'];theta=math.radians(node['rotation']);cs,sn=math.cos(theta),math.sin(theta)
                if support_points:
                    if cfg['point_profile']:
                        pts=[((p[0]+cs*x-sn*y)*2,(p[1]+sn*x+cs*y)*2) for x,y in support_points];box=[min(x for x,y in pts)-.5,min(y for x,y in pts)-.5,max(x for x,y in pts)+.5,max(y for x,y in pts)+.5]
                    else:
                        ab=cfg['art']['support_box'];box=[(p[0]+ab[0])*2,(p[1]+ab[1])*2,(p[0]+ab[2])*2,(p[1]+ab[3])*2]
                else:rad=cfg['circle_diameter'];box=[p[0]*2-rad,p[1]*2-rad,p[0]*2+rad,p[1]*2+rad]
                if box[2]>0 and box[3]>0 and box[0]<w and box[1]<h:extents.append([max(0,box[0]),max(0,box[1]),min(w,box[2]),min(h,box[3])])
                px=(p[0]+cs*local_probe[0]-sn*local_probe[1])*2;py=(p[1]+sn*local_probe[0]+cs*local_probe[1])*2
                if 1<=px<w-1 and 1<=py<h-1:
                    visible_probes+=1;probe_checked+=1;small=mask.crop((round(px)-1,round(py)-1,round(px)+2,round(py)+2));missed+=int(small.getbbox() is None)
                if cfg['point_profile']:
                    points=[]
                    for yy in range(max(0,round(p[1]*2)-28),min(h,round(p[1]*2)+29)):
                        for xx in range(max(0,round(p[0]*2)-28),min(w,round(p[0]*2)+29)):
                            color=im.getpixel((xx,yy))
                            if color[0]>170 and color[1]>170:points.append((xx,yy))
                    try:
                        angle,ratio=axis(points);error=angle_error(angle,node['rotation']+local_axis);axis_count+=1;max_axis_error=max(max_axis_error,error)
                        if error>2 or ratio<2:failures.append(dict(frame=f,index=node['index'],axis_error=error,anisotropy=ratio))
                    except ValueError as e:failures.append(dict(frame=f,index=node['index'],axis_error=str(e)))
            if row['target']:
                tx,ty=row['target'][:2];extents.append([max(0,(tx-10)*2),max(0,(ty-10)*2),min(w,(tx+10)*2),min(h,(ty+10)*2)])
            expected=[min(b[0] for b in extents),min(b[1] for b in extents),max(b[2] for b in extents),max(b[3] for b in extents)] if extents else None
            err=max(abs(a-b) for a,b in zip(expected,bbox)) if expected and bbox else (0 if expected==bbox else 999);max_bbox_error=max(max_bbox_error,err);pixels.append(dict(frame=f,expected_bbox=expected,observed_bbox=bbox,bbox_error=err,visible_probes=visible_probes,missed_probes=missed))
            if err>3 or missed or not visible_probes:failures.append(dict(frame=f,bbox_error=err,missed_probes=missed,visible_probes=visible_probes))
        for p in sorted(root.glob('native-still-*.png')):
            f=int(p.stem.rsplit('-',1)[1]);ref=native_rgb(p);actual=Image.frombytes('RGB',(w,h),movie.stdout[f*size:(f+1)*size]);mae=sum(ImageStat.Stat(ImageChops.difference(ref,actual)).mean)/3;checkpoints.append(dict(frame=f,rgb_mae=mae))
    feedback=sum(ImageStat.Stat(ImageChops.difference(native_rgb(root/'native-control-layout-off.png'),native_rgb(root/'native-control-layout-on.png'))).mean)/3
    geometry=r.get('geometry');geometry_ok=cfg['asset'] is not None or geometry is not None and geometry['solid_width']==320 and geometry['solid_height']==240 and geometry['mask_add'] is True and abs(geometry['anchor'][0]-160)<.001 and abs(geometry['vertices'][0][0]-160-cfg['circle_diameter']/2)<.001
    checks=dict(full_movie=full,all_frame_pixel_envelope_and_probes=len(pixels)==n and not failures,native_checkpoint_rgb=bool(checkpoints) and all(x['rgb_mae']<3 for x in checkpoints),native_formula=native_error<.001 and r['max_formula_error']<.001 and r['native_frames_checked']==n,profile_replay=profile_error<.06,composed_rotation=rotation_error<.001 and (not cfg['point_profile'] or axis_count==n*cfg['count']),native_source_geometry=geometry_ok,native_reopened=r['project_reopened'] is True and not r['expression_errors'],all_unparented_2d=r['all_unparented_2d'] is True,controller_last=cfg['layout']=='fixed' or r['control_index']==cfg['count']+(2 if cfg['point_profile'] else 1) and r['control_enabled'] is False,native_edit=r['native_edit']['kind']=='mask_radius' and abs(r['native_edit']['edited_vertex'][0]-r['native_edit']['original_vertex'][0]-1)<.001 or r['native_edit']['kind']=='controller_x_distance' and abs(r['native_edit']['edited']-r['native_edit']['original']-3)<.001,actual_feedback_pixels=feedback>.01,media=not any(x['missing'] or abs(x['pixel_aspect']-1)>.001 for x in r['media']))
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),frames=n,max_bbox_error_pixels=max_bbox_error,visible_probes_checked=probe_checked,composed_pixel_axes_checked=axis_count,max_axis_error_degrees=max_axis_error if axis_count else None,max_native_formula_error=native_error,max_profile_error=profile_error,max_rotation_error=rotation_error,native_offcanvas_centers_counted=observed_outside,feedback_global_mean_rgb_difference=feedback,all_frame_pixels=pixels,native_checkpoint_rgb=checkpoints,failures=failures,scope='Course index/ceil/column/four-slider behavior and actual editable outputs; source mask size/color inferred, manual replay/UI ghost timing not recovered',limitations=['Envelope/probe QA is not whole-image source pixel identity or aesthetic review','Positions remain unclamped; overlap/cropping in source is preserved','Controller replay includes explicitly inferred edge-motion values, not recovered source keyframes','Optional course33pointing/PNG material are explicit composition variants'])
    (root/output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='array-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['all_frame_pixels','native_checkpoint_rgb','failures']},indent=2));raise SystemExit(r['status']!='passed')
