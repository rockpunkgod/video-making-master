"""Native tunnel structure and codec checks; does not assert course equivalence."""
import json
from pathlib import Path
from validate_radial import thumbnail

def validate(directory):
    root = Path(directory)
    cfg = json.loads((root/'request.json').read_text(encoding='utf-8'))
    r = json.loads((root/'receipt.json').read_text(encoding='utf-8-sig'))
    edit = r.get('native_edit', {})
    checks = dict(reopened=r.get('project_reopened') is True,
                  no_expression_errors=r.get('expression_errors') == [],
                  no_external_media=r.get('media') == [],
                  first_disabled=r.get('first_contour',{}).get('enabled') is False,
                  null_static=r.get('null_position_keys') == 0,
                  null_position=r.get('null_position') == cfg['null_position'],
                  spacing_keys=r.get('z_spacing_keys') == [0,cfg['z_spacing']],
                  rotation_expression=r.get('rotation_expression') == 'time*'+str(cfg['rotation_speed']).removesuffix('.0')+'+value',
                  rotation_keys=r.get('rotation_keys') == [0,cfg['rotation_end']],
                  # Adobe JSON encoder emits15 significant digits. Compare time with
                  # sub-frame tolerance rather than Python binary-float equality.
                  key_times=all(len(r.get(name,[])) == 2 and all(abs(t-f/24)<1e-8 for t,f in zip(r[name],cfg['outer_frames']))
                                for name in ('rotation_key_times','opacity_key_times')),
                  opacity_keys=r.get('opacity_keys') == [100,0],
                  frame_coverage=r.get('native_frames_checked') == 480 and len(r.get('trace',[])) == 480,
                  rotation_formula=r.get('max_rotation_error',999) < 1e-5,
                  linear_fade=r.get('max_opacity_error',999) < 1e-5,
                  edit_reopened=edit.get('original') == cfg['null_position'] and edit.get('restored') == cfg['null_position']
                      and edit.get('changed') == [cfg['null_position'][0],cfg['null_position'][1],cfg['null_position'][2]+1])
    rows=[]
    for f in cfg['checkpoints']:
        a=thumbnail(root/f'native-still-{f}.png')
        b=thumbnail(root/'final.mp4',f)
        error=sum(abs(x-y) for x,y in zip(a,b))/len(a)
        rows.append(dict(frame=f,mean_luma_error_255=error,passed=error<=8))
    checks['native_render_checkpoints']=all(x['passed'] for x in rows)
    report=dict(status='passed' if all(checks.values()) else 'failed',checks=checks,checkpoints=rows,
                course_fidelity='unverified',scope='Course17 tunnel continuation only. Camera and graph approximate; later stylization and title unresolved.')
    (root/'scene-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
