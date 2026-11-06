
(function(){    function encode(value) {
        if(value===null)return 'null';
        if(typeof value==='string')return '"'+value.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';
        if(typeof value==='number'||typeof value==='boolean')return String(value);
        var entries=[],key;
        if(value instanceof Array){for(var z=0;z<value.length;z++)entries.push(encode(value[z]));return '['+entries.join(',')+']';}
        for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
        return '{'+entries.join(',')+'}';
    }

var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/evaluations/tracking-suite-001",cases=["E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/composite-001", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/composite-typography", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-gallery-001/solve-001/composite-pixel-sized", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-corridor-001/solve-calibrated-001/composite-pixel-sized"],results=[];
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
