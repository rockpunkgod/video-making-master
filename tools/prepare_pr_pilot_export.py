import json
from pathlib import Path
root=Path('.').resolve();out=root/'samples/pr-pilot-001';preset='E:/自媒体/Adobe Premiere Pro 2026/MediaIO/systempresets/4E49434B_48323634/01 - Match Source - High bitrate.epr'
body=r'''(function(){var s=app.project.activeSequence;if(!s||s.name!=='LAB_SOUND_PILOT')throw Error('Wrong pilot sequence');var output=new File(__OUTPUT__),preset=new File(__PRESET__);if(output.exists||!preset.exists)throw Error('Existing output or missing installed native preset');var result=s.exportAsMediaDirect(output.fsName,preset.fsName,0);return {status:'export_returned',return_value:result,output_exists:output.exists,output_bytes:output.exists?output.length:0,width:s.frameSizeHorizontal,height:s.frameSizeVertical,timebase:s.timebase,end_ticks:s.end};}());'''
(out/'export-baseline.jsx').write_text(body.replace('__OUTPUT__',json.dumps((out/'baseline.mp4').as_posix(),ensure_ascii=False)).replace('__PRESET__',json.dumps(preset,ensure_ascii=False)),encoding='utf-8')
