"""Emit a native AE audit which exercises editability without saving changed projects."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];suite=ROOT/'samples/runs/suite-20261106-091450'
records=json.loads((suite/'results.json').read_text(encoding='utf-8'))
cases=[{'dir':(ROOT/r['run']).as_posix(),'config':json.loads((ROOT/r['run']/'request.json').read_text(encoding='utf-8'))} for r in records]
template=(ROOT/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_text(encoding='utf-8')
encoder=template[template.index('    function encode'):template.index('    function write')]
body=r'''
function safeClose(){
 if(app.project&&app.project.numItems>0){
  if(app.project.dirty)throw Error('Unsaved project; refusing audit');
  for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem && app.project.item(i).comment!=='video-skills-lab:ae-procedural-motion')throw Error('Non-lab project; refusing audit');
  app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
 }
}
var records=[];
try{
safeClose();
for(var c=0;c<cases.length;c++){
 var item=cases[c],cfg=item.config;app.open(new File(item.dir+'/project.aep'));
 var comp=null,missing=[];
 for(var i=1;i<=app.project.numItems;i++){
  var it=app.project.item(i);if(it instanceof CompItem && it.name===cfg.name)comp=it;
  if(it instanceof FootageItem && it.file && !it.file.exists)missing.push(it.file.fsName);
 }
 if(!comp)throw Error('Missing composition '+cfg.name);
 var layer=comp.layer('LAB_ELEMENT_0');var order=layer.property('ADBE Effect Parade').property('Order').property(1);
 var original=order.value;order.setValue(1);
 var changedZ=layer.property('ADBE Transform Group').property('ADBE Position').valueAtTime(1,false)[2];
 order.setValue(original);var restoredZ=layer.property('ADBE Transform Group').property('ADBE Position').valueAtTime(1,false)[2];
 var good=Math.abs(changedZ-cfg.z_spacing)<0.001 && Math.abs(restoredZ)<0.001;
 records.push({name:cfg.name,project_reopened:true,layers:comp.numLayers,expected_layers:cfg.count+2,editable_parameter_test:good,missing_assets:missing,changed_z:changedZ,restored_z:restoredZ,status:good&&missing.length===0&&comp.numLayers===cfg.count+2?'passed':'failed'});
 app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}
}catch(e){records.push({status:'failed',error:e.toString(),line:e.line});}
var file=new File(reportPath);file.encoding='UTF-8';file.open('w');file.write(encode(records));file.close();
'''
target=ROOT/'tools/audit-motion-suite.jsx';target.write_text('(function(){\n'+encoder+'var cases='+json.dumps(cases,ensure_ascii=True)+';var reportPath='+json.dumps((ROOT/'evaluations/motion-suite-001/native-editability.json').as_posix(),ensure_ascii=True)+';\n'+body+'\n}());',encoding='utf-8')
print(target)
