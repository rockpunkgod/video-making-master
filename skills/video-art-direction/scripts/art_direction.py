"""Small art-direction contracts; media playback/listening remain reviewer tasks."""
import argparse
import hashlib
import json
import math
import random
import secrets
import subprocess
from pathlib import Path


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError('Use a new versioned output; preserve prior evidence')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def brief_errors(brief):
    if not isinstance(brief, dict):
        return ['brief_not_object']
    errors = []
    for key in ['project', 'purpose', 'audience', 'selected_direction', 'motion_language', 'camera_language']:
        if not nonempty(brief.get(key)):
            errors.append('brief_missing_' + key)
    mode = brief.get('task_mode')
    if mode not in ['new_concept', 'existing_film_review', 'specified_direction']:
        errors.append('brief_task_mode')
    directions = brief.get('directions', [])
    if not isinstance(directions, list):
        return errors + ['directions_not_list']
    if mode == 'new_concept' and not 2 <= len(directions) <= 3:
        errors.append('new_concept_needs_2_or_3_directions')
    dimensions = ['treatment', 'space', 'camera', 'rhythm', 'composition', 'sound']
    ids = [v.get('id') for v in directions if isinstance(v, dict) and nonempty(v.get('id'))]
    if len(ids) != len(directions) or len(set(ids)) != len(ids):
        errors.append('direction_ids')
    if brief.get('selected_direction') not in ids:
        errors.append('selected_direction_missing')
    for direction in directions:
        if not isinstance(direction, dict):
            continue
        if not all(nonempty(direction.get(key)) for key in dimensions + ['bold_choice', 'tradeoff']):
            errors.append('direction_incomplete_' + str(direction.get('id')))
    for i, left in enumerate(directions):
        for right in directions[i + 1:]:
            if isinstance(left, dict) and isinstance(right, dict) and all(left.get(k) == right.get(k) for k in dimensions):
                errors.append('directions_only_cosmetically_different')
    fmt = brief.get('format', {})
    if not isinstance(fmt, dict) or not all(isinstance(fmt.get(k), (int, float)) and not isinstance(fmt.get(k), bool) and math.isfinite(fmt[k]) and fmt[k] > 0 for k in ['width', 'height', 'fps', 'duration_s']):
        errors.append('brief_format')
        return sorted(set(errors))
    style = brief.get('visual_style', {})
    if not isinstance(style, dict) or not style.get('colors') or not style.get('fonts') or not nonempty(style.get('composition_rule')):
        errors.append('brief_visual_style')
    sound = brief.get('sound', {})
    if not isinstance(sound, dict) or sound.get('intent') not in ['music_and_effects', 'dialogue_and_sound', 'intentional_silence'] or not nonempty(sound.get('strategy')):
        errors.append('brief_sound_strategy')
    if not brief.get('emotional_arc') or not brief.get('subtractions'):
        errors.append('brief_emotion_or_subtractions')
    shots = brief.get('shots', [])
    if not isinstance(shots, list):
        return errors + ['shots_not_list']
    cursor = 0
    for shot in shots:
        if not isinstance(shot, dict) or not all(nonempty(shot.get(k)) for k in ['focus', 'framing', 'movement', 'motivation', 'sound']):
            errors.append('shot_missing_viewing_intent')
            continue
        start, end = shot.get('start'), shot.get('end')
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in [start, end]) or start < 0 or end <= start or abs(start - cursor) > .001:
            errors.append('shot_timeline_gap_overlap_or_order')
        else:
            cursor = end
    if not shots or abs(cursor - fmt.get('duration_s', -100)) > .001:
        errors.append('shot_timeline_incomplete')
    budget = brief.get('iteration_budget', {})
    if not isinstance(budget, dict) or not isinstance(budget.get('max_rounds'), int) or isinstance(budget.get('max_rounds'), bool) or budget.get('max_rounds', 0) < 1 or not isinstance(budget.get('max_changes_per_round'), int) or not 1 <= budget.get('max_changes_per_round', 0) <= 3:
        errors.append('iteration_budget')
    return sorted(set(errors))


