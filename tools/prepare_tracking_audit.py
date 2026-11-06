import json
from pathlib import Path
root=Path('.').resolve();out=root/'evaluations/tracking-suite-001';out.mkdir(exist_ok=True)
cases=['samples/tracking-fixture-001/solve-calibrated-001/composite-001','samples/tracking-fixture-001/solve-calibrated-001/composite-typography','samples/tracking-gallery-001/solve-001/composite-pixel-sized','samples/tracking-corridor-001/solve-calibrated-001/composite-pixel-sized']
t=(root/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_text(encoding='utf-8');enc=t[t.index('    function encode'):t.index('    function write')]
body=r'''
(function(){__ENCODER__
var out=__OUT__,cases=__CASES__,results=[];
function write(v){var f=new File(out+'/native-editability.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
try{
if(app.project&&app.project.numItems>0)throw Error('Expected empty lab host');
for(var k=0;k<cases.length;k++){
 var path=cases[k];app.open(new File(path+'/project.aep'));var c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='TRACKING_SOLVE')c=app.project.item(i);
 if(!c)throw Error('Missing comp');var missing=[];for(var i=1;i<=app.project.numItems;i++){var it=app.project.item(i);if(it instanceof FootageItem&&it.file&&!it.file.exists)missing.push(it.file.fsName);}if(missing.length)throw Error('Missing inputs');
 var l=c.layer('LAB_TRACKED_OVERLAY'),s=l.property('ADBE Transform Group').property('ADBE Scale'),base=s.value;
 function width(){var min=Infinity,max=-Infinity;for(var j=0;j<4;j++){var p=l.property('ADBE Effect Parade').property('LAB_CORNER_'+j).property(1).valueAtTime(0,false);min=Math.min(min,p[0]);max=Math.max(max,p[0]);}return max-min;}
 var before=width();s.setValue([base[0]*1.1,base[1]*1.1,base[2]*1.1]);var edited=width();if(edited<before*1.08)throw Error('Native scale edit did not affect projection');s.setValue(base);var restored=width();if(Math.abs(before-restored)>0.001)throw Error('Scale not restored');
 var copy=out+'/editable-case-'+k+'.aep';if(new File(copy).exists)throw Error('Refusing stale audit copy');app.project.save(new File(copy));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(copy));
 c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='TRACKING_SOLVE')c=app.project.item(i);
 var camera=null;for(var i=1;i<=c.numLayers;i++)if(c.layer(i) instanceof CameraLayer)camera=c.layer(i);if(!camera)throw Error('Camera missing after reopen');
 var reopened=c.layer('LAB_TRACKED_OVERLAY').property('ADBE Transform Group').property('ADBE Scale').value;for(var j=0;j<3;j++)if(Math.abs(reopened[j]-base[j])>0.001)throw Error('Edit/reopen mismatch');
 results.push({case_path:path,missing_files:missing,original_width:before,edited_width:edited,restored_width:restored,scale_edit_applied:true,copy_reopened:true,camera_position_keys:camera.property('ADBE Transform Group').property('ADBE Position').numKeys,editable_copy:copy});
 app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}
app.newProject();write({status:'passed',cases:results});
}catch(e){write({status:'failed',error:e.toString(),line:e.line,cases:results});}
}());
'''
(out/'audit.jsx').write_text(body.replace('__ENCODER__',enc).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=True)).replace('__CASES__',json.dumps([(root/p).as_posix() for p in cases],ensure_ascii=True)),encoding='utf-8')
