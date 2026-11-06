import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'samples/tracking-fixture-001/solve-typical-001';out=source/'plane-fit-001'
out.mkdir(exist_ok=False);(out/'input.json').write_text((source/'input.json').read_text(encoding='utf-8'),encoding='utf-8')
script=r'''
(function(){var expected=__SOURCE__,out=__OUT__;
if(!app.project.file||app.project.file.fsName!==new File(expected+'/tracking-attempt.aep').fsName||app.project.dirty)throw Error('Expected clean lab tracking project');
var c=app.project.activeItem;if(!(c instanceof CompItem)||c.name!=='TRACKING_SOLVE')throw Error('Wrong composition');
for(var i=c.numLayers;i>=1;i--){var l=c.layer(i);if(!(l instanceof CameraLayer)&&l.threeDLayer){if(l.name.indexOf('跟踪实底')!==0)throw Error('Unexpected user layer');l.remove();}}
c.time=0;for(var i=1;i<=c.numLayers;i++)c.layer(i).selected=false;c.layer('ANALYSIS_SOURCE').selected=true;c.layer('ANALYSIS_SOURCE').property('ADBE Effect Parade').property('ADBE 3D Tracker').selected=true;
var v=c.openInViewer();v.maximized=true;v.views[0].options.zoom=1;app.project.save(new File(out+'/tracking-attempt.aep'));
}());
'''
(out/'prepare.jsx').write_text(script.replace('__SOURCE__',json.dumps(source.as_posix(),ensure_ascii=True)).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=True)),encoding='utf-8');print(out/'prepare.jsx')
