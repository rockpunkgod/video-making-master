"""Check native candidate structure separately from unresolved course fidelity."""
import json
from pathlib import Path

def validate(root):
    root = Path(root)
    r = json.loads((root / 'receipt.json').read_text(encoding='utf-8-sig'))
    cfg = json.loads((root / 'request.json').read_text(encoding='utf-8'))
    layers = {x['name']: x for x in r.get('layers', [])}
    projection = r.get('projection', {})
    def close(a, b):
        if isinstance(a, list) and isinstance(b, list):
            return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
        return isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= .001
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
        'title_plane_before_lines': projection.get('title_plane_before_lines') is True,
        'saved_title_position': close(projection.get('title_position'), cfg.get('positions', {}).get('ROLE_TITLE')),
        'saved_lines_position': close(projection.get('lines_position'), cfg.get('positions', {}).get('ROLE_LINES')),
        'saved_title_scale': close(projection.get('title_scale'), cfg.get('scales', {}).get('ROLE_TITLE')),
        'saved_camera_rotation': close(projection.get('camera_rotation_keys'), cfg.get('camera_rotation')),
        'saved_dof_keys': close(projection.get('dof_keys'), cfg.get('dof')),
        'saved_blur_keys': close(projection.get('blur_keys'), cfg.get('blur_level')),
        'saved_mask_vertices': close(projection.get('mask_vertices'), cfg.get('radial_mask', {}).get('vertices')),
        'retained_mask_feather': close(projection.get('mask_feather'), [114, 114]),
        'retained_mask_expansion': close(projection.get('mask_expansion'), -33),
    }
    result = dict(status='passed' if all(checks.values()) else 'failed', checks=checks,
                  scope='Native structure and sampled expressions only; expression evaluation is not claimed for every property on every frame',
                  course_fidelity='not_evaluated', visual_review='requires_case_specific_visual_review',
                  unresolved=['Exact final camera poses/ease and label animation are not recovered',
                              'Vig implementation not shown; inherited background retained',
                              'No three-material or parameter-variation suite for this branch'],
                  user_acceptance='not_requested', audio_sync='not_applicable_silent_visual_candidate')
    (root / 'scene-quality.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result
