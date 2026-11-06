"""A concrete revision of the rejected baseline: quieter, bandwidth-limited room beds."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];source=root/'samples/pr-sound-suite-001/baseline-003';out=root/'samples/pr-sound-suite-001/baseline-quiet-001'
out.mkdir(exist_ok=False);shutil.copytree(source/'inputs',out/'inputs');shutil.copy2(source/'sequence.sqpreset',out/'sequence.sqpreset')
plan=json.loads((source/'compiled-plan.json').read_text(encoding='utf-8'))
for spec in [*plan['picture_clips'],*plan['audio_clips']]:spec['path']=str(out/Path(spec['path']).relative_to(source))
for clip in plan['audio_clips']:
    if clip['role']=='ambience':
        src=Path(clip['path']);dest=src.with_name(src.stem+'-quiet.wav')
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(src),'-af','lowpass=f=400','-c:a','pcm_s24le',str(dest)],capture_output=True,check=True)
        clip['path']=str(dest);clip['nominal_db']-=18
        clip['gain_keys']=[[t,v*10**(-18/20)] for t,v in clip['gain_keys']]
plan['variant']='baseline-quiet-001';plan['human_feedback']={'source':'user listening to baseline review.mp3','verdict':'not accepted','specific_issue':'continuous hiss/background noise'}
plan['revision']={'ambience_gain_delta_db':-18,'ambience_source_lowpass_hz':400,'dialogue_music_and_event_timing':'unchanged','subjective_status':'awaiting listening; technical checks do not establish aesthetic acceptance'}
(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
assets=[{'file':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (out/'inputs').iterdir() if p.is_file()]
(out/'assets.json').write_text(json.dumps(assets,indent=2),encoding='utf-8');print(out/'plan.json')
