"""Package native Premiere picture + native WAV mix; never use the diagnostic reference mix."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory.resolve()
native=root/'native-picture-aac.mp4';final=root/'final.mp4';wav=root/'native-mix.wav'
if (root/'native-wav.json').is_file():receipt={'status':'executed','result':json.loads((root/'native-wav.json').read_text(encoding='utf-8-sig'))}
else:receipt=json.loads((root/'wav-export-transport/native-result.json').read_text(encoding='utf-8-sig'))
build=json.loads((root/'native-build.json').read_text(encoding='utf-8-sig'))
if receipt.get('status')!='executed' or receipt['result'].get('status')!='native_wav_exported':raise ValueError('Actual native WAV export receipt required')
if receipt['result']['sequence_id']!=build['sequence_id'] or not wav.is_file() or wav.stat().st_size!=receipt['result']['bytes']:raise ValueError('Native WAV source mismatch')
if native.exists():raise FileExistsError('Refusing existing packaged run; use new outputs')
if not final.is_file():raise FileNotFoundError('Native picture output missing')
archives=[]
for name in ['quality.json','audio-quality.json']:
    src=root/name;dest=root/name.replace('.json','-native-aac.json')
    if src.exists():
        if dest.exists():raise FileExistsError(dest)
        archives.append((src,dest))
final.rename(native)
for src,dest in archives:src.rename(dest)
command=['ffmpeg','-v','error','-n','-i',str(native),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',str(final)]
subprocess.run(command,capture_output=True,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'packaged_validation_pending','picture_source':native.name,'picture_sha256':sha(native),'audio_source':wav.name,'native_wav_sha256':sha(wav),'final_sha256':sha(final),'picture_reencoded':False,'audio_encoder':'FFmpeg AAC 320kbps from actual native Premiere WAV','diagnostic_reference_used_as_production':False,'reason':'Installed native Premiere H264/AAC preset introduced measured 1024-sample priming delay; native WAV has zero measured delay','native_sequence_id':build['sequence_id'],'command':command}
(root/'packaging.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='command'},indent=2))
