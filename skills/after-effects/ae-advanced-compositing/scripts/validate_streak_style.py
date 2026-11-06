"""Check actual course17 streak native structure and rendered-frame consistency."""
import json
from pathlib import Path
from validate_radial import thumbnail

def validate(directory):
    root=Path(directory)
    cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
    r=json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    noise=r.get('noise',{})
    glows=r.get('glows',[])
    checks=dict(reopened=r.get('project_reopened') is True,
                expressions=r.get('expression_errors')==[],media=r.get('media')==[],
                seven_noise=r.get('internal_count')==9 and len(r.get('internal_rows',[]))==7,
                all_noise=all(x.get('effect_chain')==['ADBE Fractal Noise','ADBE Linear Color Key2'] and x.get('multiply') is True and x.get('width')==cfg['noise_width'] and x.get('height')==2270 and x.get('contrast')==2000 for x in r.get('internal_rows',[])),
                internal_effects=r.get('internal_chain')==['ADBE Fractal Noise','ADBE Linear Color Key2'],
                multiply=r.get('internal_multiply') is True,
                noise=all(noise.get(k)==v for k,v in dict(contrast=2000,width=cfg['noise_width'],height=2270,complexity=1).items()),
                outer_effects=r.get('outer_chain')==['ADBE CurvesCustom','ADBE Glo2','ADBE Glo2'],
                position=r.get('outer_position')==[960,540,cfg['depth']],
                collapse=r.get('collapse') is True,
                scale_keys=r.get('scale_values')==[[100,100,100],[0,100,100]],
                scale_times=len(r.get('scale_times',[]))==2 and all(abs(a-b/24)<1e-8 for a,b in zip(r['scale_times'],cfg['scale_frames'])),
                scale_continuous=r.get('scale_monotonic') is True,
                all_frames=r.get('native_frames_checked')==480 and len(r.get('scale_trace',[]))==480,
                edit=r.get('native_glow_edit')==dict(original=111,changed=112,restored=111))
    expected=[dict(threshold=29.4*2.55,radius=30,intensity=cfg['glow_intensity']),dict(threshold=56.9*2.55,radius=111,intensity=1)]
    checks['glows']=len(glows)==2 and all(abs(g.get(k,-999)-v)<1e-4 for g,e in zip(glows,expected) for k,v in e.items())
    rows=[]
    for f in cfg['checkpoints']:
        a=thumbnail(root/f'native-still-{f}.png');b=thumbnail(root/'final.mp4',f)
        error=sum(abs(x-y) for x,y in zip(a,b))/len(a)
        rows.append(dict(frame=f,mean_luma_error_255=error,passed=error<=8))
    checks['native_render_checkpoints']=all(row['passed'] for row in rows)
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,checkpoints=rows,
                course_fidelity='unverified',scope='Native streak structure, animation continuity and codec checks only. Estimated RGB curves/random layout/camera and pending lines/title remain.')
    (root/'scene-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
