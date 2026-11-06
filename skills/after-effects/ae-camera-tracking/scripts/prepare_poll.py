"""Generate a read-only state probe for a specific native tracking project."""
import argparse
import json
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();root=a.directory.resolve()
if not (root/'input.json').is_file():raise FileNotFoundError('No tracking attempt metadata')
template=r'''
(function(){var out=__OUT__;var f=new File(out+'/solve-state.json');f.encoding='UTF-8';f.open('w');try{
if(!app.project.file||app.project.file.fsName!==new File(out+'/tracking-attempt.aep').fsName)throw Error('Different active project');
var c=app.project.activeItem;if(!(c instanceof CompItem)||c.name!=='TRACKING_SOLVE')throw Error('Different active composition');
var e=c.layer('ANALYSIS_SOURCE').property('ADBE Effect Parade').property('ADBE 3D Tracker');var label=e.property('ADBE 3D Tracker-0311').name;
var match=label.match(/-?\d+(?:[.,]\d+)?/);var ready=label.indexOf('%')===-1&&match!==null;
var error=ready?parseFloat(match[0].replace(',','.')):null;
var cameras=0,keys=0;for(var i=1;i<=c.numLayers;i++)if(c.layer(i) instanceof CameraLayer){cameras++;keys+=c.layer(i).property('ADBE Transform Group').property('ADBE Position').numKeys;}
f.write('{"status":"'+(ready?'solved_camera_and_composite_pending':'analyzing_or_unsolved')+'","average_error_pixels":'+error+',"camera_count":'+cameras+',"position_keys":'+keys+',"solve_method_value":'+e.property('ADBE 3D Tracker-0410').value+',"detailed_value":'+e.property('ADBE 3D Tracker-0036').value+'}');
}catch(err){f.write('{"status":"failed_probe"}');}f.close();}());
'''
(root/'poll.jsx').write_text(template.replace('__OUT__',json.dumps(root.as_posix(),ensure_ascii=True)),encoding='utf-8');print(root/'poll.jsx')
