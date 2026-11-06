"""Prepare guarded native UI/finalize JSX for an already open lab tracking attempt."""
import argparse
import json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();out=a.directory.resolve()
if not (out/'input.json').is_file() or not (out/'tracking-attempt.aep').is_file():raise ValueError('Expected generated tracking attempt')
guard="if(!app.project.file||app.project.file.fsName!==new File("+json.dumps((out/'tracking-attempt.aep').as_posix(),ensure_ascii=True)+").fsName)throw Error('Different native project');"
prefix="(function(){"+guard+"var c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='TRACKING_SOLVE')c=app.project.item(i);if(!c)throw Error('Missing tracking comp');"
(out/'show-ui.jsx').write_text(prefix+"c.time=0;for(var i=1;i<=c.numLayers;i++)c.layer(i).selected=false;var l=c.layer('ANALYSIS_SOURCE');l.selected=true;l.property('ADBE Effect Parade').property('ADBE 3D Tracker').selected=true;var v=c.openInViewer();v.maximized=true;v.views[0].options.zoom=1;app.activate();}());",encoding='utf-8')
encoder=(Path(__file__).parent/'json-encode.jsx').read_text(encoding='utf-8')
body=r'''
var camera=null,plane=null;for(var i=1;i<=c.numLayers;i++){var l=c.layer(i);if(l instanceof CameraLayer){if(camera)throw Error('Multiple cameras');camera=l;}else if(l.threeDLayer){if(plane)throw Error('Multiple reference planes');plane=l;}}
if(!camera||!plane)throw Error('No actual native camera and reference plane');
var t=plane.property('ADBE Transform Group');
var record={status:'camera_and_plane_created',camera_position_keys:camera.property('ADBE Transform Group').property('ADBE Position').numKeys,plane_position:t.property('ADBE Position').value,plane_orientation:t.property('ADBE Orientation').value,comp_frames:Math.round(c.duration*c.frameRate)};
c.openInViewer();app.project.save();var f=new File(__OUT__+'/native-plane.json');f.encoding='UTF-8';f.open('w');f.write(encode(record));f.close();
'''
(out/'finalize-plane.jsx').write_text(prefix+encoder+body.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=True))+'}());',encoding='utf-8')
print(out/'show-ui.jsx');print(out/'finalize-plane.jsx')
