"""Compare rendered radial checkpoints to actual native PNGs, without claiming aesthetic fidelity."""
import json
import subprocess
from pathlib import Path


def thumbnail(path, frame=None):
    filters = ([f'select=eq(n\\,{frame})'] if frame is not None else []) + ['scale=160:90', 'format=gray']
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', ','.join(filters),
                             '-frames:v', '1', '-f', 'rawvideo', '-'], capture_output=True, timeout=120)
    if result.returncode or len(result.stdout) != 14400:
        raise RuntimeError('Checkpoint decode failed: ' + str(path))
    return result.stdout


def validate(directory):
    root = Path(directory)
    cfg = json.loads((root / 'request.json').read_text(encoding='utf-8-sig'))
    receipt = json.loads((root / 'receipt.json').read_text(encoding='utf-8-sig'))
    frames = round(cfg['duration'] * cfg['fps'])
    expected = sorted({0, min(round(cfg['fps']), frames-1), frames//2, frames-1})
    if cfg.get('name') == 'COURSE_P16_NOISE_STYLE':
        expected = sorted(set(expected) | {39, 60, 80})
    rows = []
    for frame in expected:
        image = root / f'native-still-{frame}.png'
        if not image.is_file():
            rows.append(dict(frame=frame, passed=False, reason='Native PNG missing'))
            continue
        native = thumbnail(image)
        rendered = thumbnail(root / 'final.mp4', frame)
        error = sum(abs(a-b) for a, b in zip(native, rendered)) / len(native)
        rows.append(dict(frame=frame, mean_luma_error_255=error, passed=error <= 8))
    coverage_key = 'native_frames_checked' if cfg.get('name') in {'COURSE_P15_POLAR', 'COURSE_P15_STREAKS', 'COURSE_P16_CORE'} else 'evolution_frames_checked'
    checks = dict(checkpoints=all(r['passed'] for r in rows),
                  native_evolution_coverage=receipt.get(coverage_key) == frames,
                  native_expression_errors=receipt.get('expression_errors') == [],
                  native_project_reopened=receipt.get('project_reopened') is True)
    if cfg.get('name') == 'COURSE_P15_POLAR':
        checks.update(native_layer_count=len(receipt.get('layers', [])) == cfg['count'],
                      native_offset=receipt.get('max_offset_error', 999) < 1e-5,
                      native_evolution=receipt.get('max_evolution_error', 999) < 1e-5,
                      native_z_spacing=receipt.get('max_z_error', 999) < 1e-5)
    if cfg.get('name') == 'COURSE_P15_STREAKS':
        checks.update(native_layer_count=len(receipt.get('layers', [])) == cfg['count'],
                      native_zero_drift=receipt.get('max_position_drift', 999) < 1e-5,
                      native_evolution=receipt.get('max_evolution_error', 999) < 1e-5,
                      native_scale=receipt.get('max_scale_error', 999) < 1e-5)
    if cfg.get('name') == 'COURSE_P16_NOISE_STYLE':
        checks.update(native_fade=receipt.get('max_fade_error', 999) < 1e-5,
                      native_disabled_layers=set(receipt.get('disabled_layers', [])) == {'FN 6', 'FN 7'},
                      native_effect_order=receipt.get('effect_chain') == ['ADBE Linear Color Key2', 'APC Colorama', 'ADBE Glo2'],
                      native_scale=receipt.get('scale') == cfg['noise_scale'],
                      native_glow_threshold=abs(receipt.get('glow', {}).get('threshold', -999)-255*.482) < .001,
                      native_glow_intensity=abs(receipt.get('glow', {}).get('intensity', -999)-cfg['glow_intensity']) < .001,
                      native_edit=receipt.get('native_glow_radius_edit') == dict(original=122, changed=123, restored=122))
    if cfg.get('name') == 'COURSE_P16_CORE':
        checks.update(native_count=receipt.get('shape_count') == cfg['count'],
                      native_position=receipt.get('max_position_error', 999) < 1e-5,
                      native_phase=receipt.get('max_phase_error', 999) < 1e-5,
                      native_matte=receipt.get('alpha_matte_linked') is True,
                      native_effect_order=receipt.get('effect_chain') == ['ADBE Tritone', 'CC Vector Blur', 'CC Lens'],
                      native_edit=receipt.get('native_phase_increment_edit') == dict(original=63, changed=64, restored=63))
    report = dict(status='passed' if all(checks.values()) else 'failed', checks=checks, checkpoints=rows,
                  tolerance='Mean absolute luma error <=8/255 on160x90 checkpoints; allows codec differences',
                  scope='Native/render consistency at sampled frames plus native evolution coverage; no course aesthetics or material-generalization claim')
    (root / 'scene-quality.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