def plan(brief, registry=None):
    errors = brief_errors(brief)
    bindings = brief.get('skill_bindings', [])
    if registry is not None:
        catalog = {v['name']: v for v in registry['skills']}
        for binding in bindings:
            item = catalog.get(binding.get('name'))
            if item is None or item.get('status') == 'unimplemented':
                errors.append('unavailable_skill_' + str(binding.get('name')))
    return dict(status='invalid_brief' if errors else 'production_plan_ready', errors=errors,
                selected_direction=brief.get('selected_direction'), shots=brief.get('shots'),
                skill_bindings=bindings, artistic_status='pending',
                creative_distinctness='Declared differences need human/Agent judgment; string checks do not judge creativity',
                scope='Plan only; no AE/PR execution, render, playback or listening implied')


def exploration(seed=None):
    supplied = seed is not None
    seed = seed if supplied else secrets.token_hex(16)
    rng = random.Random(seed)
    axes = dict(space=['贴近材质与局部变化', '一个平面中的连续形变', '从个体进入群体的纵深', '固定观察点中的多层遮挡'],
                rhythm=['长镜头内改变密度', '短促提问后留一个完整回答', '保持一次动作的完整起停', '以安静而非新特效制造转折'],
                composition=['一个主焦点带动其余层退让', '让留白成为下一次运动的路径', '通过一次破格改变观看关系', '让同一形状承担开场与结尾'])
    samples = {key: rng.sample(values, 3) for key, values in axes.items()}
    return dict(kind='exploration_prompts_not_design_directions', seed=seed,
                seed_source='caller_replay' if supplied else 'system_entropy_secrets',
                prompts=[{key: values[i] for key, values in samples.items()} for i in range(3)],
                keep_locked='User/brand/content constraints; no randomized public seed label',
                next='Author2–3 genuinely different treatments, compare their expression and tradeoffs')


def probe_media(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, check=True)
    data = json.loads(result.stdout)
    video = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
    if video is None:
        raise ValueError('Input has no real video stream')
    num, den = video['avg_frame_rate'].split('/')
    return dict(duration_s=float(video.get('duration', data['format']['duration'])),
                width=video['width'], height=video['height'], fps=float(num) / float(den),
                audio_present=any(s['codec_type'] == 'audio' for s in data['streams']))


def packet(brief_path, video_path, out):
    brief = read(brief_path)
    errors = brief_errors(brief)
    if errors:
        raise ValueError('Invalid Brief: ' + ', '.join(errors))
    video = Path(video_path).resolve()
    info = probe_media(video)
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    fmt = brief['format']
    metadata_ok = info['width'] == fmt['width'] and info['height'] == fmt['height'] and abs(info['fps'] - fmt['fps']) < .01 and abs(info['duration_s'] - fmt['duration_s']) <= 1 / info['fps'] + .001
    sound_ok = info['audio_present'] or brief['sound']['intent'] == 'intentional_silence'
    decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(video), '-f', 'null', '-'], capture_output=True)
    technical = dict(status='passed' if metadata_ok and sound_ok and decode.returncode == 0 and not decode.stderr.strip() else 'failed',
                     video_sha256=sha(video), metadata_matches_brief=metadata_ok, required_audio_present=sound_ok,
                     full_decode=decode.returncode == 0 and not decode.stderr.strip(), stderr=decode.stderr.decode(errors='replace'))
    chosen = next(d for d in brief['directions'] if d['id'] == brief['selected_direction'])
    # Reviewer receives the selected artistic target, not rejected concepts, code or implementation history.
    clean = {key: brief[key] for key in ['project', 'purpose', 'audience', 'format', 'visual_style', 'motion_language', 'camera_language', 'emotional_arc', 'sound', 'shots']}
    clean['direction'] = {key: chosen[key] for key in ['treatment', 'space', 'camera', 'rhythm', 'composition', 'sound', 'bold_choice']}
    result = dict(schema_version=1, video_path=str(video), video_sha256=sha(video), media=info,
                  selected_brief=clean, brief_sha256=sha(brief_path), iteration_budget=brief['iteration_budget'],
                  technical_file='technical-observations.json', artistic_status='pending',
                  mandatory='Full-length1x continuous audiovisual playback and actual listening; screenshots/frames/metrics are not substitutes')
    write(out/'review-packet.json', result)
    write(out/'brief.json', clean)
    write(out/'technical-observations.json', technical)
    template = dict(video_sha256=result['video_sha256'], reviewer=dict(id=None, kind=None, was_implementer=None, received_code_history_or_scores=None),
                    playback=dict(kind='pending', speed=1, intervals=[], observation=''),
                    sound=dict(kind='pending', intervals=[], listening_conditions='', observation=''),
                    observations=[], priority_issues=[], iteration=dict(round=1, changes=[]), artistic_decision='pending')
    write(out/'review-template.json', template)
    (out/'reviewer-prompt.md').write_text(
        '# 独立声画评审\n\n只读取brief.json、此处原片和必要参考。不要读取代码、制作说明、历史评分或期望分。\n\n'
        + '原片：' + str(video) + '\n\nSHA256：' + result['video_sha256']
        + '\n\n请正常速度全长播放并实际试听；记录速度、时间区间和听音条件。先概括感受到的艺术方向，再按叙事/节奏、运动/镜头、焦点/文字、声音/声画给出有时间码的观察，最后只选1–3个最值得改的问题。优先考虑删减。不能观看或听音的项目保留pending，不用抽帧或响度代替。填写review-template.json的新副本；这份表格本身不证明观看发生。\n', encoding='utf-8')
    return result


