"""Derive a local sequence preset from the user's installed native Adobe preset.
Never modify installation files or distribute the proprietary base preset by default.
"""
import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROLES=['DIALOGUE','MUSIC','ROOM_A','ROOM_B','FOLEY','RISER','IMPACT','DETAIL']

def sequence_preset(base,out,width=960,height=540,fps=24):
    tree=ET.parse(base);settings=tree.getroot().find('./SequencePreset[@ObjectID]')
    if settings is None:raise ValueError('Unsupported installed preset structure')
    settings.find('VideoFrameRate').text=str(round(254016000000/fps))
    settings.find('VideoFrameSize').text=f'0,0,{width},{height}'
    settings.find('PreviewVideoFrameSize').text=f'0,0,{width},{height}'
    settings.find('./Names/NameItem/Second').text=f'LAB {width}x{height} {fps}fps eight stereo tracks'
    # Native probe proved each AudioTracks record creates one track; no master record.
    original=json.loads(settings.find('AudioTracks').text);tracks=[]
    for role in ROLES:
        track=copy.deepcopy(original[0]);track['mName']=role;tracks.append(track)
    settings.find('AudioTracks').text=json.dumps(tracks,separators=(',',':'))
    tree.write(out,encoding='utf-8',xml_declaration=True)

