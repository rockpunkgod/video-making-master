"""Compile the reviewed sound plan into native Premiere operations; no private QE API."""
import argparse
import json
import math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--empty-project',type=Path,required=True);ap.add_argument('--export-preset',type=Path,required=True);ap.add_argument('--audio-preset',type=Path,required=True);a=ap.parse_args()
out=a.directory.resolve();plan=json.loads((out/'plan.json').read_text(encoding='utf-8'))
if (out/'project.prproj').exists() or (out/'build.jsx').exists():raise FileExistsError('Refusing an existing native run')
if not all(p.is_file() for p in [a.empty_project,a.export_preset,a.audio_preset]):raise FileNotFoundError('Native blank project and installed picture/audio export presets required')
for clip in plan['audio_clips']:
    if not Path(clip['path']).is_file() or clip['source_in']!=0 or clip['duration']<=0:raise ValueError('Invalid audio plan or uncalibrated source in-point')
    if clip['track'] not in range(8):raise ValueError('Track outside declared native preset')
    keys={round(float(t),8):float(v) for t,v in clip['gain_keys']}
    if any(v<0 or v>2 for v in keys.values()):raise ValueError('Gain outside tested range')
    # PR26 reloads zero-ended audio segments with nonlinear intermediate values.
    # Preserve the requested linear amplitude ramp by sampling only those intervals
    # at <=1ms; unchanged/ordinary intervals retain their compact original keys.
    ordered=sorted(keys.items())
    for (t0,v0),(t1,v1) in zip(ordered,ordered[1:]):
        if min(v0,v1)==0 and max(v0,v1)>0:
            steps=max(1,math.ceil((t1-t0)/.001))
            for k in range(1,steps):
                t=round(t0+(t1-t0)*k/steps,8);keys[t]=v0+(v1-v0)*(t-t0)/(t1-t0)
    clip['gain_keys']=[[t,keys[t]] for t in sorted(keys)]
