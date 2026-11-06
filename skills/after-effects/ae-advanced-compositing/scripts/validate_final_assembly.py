"""Check native candidate structure separately from unresolved course fidelity."""
import json
from pathlib import Path

def validate(root):
    root = Path(root)
    r = json.loads((root / 'receipt.json').read_text(encoding='utf-8-sig'))
    cfg = json.loads((root / 'request.json').read_text(encoding='utf-8'))
    layers = {x['name']: x for x in r.get('layers', [])}
    checks = {
        'native_build': r.get('status') == 'built',
        'native_reopened': r.get('project_reopened') is True,
        'expression_sample_checks': r.get('expressions_checked', 0) > 0 and not r.get('expression_errors'),
        'root_layers': len(layers) == 19,
        'camera_parent': layers.get('Camera 1', {}).get('parent') == 'drift',
        'first_label_parent': all(layers.get(n, {}).get('parent') == 'T1_ctrl' for n in ['TECHNOLOGY', 'INTERNET', 'BIG DATA']),
        'camera_samples': len(r.get('camera_samples', [])) == 600,
        'title_in_front_at22': r.get('title_in_front_of_camera_at22') is True,
        'native_text_edit_restore': r.get('native_text_edit') == dict(original='BIG DATA', changed='EDIT TEST', restored='BIG DATA'),
        'self_contained_media': r.get('media') == [],
        'native_pngs': len(r.get('native_png_exports', [])) == len(cfg['checkpoints']) and all((root / n).is_file() for n in r.get('native_png_exports', [])),
    }
    result = dict(status='passed' if all(checks.values()) else 'failed', checks=checks,
                  scope='Native structure and sampled expressions only; expression evaluation is not claimed for every property on every frame',
                  course_fidelity='not_passed', visual_review='incomplete reconstruction',
                  unresolved=['Middle tunnel is too small in native checkpoints',
                              'Streak section fills frame more than available course reference',
                              'Exact final camera poses/ease and label animation are not recovered',
                              'Vig implementation not shown; inherited background retained',
                              'No three-material or parameter-variation suite for this branch'],
                  user_acceptance='not_requested', audio_sync='not_applicable_silent_visual_candidate')
    (root / 'scene-quality.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result
