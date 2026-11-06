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
    checks = dict(checkpoints=all(r['passed'] for r in rows),
                  native_evolution_coverage=receipt.get('evolution_frames_checked') == frames,
                  native_expression_errors=receipt.get('expression_errors') == [],
                  native_project_reopened=receipt.get('project_reopened') is True)
    report = dict(status='passed' if all(checks.values()) else 'failed', checks=checks, checkpoints=rows,
                  tolerance='Mean absolute luma error <=8/255 on160x90 checkpoints; allows codec differences',
                  scope='Native/render consistency at sampled frames plus native evolution coverage; no course aesthetics or material-generalization claim')
    (root / 'scene-quality.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
