"""Verify an actual edited Premiere WAV against separately summed input PCM."""
import argparse,json
from pathlib import Path
import numpy as np
from validate_pr_sound import decode

ap=argparse.ArgumentParser();ap.add_argument('audit',type=Path);ap.add_argument('--original-case',type=Path,required=True);a=ap.parse_args()
plan=json.loads((a.audit/'edited-plan.json').read_text(encoding='utf-8'));n=round(plan['duration']*48000)
reference=np.zeros((n,2));music=np.zeros((n,2))
for c in plan['audio_clips']:
    start=round(c['start']*48000);count=round(c['duration']*48000);offset=round(c['source_in']*48000)
    pcm=decode(c['path'])[offset:offset+count];keys=np.asarray(c['gain_keys']);gain=np.interp(np.arange(count)/48000,keys[:,0],keys[:,1]);piece=pcm*gain[:,None]
    end=min(n,start+count);reference[start:end]+=piece[:end-start]
    if c['role'].lower()=='music':music[start:end]+=piece[:end-start]
actual=decode(a.audit/'edited-native-mix.wav')[:n];original=decode(a.original_case/'native-mix.wav')[:n]
def snr(signal,error):return float(20*np.log10(max(np.sqrt(np.mean(signal**2)),1e-15)/max(np.sqrt(np.mean(error**2)),1e-15)))
mix_snr=snr(reference,actual-reference)
# Original music minus half music equals half music; compare the actual render difference.
delta=original-actual;delta_snr=snr(music,delta-music)
receipt=json.loads((a.audit/'edit-audit.json').read_text(encoding='utf-8-sig'))
report={'status':'passed' if mix_snr>=35 and delta_snr>=35 and receipt['reopened_clips_checked']==len(plan['audio_clips']) else 'failed','edited_native_mix_snr_db':mix_snr,'actual_music_change_snr_db':delta_snr,'minimum_snr_db':35,'method':'actual saved-and-reopened PR gain edit and WAV export; compare both absolute PCM and original-minus-edited difference to independently summed source stems','native_receipt':receipt}
(a.audit/'edit-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
