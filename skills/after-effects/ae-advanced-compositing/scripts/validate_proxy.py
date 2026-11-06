"""Check real native proxy persistence, editable sources, alpha and final render policy."""
import json,subprocess,statistics
from pathlib import Path
from validate_radial import thumbnail

def rgb(path):
    r=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf','scale=160:90,format=rgb24','-frames:v','1','-f','rawvideo','-'],capture_output=True,check=True)
    if len(r.stdout)!=43200:raise ValueError('RGB checkpoint dimensions differ')
    return r.stdout

def compare(a,b):
    bg=a[:3];total=sum(abs(x-y) for x,y in zip(a,b))/len(a);error=0;count=0
    for i in range(0,len(a),3):
        if any(abs(a[i+j]-bg[j])>5 for j in range(3)):
            error+=sum(abs(a[i+j]-b[i+j]) for j in range(3));count+=3
    foreground=error/count if count else 0
    return dict(mean_rgb_error_255=total,foreground_rgb_error_255=foreground,foreground_pixels=count//3,passed=total<=2 and foreground<=6)

def validate(directory):
    root=Path(directory)
    def read(n):return json.loads((root/n).read_text(encoding='utf-8-sig'))
    cfg=read('request.json');r=read('receipt.json');before=read('proxy-build.json');media=read('proxy-media.json');edit=r.get('original_edit',{})
    checks=dict(reopened=r.get('project_reopened') is True,alpha=r.get('proxy_has_alpha') is True and r.get('proxy_alpha_premultiplied') is True and r.get('proxy_premul_color')==[0,0,0],codec=media.get('status')=='passed',proxy_enabled=r.get('proxy_enabled') is True,source_structure=r.get('original_layers')==before.get('original_layers'),editable=edit.get('edited_reopened')==99 and edit.get('restored')==edit.get('original'),toggle=r.get('proxy_toggle')==dict(disabled_reopened=False,enabled_reopened=True),eligible=before.get('blocked_uses')==[],render_policy=r.get('render_settings',{}).get('Proxy Use')==('Use All Proxies' if cfg['final_policy']=='proxies' else 'Use No Proxies'),full_duration=r.get('native_frames_checked')==round(cfg['duration']*cfg['fps']),original_render_best=before.get('render_settings',{}).get('Quality')=='Best' and before.get('render_settings',{}).get('Resolution')=='Full',native_depth=before.get('output_settings',{}).get('Depth')=='Trillions of Colors+')
    rows=[]
    for backplate,frames in [('dark',cfg['checkpoints']),('white',cfg['white_checkpoints'])]:
        for frame in frames:
            suffix=f'white-{frame}' if backplate=='white' else str(frame)
            c=compare(rgb(root/f'native-still-original-{suffix}.png'),rgb(root/f'native-still-proxy-{suffix}.png'))
            rows.append(dict(frame=frame,backplate=backplate,**c))
    checks['proxy_alpha_color_equivalence']=all(x['passed'] for x in rows)
    final=[]
    for frame in cfg['checkpoints']:
        a=thumbnail(root/f'native-still-{frame}.png');b=thumbnail(root/'final.mp4',frame);error=sum(abs(x-y) for x,y in zip(a,b))/len(a)
        final.append(dict(frame=frame,mean_luma_error_255=error,passed=error<=8))
    checks['native_final_checkpoints']=all(x['passed'] for x in final)
    original=statistics.median(x['ms'] for x in before['original_png_timings']);proxy=statistics.median(x['ms'] for x in r['proxy_png_timings'])
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,alpha_color_checkpoints=rows,final_checkpoints=final,timing=dict(original_median_ms=original,proxy_median_ms=proxy,ratio=original/proxy if proxy else None,cache_purge_confirmed=before['purge_available'] and r['purge_available'],scope='Selected native PNG exports, includes compression/wait/IO; not interactive playback FPS or a general speed guarantee'),course_fidelity='unverified final-film; proxy workflow candidate',scope='Native full-size alpha proxy workflow only; original complex component remains editable; QA dark/white backplates are explicit test adaptations')
    (root/'scene-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
