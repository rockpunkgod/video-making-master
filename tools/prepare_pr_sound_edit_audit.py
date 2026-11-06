"""Build an actual native gain-edit/reopen/export audit on a new project copy."""
import argparse
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('case',type=Path)
ap.add_argument('--out',type=Path,required=True)
ap.add_argument('--audio-preset',type=Path,required=True)
a=ap.parse_args()
case=a.case.resolve(); out=a.out.resolve()
if out.exists():raise FileExistsError('Audit needs a fresh directory')
plan=json.loads((case/'compiled-plan.json').read_text(encoding='utf-8'))
if not (case/'project.prproj').is_file() or not a.audio_preset.is_file():raise FileNotFoundError('Native project/preset required')
out.mkdir(parents=True)
body=r'''(function(){var source=__SOURCE__,out=__OUT__,plan=__PLAN__,allowed=__ALLOWED__,stage='original';
function time(s){var t=new Time();t.seconds=s;return t;}
function write(v){var f=new File(out+'/edit-audit.json');f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write audit');f.write(encode(v));f.close();}
function open(path){var closing=[];for(var i=0;i<app.projects.numProjects;i++){var p=app.projects[i];for(var j=0;j<allowed.length;j++)if(new File(p.path).fsName===new File(allowed[j]).fsName){closing.push(p);break;}}for(var i=0;i<closing.length;i++){closing[i].save();closing[i].closeDocument(1,0);}app.openDocument(new File(path).fsName,true,true,true,true);if(new File(app.project.path).fsName!==new File(path).fsName)throw Error('Unexpected opened audit project');return app.project.activeSequence;}
function volume(c){for(var k=0;k<c.components.numItems;k++)if(c.components[k].matchName==='Internal Volume Stereo')return c.components[k].properties[1];throw Error('No inspected stereo volume');}
function inspect(seq,factor){
 if(!seq||seq.audioTracks.numTracks!==8)throw Error('Eight native tracks required');
 var checked=0;
 for(var i=0;i<plan.audio_clips.length;i++){
  var p=plan.audio_clips[i],track=seq.audioTracks[p.track],clip=null;
  for(var j=0;j<track.clips.numItems;j++)if(track.clips[j].name==='LAB_'+p.role+'_'+i)clip=track.clips[j];
  if(!clip||clip.projectItem.isOffline())throw Error('Missing/offline native media');
  if(new File(clip.projectItem.getMediaPath()).fsName!==new File(p.path).fsName)throw Error('Unexpected media path');
  var v=volume(clip),keys=v.getKeys();if(!keys||keys.length!==p.gain_keys.length)throw Error('Envelope key count changed');
  var f=p.role.toLowerCase()==='music'?factor:1;
  for(var k=0;k<p.gain_keys.length;k++){var observed=v.getValueAtKey(time(p.gain_keys[k][0])),expected=plan.native_unity_parameter*p.gain_keys[k][1]*f;if(Math.abs(observed-expected)>1e-6)throw Error('Saved envelope mismatch stage='+stage+' '+p.role+' key='+k+' observed='+observed+' expected='+expected+' factor='+factor);}
  checked++;
 }
 return checked;
}
var seq=open(source),checked=inspect(seq,1);
app.project.saveAs(new File(out+'/edited-project.prproj').fsName);
// saveAs can invalidate native Sequence/Clip handles; bind to the saved document.
seq=app.project.activeSequence;
var edits=0;
for(var i=0;i<plan.audio_clips.length;i++){var p=plan.audio_clips[i];if(p.role.toLowerCase()!=='music')continue;var track=seq.audioTracks[p.track];
for(var j=0;j<track.clips.numItems;j++){var clip=track.clips[j];if(clip.name!=='LAB_'+p.role+'_'+i)continue;var v=volume(clip);
for(var k=0;k<p.gain_keys.length;k++)v.setValueAtKey(time(p.gain_keys[k][0]),plan.native_unity_parameter*p.gain_keys[k][1]*0.5,false);edits++;}}
if(edits!==1)throw Error('Expected exactly one original music stem');
stage='immediate_edit';inspect(seq,0.5);
app.project.save();
// Switch documents before reopening; the test must read saved project data.
open(source);seq=open(out+'/edited-project.prproj');stage='reopened';var reopened=inspect(seq,0.5);
var wav=new File(out+'/edited-native-mix.wav');if(wav.exists)throw Error('Refusing prior output');
var result=seq.exportAsMediaDirect(wav.fsName,new File(__PRESET__).fsName,0);
if(!wav.exists||wav.length<1024)throw Error('No native edited audio');
var report={status:'native_edit_exported_numeric_check_pending',source_project:source,edited_project:app.project.path,original_clips_checked:checked,reopened_clips_checked:reopened,music_stems_edited:edits,music_gain_factor:0.5,other_stems_unchanged:true,export_return:result,output_bytes:wav.length};write(report);return report;
}());'''
allowed=[(case/'project.prproj').as_posix(),(out/'edited-project.prproj').as_posix()]
allowed += [p.as_posix() for p in out.parent.glob('*-edit*/edited-project.prproj')]
for key,value in [('__SOURCE__',(case/'project.prproj').as_posix()),('__OUT__',out.as_posix()),('__PLAN__',plan),('__PRESET__',a.audio_preset.resolve().as_posix()),('__ALLOWED__',allowed)]:
    body=body.replace(key,json.dumps(value,ensure_ascii=False))
(out/'audit.jsx').write_text(body,encoding='utf-8')
edited=json.loads(json.dumps(plan))
for clip in edited['audio_clips']:
    if clip['role'].lower()=='music':clip['gain_keys']=[[t,v*0.5] for t,v in clip['gain_keys']]
(out/'edited-plan.json').write_text(json.dumps(edited,indent=2,ensure_ascii=False),encoding='utf-8')
print(out/'audit.jsx')
