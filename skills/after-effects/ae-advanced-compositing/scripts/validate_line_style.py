"""Validate saved native line geometry, staggered animation and render consistency."""
import json
from pathlib import Path
from validate_radial import thumbnail

def validate(directory):
    root=Path(directory)
    cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
    r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    groups=r.get('groups',[])
    checks=dict(reopened=r.get('project_reopened') is True,expressions=r.get('expression_errors')==[],media=r.get('media')==[],
                source_layers=r.get('internal_count')==3 and len(groups)==2,adjustment=r.get('adjustment_layer') is True,
                frames=r.get('native_frames_checked')==480,edit=r.get('native_glow_edit')==dict(original=50,changed=51,restored=50))
    expected_effects=['ADBE Slider Control']*4+['ADBE Mirror','ADBE Tritone','ADBE Find Edges','ADBE CurvesCustom','ADBE HUE SATURATION']
    for i,(g,spec) in enumerate(zip(groups,cfg['groups'])):
        tag=f'group{i+1}_'
        edge=g.get('edge',[])
        checks[tag+'effects']=g.get('effect_chain')==expected_effects and len(edge)==2 and edge[0]==0 and abs(edge[1]-.1)<1e-6
        checks[tag+'controls']=g.get('parameters')==[spec['points'],spec['minimum'],spec['maximum'],spec['seed']]
        checks[tag+'color']=abs(g.get('hue',-9999)-spec['hue'])<1e-6 and all(abs(x-spec['mid']/255)<1e-6 for x in g.get('mid',[])[:3])
        start=cfg['second_start_frame']/30 if i else 0
        checks[tag+'timing']=abs(g.get('start',-999)-start)<1e-8 and abs(g.get('in_point',-999)-start)<1e-8 and g.get('trim_values')==[1,100] and len(g.get('trim_times',[]))==2 and all(abs(x-y)<1e-8 for x,y in zip(g['trim_times'],[start,start+cfg['trim_end_frame']/30]))
        trace=g.get('trim_trace',[])
        checks[tag+'animation']=g.get('monotonic') is True and len(trace)==150 and abs(trace[0]-1)<1e-6 and abs(trace[-1]-100)<1e-6 and any(1<x<100 for x in trace)
        paths=g.get('paths',[])
        geometry=len(paths)==cfg['path_count'] and g.get('stroke_width')==2
        for path in paths:
            vertices=path.get('vertices',[])
            geometry=geometry and len(vertices)==spec['points']+1 and path.get('closed') is False and vertices[0]==[0,0]
            for j,(a,b) in enumerate(zip(vertices,vertices[1:]),1):
                dx,dy=b[0]-a[0],b[1]-a[1]
                # Saved Shape coordinates are float32; subtracting vertices introduces subpixel rounding.
                geometry=geometry and spec['minimum']-.001<=dy<=spec['maximum']+.001 and (abs(abs(dx)-dy)<.001 if j%2==0 else abs(dx)<.001)
        checks[tag+'geometry']=geometry
    expected=[dict(threshold=65*2.55,radius=10,intensity=cfg['glow_intensity']),dict(threshold=20*2.55,radius=50,intensity=.2)]
    checks['glows']=len(r.get('glows',[]))==2 and all(abs(g.get(k,-999)-v)<1e-4 for g,e in zip(r['glows'],expected) for k,v in e.items())
    rows=[]
    for frame in cfg['checkpoints']:
        a=thumbnail(root/f'native-still-{frame}.png');b=thumbnail(root/'final.mp4',frame)
        error=sum(abs(x-y) for x,y in zip(a,b))/len(a)
        rows.append(dict(frame=frame,mean_luma_error_255=error,passed=error<=8))
    checks['native_render_checkpoints']=all(x['passed'] for x in rows)
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,checkpoints=rows,course_fidelity='unverified',scope='Native line geometry/effects/trim animation and codec only. Estimated curves/count/timing/first-group final state and inherited camera remain; no full-film or three-material claim.')
    (root/'scene-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
