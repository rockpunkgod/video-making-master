"""Native assembly conformance and codec consistency, separate from course aesthetics."""
import json
from pathlib import Path
from validate_radial import thumbnail


def validate(directory):
    root = Path(directory)
    cfg = json.loads((root / 'request.json').read_text(encoding='utf-8'))
    native = json.loads((root / 'receipt.json').read_text(encoding='utf-8-sig'))
    gradient = native.get('gradient', {})
    if (root / 'native-bg-audit.json').is_file():
        audit = json.loads((root / 'native-bg-audit.json').read_text(encoding='utf-8-sig'))
        if audit.get('project_reopened') and audit.get('status') == 'passed':
            gradient = audit
    layers = {row['name']: row for row in native.get('layers', [])}
    checks = dict(native_reopened=native.get('project_reopened') is True,
                  native_expression_errors=native.get('expression_errors') == [],
                  native_frame_coverage=native.get('native_frames_checked') == 480,
                  no_external_media=native.get('media') == [],
                  layer_count=len(layers) == 11)
    checks['native_background_blend'] = gradient.get('blend') == cfg['background_blend']
    for role, spec in cfg['layers'].items():
        row = layers.get('ROLE_' + role.upper(), {})
        checks[role + '_structure'] = (
            row.get('threeD') is True and row.get('collapse') == spec['collapse']
            and row.get('position') == [960, 540, spec['z']]
            and abs(row.get('inPoint', -99) - spec['start_frame'] / 24) < 1e-5)
    desired_order = ['Camera 1', 'ROLE_TITLE', 'ROLE_DOTS', 'ROLE_NOISE', 'ROLE_CONTOURS',
                     'ROLE_STREAKS', 'ROLE_POLAR', 'ROLE_LINES', 'ROLE_CORE',
                     'ROLE_RADIAL', 'ROLE_BACKGROUND']
    checks['layer_order'] = [row['name'] for row in native.get('layers', [])] == desired_order
    for role in ('POLAR', 'STREAKS', 'NOISE'):
        checks[role.lower() + '_white_key'] = layers.get('ROLE_' + role, {}).get('white_key') == dict(color=[1, 1, 1, 1], tolerance=0, softness=10)
    fade = native.get('radial_opacity_trace', [])
    checks['radial_fade'] = (len(fade) == 480 and all(v == 100 for v in fade[:29])
                             and all(v == 0 for v in fade[37:])
                             and all(a >= b for a, b in zip(fade, fade[1:])))
    edit = native.get('background_edit', {})
    checks['editable_gradient'] = (edit.get('before') == [1674, 824]
                                   and edit.get('changed') == [1675, 824]
                                   and edit.get('restored') == [1674, 824])
    rows = []
    for frame in (0, 24, 96, 144, 216, 240, 479):
        reference = thumbnail(root / f'native-still-{frame}.png')
        rendered = thumbnail(root / 'final.mp4', frame)
        error = sum(abs(a-b) for a, b in zip(reference, rendered)) / len(reference)
        rows.append(dict(frame=frame, mean_luma_error_255=error, passed=error <= 8))
    checks['native_render_checkpoints'] = all(row['passed'] for row in rows)
    report = dict(status='passed' if all(checks.values()) else 'failed', checks=checks,
                  checkpoints=rows, course_fidelity='unverified',
                  unresolved_title_behind_camera_frames=native.get('unresolved_title_behind_camera_frames'),
                  scope='Native structural/codec checks only. Title projection unresolved; later styling and three-material generalization not completed. Never label this a complete film.')
    (root / 'scene-quality.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
