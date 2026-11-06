import json
from pathlib import Path
root=Path('.').resolve();out=root/'samples/pr-sound-suite-001/baseline-003';plan=json.loads((out/'compiled-plan.json').read_text(encoding='utf-8'))
for name in ['native-build.json','native-render.json']:
 source=out/name;dest=out/(name+'.invalid-json.txt')
 if source.exists():
  if dest.exists():raise FileExistsError(dest)
  source.rename(dest)
source=out/'final.mp4';dest=out/'first-export.mp4'
if source.exists():
 if dest.exists():raise FileExistsError(dest)
 source.rename(dest)
body=r'''(function(){var out=__OUT__,plan=__PLAN__,s=app.project.activeSequence;
function t(seconds){var v=new Time();v.seconds=seconds;return v;}
function write(name,value){var f=new File(out+'/'+name);f.encoding='UTF-8';if(!f.open('w'))throw Error(f.error);f.write(encode(value));f.close();}
if(!s||s.name!=='LAB_LAYERED_SOUND'||s.audioTracks.numTracks!==8)throw Error('Wrong saved sound sequence');
var rows=[];for(var i=0;i<plan.audio_clips.length;i++){var spec=plan.audio_clips[i],name='LAB_'+spec.role+'_'+i,clip=null,track=s.audioTracks[spec.track];for(var j=0;j<track.clips.numItems;j++)if(track.clips[j].name===name)clip=track.clips[j];if(!clip)throw Error('Missing native saved clip');var volume=null;for(var j=0;j<clip.components.numItems;j++)if(clip.components[j].matchName==='Internal Volume Stereo')volume=clip.components[j].properties[1];if(!volume)throw Error('Missing native volume');var keys=volume.getKeys();if(keys.length!==spec.gain_keys.length)throw Error('Saved key count differs');var max=0;for(var k=0;k<spec.gain_keys.length;k++)max=Math.max(max,Math.abs(volume.getValueAtKey(t(spec.gain_keys[k][0]))-plan.native_unity_parameter*spec.gain_keys[k][1]));if(max>0.000001)throw Error('Saved envelope changed');if(Math.abs(clip.start.seconds-spec.start)>1/48000||Math.abs(clip.end.seconds-spec.start-spec.duration)>1/48000)throw Error('Saved audio timing differs');rows.push({name:name,role:spec.role,track:spec.track,start:clip.start.seconds,end:clip.end.seconds,in_point:clip.inPoint.seconds,keys:keys.length,maximum_parameter_error:max});}
write('native-build.json',{status:'built_reopened_and_recovered_json',project:app.project.path,sequence_name:s.name,sequence_id:s.sequenceID,audio_tracks:s.audioTracks.numTracks,video_clips:s.videoTracks[0].clips.numItems,audio_clips:rows,width:s.frameSizeHorizontal,height:s.frameSizeVertical,timebase:s.timebase,end_ticks:s.end,previous_json_preserved:true});
if(new File(out+'/final.mp4').exists)throw Error('Fresh native export required');var preset=new File(__PRESET__);var value=s.exportAsMediaDirect(new File(out+'/final.mp4').fsName,preset.fsName,0);write('native-render.json',{status:'render_returned',return_value:value,bytes:new File(out+'/final.mp4').length,export_preset:preset.fsName});return {status:'reopened_exported',native_keys_checked:true,render_return:value};}());'''
preset='E:/自媒体/Adobe Premiere Pro 2026/MediaIO/systempresets/4E49434B_48323634/01 - Match Source - High bitrate.epr'
(out/'reopen-audit-and-export.jsx').write_text(body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__PLAN__',json.dumps(plan,ensure_ascii=False)).replace('__PRESET__',json.dumps(preset,ensure_ascii=False)),encoding='utf-8')
