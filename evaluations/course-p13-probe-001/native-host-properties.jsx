(function(){// Character-wise escaping avoids this Premiere host's replacement-string backslash behavior.
function encode(value) {
    if(value===null)return 'null';
    if(typeof value==='string'){
        var out=String.fromCharCode(34);
        for(var i=0;i<value.length;i++){
            var c=value.charCodeAt(i);
            if(c===34||c===92)out+=String.fromCharCode(92,c);
            else if(c<32){var hex=c.toString(16);while(hex.length<4)hex='0'+hex;out+=String.fromCharCode(92)+'u'+hex;}
            else out+=value.charAt(i);
        }
        return out+String.fromCharCode(34);
    }
    if(typeof value==='number'){if(!isFinite(value))throw Error('Non-finite JSON number');return String(value);}
    if(typeof value==='boolean')return String(value);
    var entries=[],key;
    if(value instanceof Array){for(var i=0;i<value.length;i++)entries.push(encode(value[i]));return '['+entries.join(',')+']';}
    for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
    return '{'+entries.join(',')+'}';
}

var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-host-probe-004",report={status:'failed'},stage='ownership';
if(app.project&&app.project.dirty){var onlyProbe=true,probeCount=0;for(var z=1;z<=app.project.numItems;z++)if(app.project.item(z) instanceof CompItem){probeCount++;if(app.project.item(z).name!=='P13_HOST_PROBE')onlyProbe=false;}if(onlyProbe&&probeCount===1){app.project.save(new File(out+'/retained-failed001.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}}
function props(p){var rows=[];for(var i=1;i<=p.numProperties;i++){var q=p.property(i),row={name:q.name,matchName:q.matchName};if(q.propertyType===PropertyType.PROPERTY){try{var v=q.value;if(typeof v==='number'||typeof v==='string'||v instanceof Array)row.value=v;}catch(e){row.read_error=e.toString();}}else row.children=props(q);rows.push(row);}return rows;}
try{
 if(app.project&&app.project.numItems){var owned=true,has=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){has=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')owned=false;}if(!owned||!has||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();var comp=app.project.items.addComp('P13_HOST_PROBE',1920,1080,1,20,24);comp.comment='video-skills-lab:course-reproduction';
 var available=[];for(var i=0;i<app.effects.length;i++)if(/Key|Fractal Noise/i.test(app.effects[i].matchName))available.push({matchName:app.effects[i].matchName,displayName:app.effects[i].displayName});
 stage='effects';var l=comp.layers.addSolid([1,1,1],'PROBE',1080,1080,1,20);var fx=l.effect.addProperty('ADBE Linear Color Key2');var key=props(fx);var noise=props(l.effect.addProperty('ADBE Fractal Noise'));
 stage='import';var imported=app.project.importFile(new ImportOptions(new File("E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-002/p06-final-003/project.aep")));var found=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name==='COURSE_P06_TRIM_FINAL')found=app.project.item(i);
 if(!found)throw Error('Project import did not retain editable composition');var layer=comp.layers.add(found);layer.threeDLayer=true;layer.collapseTransformation=true;
 var cam=comp.layers.addCamera('Camera 1',[960,540]);cam.autoOrient=AutoOrientType.NO_AUTO_ORIENT;
 report={status:'built',host:app.version,project_reopened:true,available_effects:available,linear_key_properties:key,noise_properties:noise,project_import_type:imported instanceof FolderItem?'FolderItem':'other',imported_comp:found.name,imported_layers:found.numLayers,collapse_readback:layer.collapseTransformation,camera_zoom:cam.property('ADBE Camera Options Group').property('ADBE Camera Zoom').value};
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));report.project_reopened=app.project.file.fsName===new File(out+'/project.aep').fsName;
}catch(e){report={status:'failed',error:e.toString(),line:e.line,stage:stage,available_effects:available};if(app.project)app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));report.project_reopened=app.project.file.fsName===new File(out+'/project.aep').fsName;}
var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(report));f.close();
}());