"""Independent movie pixel axes, manual replay coordinates and real native pointing evidence."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def decode_image(path,pix='rgb24'):
    return subprocess.run(['ffmpeg','-v','error','-i',str(path),'-frames:v','1','-pix_fmt',pix,'-f','rawvideo','-'],capture_output=True,check=True,timeout=60).stdout

def axis(points):
    n=len(points)
    if n<10:raise ValueError('Too few bright artwork pixels')
    mx=sum(x for x,y in points)/n;my=sum(y for x,y in points)/n
    xx=sum((x-mx)**2 for x,y in points)/n;yy=sum((y-my)**2 for x,y in points)/n;xy=sum((x-mx)*(y-my) for x,y in points)/n
    gap=math.sqrt((xx-yy)**2+4*xy*xy);major=(xx+yy+gap)/2;minor=max((xx+yy-gap)/2,1e-9)
    return math.degrees(.5*math.atan2(2*xy,xx-yy)),major/minor

def artwork(path):
    meta=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(path)],capture_output=True,check=True).stdout)['streams'][0];w,h=meta['width'],meta['height'];raw=decode_image(path,'rgba');points=[];opaque=0;radius=0
    for i in range(w*h):
        if raw[i*4+3]>128:
            opaque+=1;x,y=i%w,i//w;radius=max(radius,math.hypot(x+.5-w/2,y+.5-h/2))
            if raw[i*4]>170 and raw[i*4+1]>170:points.append((x,y))
    angle,ratio=axis(points)
    return dict(axis=angle,anisotropy=ratio,bright_fraction=len(points)/max(opaque,1),opaque_pixels=opaque,max_radius=radius,extent=max(w,h))

def pixels(data,w,h,box):
    x0,y0,x1,y1=box;points=[]
    for y in range(max(0,int(y0)),min(h,math.ceil(y1))):
        for x in range(max(0,int(x0)),min(w,math.ceil(x1))):
            i=(y*w+x)*3
            if data[i]>170 and data[i+1]>170:points.append((x,y))
    return axis(points)

def glyph_points(data,w,h,center,half=95):
    cx,cy=center;points=[]
    for y in range(max(0,int(cy-half)),min(h,math.ceil(cy+half))):
        for x in range(max(0,int(cx-half)),min(w,math.ceil(cx+half))):
            i=(y*w+x)*3
            if data[i]>170 and data[i+1]>170:points.append((x+.5-cx,y+.5-cy))
    return points

def glyph_template(reference,actual,rotation):
    # A near-isotropic lowercase a has an unstable PCA axis. Test its full directed
    # silhouette against the actual native zero-rotation export instead.
    ref={(round(x),round(y)) for x,y in reference};theta=math.radians(rotation);cs,sn=math.cos(theta),math.sin(theta);distances=[]
    offsets=sorted([(dx*dx+dy*dy,dx,dy) for dx in range(-4,5) for dy in range(-4,5)])
    for x,y in actual:
        u,v=round(cs*x+sn*y),round(-sn*x+cs*y);distance=6
        for d,dx,dy in offsets:
            if (u+dx,v+dy) in ref:distance=math.sqrt(d);break
        distances.append(distance)
    distances.sort();coverage=len(actual)/max(len(reference),1)
    return dict(mean=sum(distances)/max(len(distances),1),p95=distances[min(len(distances)-1,int(len(distances)*.95))] if distances else 6,coverage=coverage)

def replay(keys,t,field):
    if t<=keys[0]['time']:return keys[0][field]
    for a,b in zip(keys,keys[1:]):
        if t<=b['time']:
            u=(t-a['time'])/(b['time']-a['time']);return [a[field][j]+u*(b[field][j]-a[field][j]) for j in range(2)]
    return keys[-1][field]

def angle_error(a,b):return abs((a-b+90)%180-90)

def validate(root,video=None,output='pointing-quality.json'):
    root=Path(root);cfg=json.loads((root/'request.json').read_text(encoding='utf-8'));r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'));video=Path(video) if video else root/'final.mp4';w,h=640,480;n=round(cfg['duration']*30);scale=w/cfg['native_width'];trace=r['trace'];position_error=0;formula_error=0;grid_error=0
    for row in trace:
        f=row['frame'];tp=replay(cfg['keyframes'],f/30,'target');position_error=max(position_error,*[abs(tp[j]-row['target'][j]) for j in range(2)])
        for node in row['nodes']:
            p=node['position'];actual=math.degrees(math.atan2(p[1]-row['target'][1],p[0]-row['target'][0]))+cfg['offset'];formula_error=max(formula_error,abs(node['rotation']-actual))
            if cfg['mode']=='grid':
                i=node['index']-1;ex=[(i%cfg['columns']+.5)*cfg['native_width']/cfg['columns'],(i//cfg['columns']+.5)*cfg['native_height']/cfg['rows']];grid_error=max(grid_error,*[abs(p[j]-ex[j]) for j in range(2)])
            else:
                ep=replay(cfg['keyframes'],f/30,'follower');position_error=max(position_error,*[abs(p[j]-ep[j]) for j in range(2)])
    off=decode_image(root/'native-control-pointing-off.png');on=decode_image(root/'native-control-pointing-on.png');point=trace[30]['nodes'][0]['position'];half=95 if cfg['mode']=='letter' else 45;box=[point[0]*scale-half,point[1]*scale-half,point[0]*scale+half,point[1]*scale+half];feedback=sum(abs(a-b) for a,b in zip(off,on))/len(on)
    if cfg.get('asset'):local_axis=artwork(cfg['asset'])['axis']
    elif cfg['mode']=='grid':local_axis=0
    else:local_axis=None
    glyph_reference=glyph_points(off,w,h,[point[0]*scale,point[1]*scale]) if local_axis is None else None
    movie=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,timeout=120);size=w*h*3;full=movie.returncode==0 and not movie.stderr.strip() and len(movie.stdout)==n*size;measurements=[];templates=[];failures=[];max_axis_error=0;checkpoints=[]
    if full:
        for row in trace:
            f=row['frame'];data=movie.stdout[f*size:(f+1)*size]
            for node in row['nodes']:
                p=node['position'];idx=node['index']-1
                if cfg['mode']=='grid':
                    col=idx%cfg['columns'];rr=idx//cfg['columns'];box=[col*w/cfg['columns'],rr*h/cfg['rows'],(col+1)*w/cfg['columns'],(rr+1)*h/cfg['rows']]
                else:box=[p[0]*scale-95,p[1]*scale-95,p[0]*scale+95,p[1]*scale+95]
                if glyph_reference is not None:
                    metric=glyph_template(glyph_reference,glyph_points(data,w,h,[p[0]*scale,p[1]*scale]),node['rotation']);templates.append(dict(frame=f,**metric))
                    if metric['mean']>1.2 or metric['p95']>3 or not .75<=metric['coverage']<=1.25:failures.append(dict(frame=f,glyph_template=metric))
                    continue
                try:
                    observed,ratio=pixels(data,w,h,box);err=angle_error(observed,node['rotation']+local_axis);max_axis_error=max(max_axis_error,err);measurements.append(dict(frame=f,index=node['index'],axis_error=err,anisotropy=ratio))
                    if err>1.5 or ratio<2:failures.append(dict(frame=f,index=node['index'],error=err,anisotropy=ratio))
                except ValueError as e:failures.append(dict(frame=f,index=node['index'],error=str(e)))
        for p in sorted(root.glob('native-still-*.png')):
            f=int(p.stem.rsplit('-',1)[1]);ref=decode_image(p);actual=movie.stdout[f*size:(f+1)*size];mae=sum(abs(a-b) for a,b in zip(ref,actual))/size;checkpoints.append(dict(frame=f,rgb_mae=mae))
    keytime_error=max(abs(a-b['time']) for a,b in zip(r['target_key_times'],cfg['keyframes']))
    checks=dict(full_movie=full,all_frame_pixel_orientation=len(measurements)+len(templates)==n*(1 if cfg['mode']=='letter' else cfg['columns']*cfg['rows']) and not failures,native_checkpoint_rgb=bool(checkpoints) and all(x['rgb_mae']<=3 for x in checkpoints),source_formula=formula_error<.001 and r['max_formula_error']<.001 and r['native_frames_checked']==n,replay_position=position_error<.06,grid_index_position=grid_error<.001,quantized_key_times=len(r['target_key_times'])==len(cfg['keyframes']) and keytime_error<=1/30/1024,zero_rotation_keys=r['rotation_keyframes']==0,unparented_2d=r['all_unparented_2d'] is True,native_reopened=r['project_reopened'] is True and not r['expression_errors'],target_edit=abs(r['native_edit']['edited_target'][0]-r['native_edit']['original_target'][0]-11)<.001,actual_feedback_pixels=feedback>.01,media=not any(x['missing'] or abs(x.get('pixel_aspect',1)-1)>.001 for x in r['media']),native_wrapper_collapse=r['wrapper_collapse'] is True)
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),frames=n,pixel_axes_checked=len(measurements),pixel_glyph_frames_checked=len(templates),max_axis_error_degrees=max_axis_error if measurements else None,max_glyph_template_p95=max((x['p95'] for x in templates),default=None),max_replay_position_error=position_error,max_grid_position_error=grid_error,max_native_formula_error=formula_error,max_key_time_error_seconds=keytime_error,feedback_global_mean_rgb_difference=feedback,local_artwork_axis_degrees=local_axis,failures=failures,all_frame_pixel_measurements=measurements,all_frame_glyph_templates=templates,native_checkpoint_rgb=checkpoints,scope='Technical pointing/replay/editability only; source manual interaction, original artwork/font identity and exact UI repaint synchronization remain unverified',limitations=['Pixel PCA is an undirected axis modulo180 degrees; directional heading is defined by explicit offset and native transform formula. Lowercase a uses full directed native-zero-rotation silhouette matching, not unstable PCA.','PNG adapter currently tested for bright yellow/white elongated artwork inside40pixel diameter; dark/round artwork unsupported by axis validator','Input replay uses observed centers and authored linear interpolation, not source animation curves','Off/on pixel difference establishes actual effect, not aesthetic quality'])
    (root/output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--video',type=Path);p.add_argument('--output',default='pointing-quality.json');a=p.parse_args();r=validate(a.root,a.video,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ['all_frame_pixel_measurements','all_frame_glyph_templates','native_checkpoint_rgb','failures']},indent=2));raise SystemExit(r['status']!='passed')
