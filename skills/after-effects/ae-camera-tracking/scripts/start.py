"""Prepare a native tracking attempt from a validated local video; this does not claim a solve."""
import argparse
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--solve-method',choices=['auto','typical','flat','tripod'],default='auto');ap.add_argument('--detailed',action='store_true');ap.add_argument('--fov',type=float);a=ap.parse_args()
source=a.input.resolve();out=a.out.resolve()
if not source.is_file():raise FileNotFoundError(source)
if out.exists():raise FileExistsError('Use a new output directory')
r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)],capture_output=True,check=True)
meta=json.loads(r.stdout);video=next(s for s in meta['streams'] if s['codec_type']=='video');fps=float(Fraction(video['avg_frame_rate']));duration=float(video.get('duration',meta['format'].get('duration',0)))
if not 1<=duration<=60 or not 1<=fps<=120:raise ValueError('Provide a 1-60 second single-shot clip with a supported frame rate')
if a.fov is not None and (not math.isfinite(a.fov) or not 5<=a.fov<=150):raise ValueError('fov must be finite degrees in [5,150]')
settings={'solve_method':['auto','typical','flat','tripod'].index(a.solve_method)+1,'detailed':int(a.detailed),'fov':a.fov}
out.mkdir(parents=True)
script=r'''
(function(){var out=__OUT__;var f=new File(out+'/attempt.txt');f.encoding='UTF-8';f.open('w');try{
if(app.project&&app.project.numItems>0)throw Error('Open an empty project; tracking does not discard existing work');
if(!app.project)app.newProject();var src=app.project.importFile(new ImportOptions(new File(__INPUT__)));
var c=app.project.items.addComp('TRACKING_SOLVE',src.width,src.height,1,src.duration,src.frameRate);c.comment='video-skills-lab:tracking-attempt';
var l=c.layers.add(src);l.name='ANALYSIS_SOURCE';var e=l.property('ADBE Effect Parade').addProperty('ADBE 3D Tracker');var settings=__SETTINGS__;
e.property('ADBE 3D Tracker-0410').setValue(settings.solve_method);e.property('ADBE 3D Tracker-0036').setValue(settings.detailed);
if(settings.fov!==null){e.property('ADBE 3D Tracker-0403').setValue(3);e.property('ADBE 3D Tracker-0414').setValue(settings.fov);}
l.selected=true;e.selected=true;c.openInViewer();
app.project.save(new File(out+'/tracking-attempt.aep'));f.writeln('effect_added; solve_and_camera_creation_pending');
}catch(err){f.writeln('ERROR '+err.toString());}f.close();}());
'''
script=script.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=True)).replace('__INPUT__',json.dumps(source.as_posix(),ensure_ascii=True)).replace('__SETTINGS__',json.dumps(settings))
(out/'start.jsx').write_text(script,encoding='utf-8');(out/'input.json').write_text(json.dumps({'source':source.as_posix(),'width':video['width'],'height':video['height'],'fps':fps,'duration':duration,'settings':settings},indent=2),encoding='utf-8')
print(out/'start.jsx')
