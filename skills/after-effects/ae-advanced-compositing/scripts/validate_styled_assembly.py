"""Check editable assembly data and native/render consistency, not aesthetics."""
import json
from pathlib import Path
from validate_radial import thumbnail


def validate(directory):
    root = Path(directory)
    cfg = json.loads((root / 'request.json').read_text(encoding='utf-8'))
    native = json.loads((root / 'receipt.json').read_text(encoding='utf-8-sig'))
    layers = {row['name']: row for row in native.get('layers', [])}
    expected_order = ['Camera 1', 'ROLE_TITLE', 'ROLE_CORE', 'ROLE_DOTS', 'ROLE_RADIAL',
                      'ROLE_NOISE', 'ROLE_POLAR', 'ROLE_CONTOURS', 'ROLE_STREAKS',
                      'ROLE_LINES', 'ROLE_BACKGROUND']
    internal = native.get('polar_internal', [])
    glow = native.get('polar_glow', {})
    style = native.get('radial_style', {})
    traces = native.get('opacity_traces', {})
    contour = native.get('contour_style', {})
    checks = dict(project_reopened=native.get('project_reopened') is True,
                  expression_errors=native.get('expression_errors') == [],
                  no_external_media=native.get('media') == [],
                  frame_coverage=native.get('native_frames_checked') == 480,
                  layer_order=[row['name'] for row in native.get('layers', [])] == expected_order,
                  core_source=layers.get('ROLE_CORE', {}).get('source') == 'COURSE_P16_CORE',
                  core_self_opacity=layers.get('ROLE_CORE', {}).get('opacity_expression') == 'transform.opacity',
                  fade_links=all(layers.get('ROLE_'+role, {}).get('opacity_expression') == 'thisComp.layer("ROLE_CORE").transform.opacity' for role in ('DOTS', 'RADIAL')),
                  linked_fade_error=native.get('max_linked_fade_error', 999) < 1e-5,
                  fade_trace_lengths=all(len(traces.get(role, [])) == 480 for role in ('core','dots','radial')),
                  noise_scale=layers.get('ROLE_NOISE', {}).get('scale') == [342,423,100],
                  polar_layer_count=len(internal) == 6,
                  polar_screen=all(row.get('screen') is True for row in internal),
                  polar_find_edges=all(row.get('invert') == 1 and row.get('effect_chain', [])[-2:] == ['ADBE Polar Coordinates', 'ADBE Find Edges'] for row in internal),
                  polar_external_chain=layers.get('ROLE_POLAR', {}).get('effect_chain') == ['ADBE Linear Color Key2', 'APC Colorama', 'ADBE Glo2'],
                  polar_black_key=native.get('polar_black_key') == [0,0,0,1],
                  polar_depth=layers.get('ROLE_POLAR', {}).get('position') == [960,540,-7000],
                  polar_start=abs(layers.get('ROLE_POLAR', {}).get('inPoint', -999)-cfg['polar_start_frame']/24) < 1e-5,
                  polar_glow_threshold=abs(glow.get('threshold', -999)-12.75) < .001,
                  polar_glow_radius=glow.get('radius') == 20,
                  polar_glow_intensity=abs(glow.get('intensity', -999)-cfg['polar_glow_intensity']) < .001,
                  native_edit=native.get('native_glow_radius_edit') == dict(original=20, changed=21, restored=20),
                  radial_hue=style.get('hue') == cfg['radial_hue'],
                  radial_lightness=style.get('lightness') == cfg['radial_lightness'],
                  radial_feather=style.get('feather') == [cfg['radial_feather']]*2,
                  radial_expansion=style.get('expansion') == cfg['radial_expansion'])
    checks.update(contour_effect_chain=contour.get('effect_chain') == ['ADBE Fill','ADBE Glo2'],
                  contour_white_fill=contour.get('fill') == [1,1,1,1],
                  contour_internal_red_preserved=contour.get('source_stroke_color') == [1,0,0,1],
                  contour_glow=contour.get('glow') == dict(threshold=153,radius=10,intensity=1),
                  contour_time_offset=contour.get('time_offset') == cfg['contour_time_offset'],
                  contour_z_keys=contour.get('z_key_values') == [0,cfg['contour_z_spacing']]
                      and contour.get('z_key_times') == [0,cfg['contour_z_end_frame']/30],
                  contour_trim_keys=contour.get('trim_key_values') == [0,100]
                      and contour.get('trim_key_times') == [0,cfg['contour_trim_end_frame']/30],
                  contour_z_monotonic=contour.get('z_monotonic') is True,
                  contour_frame_coverage=len(contour.get('z_trace', [])) == 210 and len(contour.get('trim_trace', [])) == 210,
                  contour_incoming_ease=abs(contour.get('incoming_influence', -999)-33.333333) < 1e-5
                      and contour.get('incoming_type') == '6613')
    rows = []
    for frame in cfg['checkpoints']:
        reference = thumbnail(root / f'native-still-{frame}.png')
        rendered = thumbnail(root / 'final.mp4', frame)
        error = sum(abs(a-b) for a,b in zip(reference,rendered)) / len(reference)
        rows.append(dict(frame=frame, mean_luma_error_255=error, passed=error <= 8))
    checks['native_render_checkpoints'] = all(row['passed'] for row in rows)
    report = dict(status='passed' if all(checks.values()) else 'failed', checks=checks,
                  checkpoints=rows, course_fidelity='unverified',
                  unresolved_title_behind_camera_frames=native.get('unresolved_title_behind_camera_frames'),
                  scope='Native structure, opacity links and sampled codec consistency. Approximate camera/mask and missing later styling do not establish course visual equivalence or completed film.')
    (root / 'scene-quality.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
