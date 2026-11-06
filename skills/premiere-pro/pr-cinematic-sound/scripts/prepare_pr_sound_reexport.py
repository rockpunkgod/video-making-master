"""Explicit retry after a terminal render failure; preserve all failed render evidence."""
import argparse,json,shutil
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('case',type=Path);ap.add_argument('--export-preset',type=Path,required=True);ap.add_argument('--audio-preset',type=Path,required=True);a=ap.parse_args();root=a.case.resolve()
quality=json.loads((root/'picture-quality.json').read_text(encoding='utf-8'))
if quality['status']!='failed':raise ValueError('This recovery requires an observed terminal picture failure')
archive=root/'failed-media-pending-001'
if archive.exists():raise FileExistsError('Recovery already prepared; inspect existing state')
if not all(p.is_file() for p in [a.export_preset,a.audio_preset,root/'project.prproj']):raise FileNotFoundError('Native project and export presets required')
archive.mkdir()
for name in ['final.mp4','native-picture-aac.mp4','native-mix.wav','native-render.json','native-wav.json','packaging.json','quality.json','audio-quality.json','independent-reference.wav','picture-quality.json','picture-frame-ssim.txt','review-frames']:
    source=root/name
    if source.exists():shutil.move(str(source),str(archive/name))
body=r'''(function(){var out=__OUT__,project=new File(out+'/project.prproj');app.project.save();
app.openDocument(project.fsName,true,true,true,true);if(new File(app.project.path).fsName!==project.fsName)throw Error('Unexpected retry project');
var sequence=app.project.activeSequence;if(!sequence||sequence.audioTracks.numTracks!==8)throw Error('Missing native lab sequence');
for(var i=0;i<app.project.rootItem.children.numItems;i++)if(app.project.rootItem.children[i].isOffline())throw Error('Offline media; do not render');
function write(name,v){var f=new File(out+'/'+name);f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write retry receipt');f.write(encode(v));f.close();}
var picture=new File(out+'/final.mp4'),wav=new File(out+'/native-mix.wav');if(picture.exists||wav.exists)throw Error('Fresh export filenames required');
var result=sequence.exportAsMediaDirect(picture.fsName,new File(__PICTURE__).fsName,0);write('native-render.json',{status:'render_returned',return_value:result,bytes:picture.length,recovery:'same saved project after terminal Media pending failure; old artifacts archived'});
var audio=sequence.exportAsMediaDirect(wav.fsName,new File(__AUDIO__).fsName,0);write('native-wav.json',{status:'native_wav_exported',return_value:audio,bytes:wav.length,sequence_id:sequence.sequenceID});return {status:'native_reexported',picture_bytes:picture.length,audio_bytes:wav.length,project:app.project.path};}());'''
for key,value in [('__OUT__',root.as_posix()),('__PICTURE__',a.export_preset.resolve().as_posix()),('__AUDIO__',a.audio_preset.resolve().as_posix())]:body=body.replace(key,json.dumps(value,ensure_ascii=False))
(root/'reexport.jsx').write_text(body,encoding='utf-8');print(root/'reexport.jsx')
