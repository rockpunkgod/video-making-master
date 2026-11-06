(function(){
    function encode(value) {
        if(value===null)return 'null';
        if(typeof value==='string')return '"'+value.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';
        if(typeof value==='number'||typeof value==='boolean')return String(value);
        var entries=[],key;
        if(value instanceof Array){for(var z=0;z<value.length;z++)entries.push(encode(value[z]));return '['+entries.join(',')+']';}
        for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
        return '{'+entries.join(',')+'}';
    }
var cases=[{"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/square-baseline", "config": {"name": "square-baseline", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "count": 24, "delay_frames": 2, "z_spacing": 180, "size": 840, "stroke_width": 5, "color": [1, 0.06, 0.18], "rotation_degrees": 160, "camera_zoom": 1100, "shape": "square", "asset": null}}, {"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/triangle-variation", "config": {"name": "triangle-variation", "width": 1280, "height": 720, "fps": 24, "duration": 6, "count": 18, "delay_frames": 3, "z_spacing": 140, "size": 600, "stroke_width": 7, "color": [0.08, 0.8, 1], "rotation_degrees": -110, "camera_zoom": 950, "shape": "triangle", "asset": null}}, {"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/hexagon-portrait", "config": {"name": "hexagon-portrait", "width": 720, "height": 1280, "fps": 30, "duration": 5, "count": 30, "delay_frames": 1, "z_spacing": 120, "size": 650, "stroke_width": 4, "color": [1, 0.65, 0.12], "rotation_degrees": 210, "camera_zoom": 1000, "shape": "hexagon", "asset": null}}, {"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/asset-geometry", "config": {"name": "asset-geometry", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "count": 12, "delay_frames": 2, "z_spacing": 180, "size": 840, "stroke_width": 5, "color": [1, 0.06, 0.18], "rotation_degrees": 160, "camera_zoom": 1100, "shape": "square", "asset": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/fixtures/geometry.png"}}, {"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/asset-typography", "config": {"name": "asset-typography", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "count": 12, "delay_frames": 2, "z_spacing": 180, "size": 840, "stroke_width": 5, "color": [1, 0.06, 0.18], "rotation_degrees": 160, "camera_zoom": 1100, "shape": "square", "asset": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/fixtures/typography.png"}}, {"dir": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/runs/suite-20261106-091450/asset-texture", "config": {"name": "asset-texture", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "count": 12, "delay_frames": 2, "z_spacing": 180, "size": 840, "stroke_width": 5, "color": [1, 0.06, 0.18], "rotation_degrees": 160, "camera_zoom": 1100, "shape": "square", "asset": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/fixtures/texture.png"}}];var reportPath="E:/\u81ea\u5a92\u4f53/video-skills-lab/evaluations/motion-suite-001/native-editability.json";

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

}());