import json,copy,xml.etree.ElementTree as ET
from pathlib import Path
root=Path('.').resolve();out=root/'samples/pr-eight-track-probe-001';out.mkdir(exist_ok=False)
base=Path('E:/自媒体/Adobe Premiere Pro 2026/Settings/SequencePresets/HD 1080p/HD 1080p 23.976 fps.sqpreset')
tree=ET.parse(base);s=tree.getroot().find('./SequencePreset[@ObjectID]');s.find('VideoFrameRate').text='10584000000';s.find('VideoFrameSize').text='0,0,960,540';s.find('PreviewVideoFrameSize').text='0,0,960,540';s.find('./Names/NameItem/Second').text='LAB 960x540 24fps eight stereo tracks';roles=['DIALOGUE','MUSIC','ROOM_A','ROOM_B','FOLEY','RISER','IMPACT','DETAIL'];original=json.loads(s.find('AudioTracks').text);tracks=[]
for role in roles:
 track=copy.deepcopy(original[0]);track['mName']=role;tracks.append(track)
tracks.append(copy.deepcopy(original[-1]));s.find('AudioTracks').text=json.dumps(tracks,separators=(',',':'));tree.write(out/'eight-track.sqpreset',encoding='utf-8',xml_declaration=True)
body=r'''(function(){var out=__OUT__;if(new File(out+'/project.prproj').exists)throw Error('Existing output');app.project.saveAs(new File(out+'/project.prproj').fsName);var result=app.project.newSequence('LAB_EIGHT_TRACK',new File(out+'/eight-track.sqpreset').fsName);var s=app.project.activeSequence;if(!s||s.name!=='LAB_EIGHT_TRACK')throw Error('Native preset did not create expected sequence');var tracks=[];for(var i=0;i<s.audioTracks.numTracks;i++)tracks.push(s.audioTracks[i].name);app.project.save();return {status:'native_preset_test',new_sequence_result:result,width:s.frameSizeHorizontal,height:s.frameSizeVertical,timebase:s.timebase,audio_tracks:s.audioTracks.numTracks,track_names:tracks};}());'''
(out/'build.jsx').write_text(body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)),encoding='utf-8')
(out/'provenance.json').write_text(json.dumps({'base_installed_preset':str(base),'changes':['24fps','960x540','8 named stereo tracks plus original master record'],'actual_count_requires_native_test':True},indent=2),encoding='utf-8')
