import json
from pathlib import Path
root=Path('.').resolve();out=root/'samples/pr-pilot-001'
body=r'''(function(){var out=__OUT__;
if(app.project.rootItem.children.numItems!==0||app.project.sequences.numSequences!==0)throw Error('Expected original empty lab project');
if(new File(out+'/project.prproj').exists)throw Error('Refusing existing pilot');
var saved=app.project.saveAs(new File(out+'/project.prproj').fsName);
var paths=[new File(out+'/inputs/picture.mp4').fsName,new File(out+'/inputs/calibration.wav').fsName];
for(var i=0;i<paths.length;i++)if(!new File(paths[i]).exists)throw Error('Missing original pilot input');
var imported=app.project.importFiles(paths,true,app.project.rootItem,false);if(!imported)throw Error('Native import failed');
var picture=null,audio=null;for(var i=0;i<app.project.rootItem.children.numItems;i++){var item=app.project.rootItem.children[i];var path=item.getMediaPath();if(path===paths[0])picture=item;if(path===paths[1])audio=item;}
if(!picture||!audio)throw Error('Native imported item mismatch');
var sequence=app.project.createNewSequenceFromClips('LAB_SOUND_PILOT',[picture],app.project.rootItem);if(!sequence||!sequence.audioTracks)throw Error('Native sequence missing');
if(sequence.audioTracks.numTracks<1)throw Error('No native audio track');
sequence.audioTracks[0].overwriteClip(audio,'0');
var clip=sequence.audioTracks[0].clips[0],components=[];
for(var i=0;i<clip.components.numItems;i++){var component=clip.components[i],properties=[];for(var j=0;j<component.properties.numItems;j++){var p=component.properties[j],v;try{v=p.getValue();}catch(e){v=e.toString();}properties.push({name:p.displayName,value:v,type:typeof v,keyframe_supported:p.areKeyframesSupported()});}components.push({name:component.displayName,match_name:component.matchName,properties:properties});}
app.project.save();
return {status:'built',project:app.project.path,saved:saved,video_tracks:sequence.videoTracks.numTracks,audio_tracks:sequence.audioTracks.numTracks,audio_clips:sequence.audioTracks[0].clips.numItems,components:components,export_direct:typeof sequence.exportAsMediaDirect,sequence_id:sequence.sequenceID};
}());'''
(out/'build.jsx').write_text(body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)),encoding='utf-8')
