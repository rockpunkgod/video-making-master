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
var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/composite-001";

function write(name,value){var f=new File(out+'/'+name);f.encoding='UTF-8';f.open('w');f.write(encode(value));f.close();}
try{
 if(!app.project.file||app.project.file.fsName!==new File("E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/tracking-attempt.aep").fsName)throw Error('Different active tracking project');
 var c=app.project.activeItem;if(!(c instanceof CompItem)||c.name!=='TRACKING_SOLVE')throw Error('Expected native solve comp');
 var solid=null,camera=null;
 for(var i=1;i<=c.numLayers;i++){var l=c.layer(i);if(l instanceof CameraLayer){if(camera)throw Error('Multiple cameras');camera=l;}else if(l.threeDLayer){if(solid)throw Error('Multiple reference planes');solid=l;}}
 if(!solid||!camera)throw Error('Native tracked camera and plane required');
 var image=app.project.importFile(new ImportOptions(new File(out+'/inputs/overlay.png')));
 solid.replaceSource(image,false);solid.name='LAB_TRACKED_OVERLAY';
 solid.property('ADBE Transform Group').property('ADBE Anchor Point').setValue([image.width/2,image.height/2,0]);
 solid.property('ADBE Transform Group').property('ADBE Scale').setValue([100.0,100.0,100.0]);
 var probe=solid.property('ADBE Effect Parade').addProperty('ADBE Point Control');probe.name='LAB_PROJECTED_ANCHOR';
 probe.property(1).expression='var p=thisLayer.toComp(thisLayer.anchorPoint);[p[0],p[1]];';
 var cornerLocal=[[0,0,0],[image.width,0,0],[image.width,image.height,0],[0,image.height,0]];
 for(var corner=0;corner<4;corner++){var cp=solid.property('ADBE Effect Parade').addProperty('ADBE Point Control');cp.name='LAB_CORNER_'+corner;cp.property(1).expression='var p=thisLayer.toComp(['+cornerLocal[corner][0]+','+cornerLocal[corner][1]+',0]);[p[0],p[1]];';}
 var positions=[],corners=[];for(var frame=0;frame<Math.round(c.duration*c.frameRate);frame++){
  var xy=solid.property('ADBE Effect Parade').property('LAB_PROJECTED_ANCHOR').property(1).valueAtTime(frame/c.frameRate,false);positions.push([xy[0],xy[1]]);
  var quad=[];for(var corner=0;corner<4;corner++){var qxy=solid.property('ADBE Effect Parade').property('LAB_CORNER_'+corner).property(1).valueAtTime(frame/c.frameRate,false);quad.push([qxy[0],qxy[1]]);}corners.push(quad);
 }
 if(solid.property('ADBE Effect Parade').property('LAB_PROJECTED_ANCHOR').property(1).expressionError)throw Error('Projection expression failed');
 var fx=c.layer('ANALYSIS_SOURCE').property('ADBE Effect Parade').property('ADBE 3D Tracker');
 var errorLabel=fx.property('ADBE 3D Tracker-0311').name;
 write('projection-trace.json',{width:c.width,height:c.height,fps:c.frameRate,source_frames:positions.length,points:positions,corners:corners,native_error_label:errorLabel,position_key_count:camera.property('ADBE Transform Group').property('ADBE Position').numKeys});
 if(app.project.renderQueue.numItems!==0)throw Error('Unexpected render queue');
 var queue=app.project.renderQueue.items.add(c);var om=queue.outputModule(1),templates=om.templates,selected='';
 for(var t=0;t<templates.length;t++)if(/H\.264/.test(templates[t])&&/15 Mbps/.test(templates[t])){selected=templates[t];break;}
 if(!selected)throw Error('Native H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 var id=c.id;app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
 var reopened=app.project.itemByID(id);if(!reopened||!reopened.layer('LAB_TRACKED_OVERLAY'))throw Error('Native composite did not reopen');
 write('receipt.json',{status:'built',project_reopened:true,expression_errors:[],output_format:'mp4',selected_template:selected,native_camera:true,source:'flattened MP4 only',plane_source:'native tracker context menu',rendered:false});
}catch(e){write('receipt.json',{status:'failed',error:e.toString(),line:e.line});}

}());