def covered(intervals, duration, tolerance):
    if not isinstance(intervals, list) or not intervals:
        return False
    cursor = 0
    try:
        for start, end in sorted(intervals):
            if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in [start, end]) or start < 0 or end <= start or end > duration + tolerance or start > cursor + tolerance:
                return False
            cursor = max(cursor, end)
    except (ValueError, TypeError):
        return False
    return cursor >= duration - tolerance


def valid_interval(interval, duration, tolerance=.001):
    return (isinstance(interval, list) and len(interval) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in interval)
            and 0 <= interval[0] < interval[1] <= duration + tolerance)


def check_review(packet_path, review):
    packet_path = Path(packet_path)
    pack = read(packet_path)
    errors = []
    video = Path(pack['video_path'])
    if not video.is_file() or sha(video) != pack['video_sha256'] or review.get('video_sha256') != pack['video_sha256']:
        errors.append('stale_or_missing_video')
    # Re-probe the actual artifact. A hand-authored JSON true flag is insufficient.
    if video.is_file():
        try:
            actual = probe_media(video)
            if any(actual[k] != pack['media'][k] for k in ['width', 'height', 'audio_present']) or abs(actual['duration_s'] - pack['media']['duration_s']) > .04 or abs(actual['fps'] - pack['media']['fps']) > .01:
                errors.append('packet_media_mismatch')
        except (ValueError, subprocess.CalledProcessError):
            errors.append('actual_media_unreadable')
    technical = read(packet_path.parent/pack['technical_file'])
    if technical.get('status') != 'passed' or technical.get('video_sha256') != pack['video_sha256']:
        errors.append('technical_preflight_not_passed')
    duration = pack['media']['duration_s']
    tolerance = 1 / pack['media']['fps'] + .001
    view, sound = review.get('playback', {}), review.get('sound', {})
    if view.get('kind') != 'continuous_playback' or view.get('speed') != 1 or not covered(view.get('intervals'), duration, tolerance) or not nonempty(view.get('observation')):
        errors.append('full_normal_speed_motion_evidence_missing')
    if sound.get('kind') != 'listening' or not covered(sound.get('intervals'), duration, tolerance) or not nonempty(sound.get('listening_conditions')) or not nonempty(sound.get('observation')):
        errors.append('full_actual_listening_evidence_missing')
    who = review.get('reviewer', {})
    if not nonempty(who.get('id')) or who.get('kind') not in ['human', 'independent_agent'] or who.get('was_implementer') is not False or who.get('received_code_history_or_scores') is not False:
        errors.append('independent_review_missing_or_biased')
    observations = review.get('observations', [])
    if not isinstance(observations, list):
        observations = []
    for dimension in ['narrative_rhythm', 'motion_camera', 'focus_typography', 'sound_picture']:
        matching = [o for o in observations if isinstance(o, dict) and o.get('dimension') == dimension and nonempty(o.get('observation')) and nonempty(o.get('viewer_effect')) and valid_interval(o.get('interval'), duration, tolerance)]
        if not matching:
            errors.append('timecoded_observation_missing_' + dimension)
    issues = review.get('priority_issues', [])
    budget = pack['iteration_budget']
    if not isinstance(issues, list) or len(issues) > 3:
        errors.append('too_many_priority_issues')
    for issue in issues if isinstance(issues, list) else []:
        if not isinstance(issue, dict) or not all(nonempty(issue.get(k)) for k in ['id', 'impact', 'suggested_change']) or not valid_interval(issue.get('interval'), duration, tolerance):
            errors.append('priority_issue_not_actionable')
    iteration = review.get('iteration', {})
    round_number = iteration.get('round', 1)
    if not isinstance(round_number, int) or isinstance(round_number, bool) or round_number < 1:
        errors.append('invalid_iteration_round')
        round_number = 1
    changes = iteration.get('changes', [])
    if not isinstance(changes, list) or len(changes) > budget['max_changes_per_round']:
        errors.append('too_many_changes_this_round')
    decision = review.get('artistic_decision')
    if decision not in ['pending', 'needs_revision', 'approved']:
        errors.append('invalid_artistic_decision')
    if decision == 'approved' and issues:
        errors.append('approved_with_open_priority_issues')
    if errors:
        status, artistic = 'evidence_incomplete', 'pending'
    else:
        status, artistic = 'evidence_record_consistent', 'reviewer_approved' if decision == 'approved' else decision
    exhausted = round_number >= budget['max_rounds'] and decision == 'needs_revision'
    return dict(status=status, artistic_status=artistic, errors=sorted(set(errors)),
                next_action='stop_and_report_remaining_tradeoffs' if exhausted else ('revise_top_1_to_3_and_re_render_replay_listen' if artistic == 'needs_revision' else 'retain_evidence_or_obtain_missing_review'),
                iteration_budget_exhausted=exhausted, video_sha256=pack['video_sha256'],
                scope='Checks artifact binding and declared evidence consistency only; does not prove anyone watched/listened or certify aesthetic quality. Never sets Skill verified.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    ep = sub.add_parser('explore'); ep.add_argument('--seed'); ep.add_argument('--out', required=True, type=Path)
    pp = sub.add_parser('plan'); pp.add_argument('--brief', required=True, type=Path); pp.add_argument('--registry', type=Path); pp.add_argument('--out', required=True, type=Path)
    rp = sub.add_parser('packet'); rp.add_argument('--brief', required=True, type=Path); rp.add_argument('--video', required=True, type=Path); rp.add_argument('--out', required=True, type=Path)
    cp = sub.add_parser('check'); cp.add_argument('--packet', required=True, type=Path); cp.add_argument('--review', required=True, type=Path); cp.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    if args.command == 'explore':
        result = exploration(args.seed); write(args.out, result)
    elif args.command == 'plan':
        result = plan(read(args.brief), read(args.registry) if args.registry else None); result['brief_sha256'] = sha(args.brief); write(args.out, result)
    elif args.command == 'packet':
        result = packet(args.brief, args.video, args.out)
    else:
        result = check_review(args.packet, read(args.review)); write(args.out, result)
    print(json.dumps({k: v for k, v in result.items() if k in ['status', 'artistic_status', 'errors', 'video_sha256', 'seed_source']}, ensure_ascii=True))
    return 1 if result.get('status') in ['invalid_brief', 'evidence_incomplete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
