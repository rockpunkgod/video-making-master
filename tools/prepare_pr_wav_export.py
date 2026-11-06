import json
from pathlib import Path
root=Path('.').resolve();out=root/'samples/pr-sound-suite-001/baseline-003';preset='E:/自媒体/Adobe Premiere Pro 2026/MediaIO/systempresets/3F3F3F3F_57415645/Waveform Audio 48kHz 16-bit.epr'
body=r'''(function(){var out=__OUT__,s=app.project.activeSequence;if(!s||s.name!=='LAB_LAYERED_SOUND')throw Error('Wrong native production sequence');var output=new File(out+'/native-mix.wav'),preset=new File(__PRESET__);if(output.exists||!preset.exists)throw Error('Existing output or missing installed audio preset');var value=s.exportAsMediaDirect(output.fsName,preset.fsName,0);return {status:'native_wav_exported',return_value:value,bytes:output.length,sequence_id:s.sequenceID};}());'''
(out/'export-native-wav.jsx').write_text(body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__PRESET__',json.dumps(preset,ensure_ascii=False)),encoding='utf-8')