plan['envelope_compilation']='Zero-ended linear amplitude intervals sampled at <=1ms to bound PR26 saved/reopened interpolation changes; reference still uses intended amplitudes, not native output.'
(out/'compiled-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
body=r'''(function(){var out=__OUT__,plan=__PLAN__,base=new File(__BASE__),preset=new File(__PRESET__);
function time(seconds){var t=new Time();t.seconds=seconds;return t;}
function ticks(seconds){return String(Math.round(seconds*254016000000));}
function write(name,value){var f=new File(out+'/'+name);f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write production receipt');f.write(encode(value));f.close();}
function volume(clip){for(var i=0;i<clip.components.numItems;i++){var c=clip.components[i];if(c.matchName==='Internal Volume Stereo')return c.properties[1];}throw Error('Unsupported audio channel layout: expected inspected stereo Volume');}
function findItem(path){var expected=new File(path).fsName;for(var i=0;i<app.project.rootItem.children.numItems;i++){var item=app.project.rootItem.children[i];if(item.getMediaPath()===expected)return item;}throw Error('Native item not found: '+path);}
app.project.save();var opened=app.openDocument(base.fsName,true,true,true,true);
if(!app.project||new File(app.project.path).fsName!==base.fsName||app.project.rootItem.children.numItems!==0||app.project.sequences.numSequences!==0)throw Error('Expected original empty lab project after native open');
if(new File(out+'/project.prproj').exists||new File(out+'/final.mp4').exists)throw Error('Refusing existing output');
app.project.saveAs(new File(out+'/project.prproj').fsName);
var sequence=app.project.newSequence('LAB_LAYERED_SOUND',new File(out+'/sequence.sqpreset').fsName);sequence=app.project.activeSequence;
if(!sequence||sequence.name!=='LAB_LAYERED_SOUND'||sequence.audioTracks.numTracks!==8)throw Error('Native eight-track preset failed');
if(sequence.frameSizeHorizontal!==plan.width||sequence.frameSizeVertical!==plan.height)throw Error('Native frame dimensions differ');
var paths=[],seen={};for(var i=0;i<plan.picture_clips.length;i++){var p=new File(plan.picture_clips[i].path).fsName;if(!seen[p]){seen[p]=true;paths.push(p);}}
for(var i=0;i<plan.audio_clips.length;i++){var p=new File(plan.audio_clips[i].path).fsName;if(!seen[p]){seen[p]=true;paths.push(p);}}
if(!app.project.importFiles(paths,true,app.project.rootItem,false))throw Error('Native import failed');
for(var i=0;i<plan.picture_clips.length;i++){var spec=plan.picture_clips[i];sequence.videoTracks[0].overwriteClip(findItem(spec.path),ticks(spec.start));}
var audits=[];
for(var i=0;i<plan.audio_clips.length;i++){
 var spec=plan.audio_clips[i],track=sequence.audioTracks[spec.track];
 track.overwriteClip(findItem(spec.path),ticks(spec.start));
 var clip=null;for(var j=0;j<track.clips.numItems;j++)if(Math.abs(track.clips[j].start.seconds-spec.start)<(1/plan.fps+0.001)&&track.clips[j].projectItem.getMediaPath()===new File(spec.path).fsName)clip=track.clips[j];
 if(!clip)throw Error('Native inserted audio clip not found');
 // overwriteClip rounds insertion to a picture frame; explicit Time setters retain audio precision.
 clip.start=time(spec.start);clip.inPoint=time(spec.source_in);clip.outPoint=time(spec.source_in+spec.duration);clip.end=time(spec.start+spec.duration);clip.name='LAB_'+spec.role+'_'+i;
 if(Math.abs(clip.start.seconds-spec.start)>1/plan.audio_sample_rate||Math.abs(clip.end.seconds-spec.start-spec.duration)>1/plan.audio_sample_rate||Math.abs(clip.outPoint.seconds-spec.source_in-spec.duration)>1/plan.audio_sample_rate)throw Error('Native precise audio placement mismatch');
 var v=volume(clip);v.setTimeVarying(true);var checks=[];
 for(var k=0;k<spec.gain_keys.length;k++){
  var t=time(spec.gain_keys[k][0]);v.addKey(t);v.setValueAtKey(t,plan.native_unity_parameter*spec.gain_keys[k][1],false);v.setInterpolationTypeAtKey(t,0,false);
 }
 var keys=v.getKeys();
 if(!keys||keys.length!==spec.gain_keys.length)throw Error('Native key count mismatch: '+spec.role+' '+(keys?keys.length:0)+'/'+spec.gain_keys.length);
 var maxError=0;for(var k=0;k<spec.gain_keys.length;k++){var requested=plan.native_unity_parameter*spec.gain_keys[k][1];var observed=v.getValueAtKey(time(spec.gain_keys[k][0]));maxError=Math.max(maxError,Math.abs(requested-observed));}
 if(maxError>0.000001)throw Error('Native audio envelope value mismatch');
 audits.push({name:clip.name,role:spec.role,track:spec.track,start:clip.start.seconds,end:clip.end.seconds,in_point:clip.inPoint.seconds,keys:keys.length,maximum_parameter_error:maxError,volume_match_name:'Internal Volume Stereo'});
}
for(var i=0;i<plan.cuts.length;i++){var marker=sequence.markers.createMarker(plan.cuts[i]);marker.name='LAB_CUT_'+i;marker.comments='Transition event aligned to picture cut';}
app.project.save();
// Production must use the saved project, not transient in-memory interpolation.
app.project.closeDocument(1,0);app.openDocument(new File(out+'/project.prproj').fsName,true,true,true,true);
if(new File(app.project.path).fsName!==new File(out+'/project.prproj').fsName)throw Error('Saved production project did not reopen');
sequence=app.project.activeSequence;if(!sequence||sequence.audioTracks.numTracks!==8)throw Error('Saved native sequence missing');
var build={status:'built',project:app.project.path,sequence_name:sequence.name,sequence_id:sequence.sequenceID,audio_tracks:sequence.audioTracks.numTracks,video_clips:sequence.videoTracks[0].clips.numItems,audio_clips:audits,width:sequence.frameSizeHorizontal,height:sequence.frameSizeVertical,timebase:sequence.timebase,end_ticks:sequence.end};
build.render_after_saved_project_reopen=true;
write('native-build.json',build);
var exported=sequence.exportAsMediaDirect(new File(out+'/final.mp4').fsName,preset.fsName,0);
if(!new File(out+'/final.mp4').exists)throw Error('No native render output');
write('native-render.json',{status:'render_returned',return_value:exported,bytes:new File(out+'/final.mp4').length,export_preset:preset.fsName});
var audioPreset=new File(__AUDIO_PRESET__),audioOutput=new File(out+'/native-mix.wav');if(audioOutput.exists)throw Error('Existing native audio output');var audioExport=sequence.exportAsMediaDirect(audioOutput.fsName,audioPreset.fsName,0);
write('native-wav.json',{status:'native_wav_exported',return_value:audioExport,bytes:audioOutput.length,sequence_id:sequence.sequenceID});
return {status:'production_rendered',audio_tracks:sequence.audioTracks.numTracks,audio_clips:audits.length,video_clips:sequence.videoTracks[0].clips.numItems,project:app.project.path,render_return:exported};
}());'''
body=body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__PLAN__',json.dumps(plan,ensure_ascii=False)).replace('__BASE__',json.dumps(a.empty_project.resolve().as_posix(),ensure_ascii=False)).replace('__PRESET__',json.dumps(a.export_preset.resolve().as_posix(),ensure_ascii=False)).replace('__AUDIO_PRESET__',json.dumps(a.audio_preset.resolve().as_posix(),ensure_ascii=False))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
