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

var cfg={"name": "COURSE_P09_DISPLACEMENT", "width": 1920, "height": 1080, "fps": 30, "duration": 5, "stage": "final", "seed": 165, "drift_speed": 310.0, "count": 48, "asset": "E:/自媒体/video-skills-lab/samples/course-reproduction-005/p09-typography-001/assets/input.png", "pos_min": [-1084, -630, 1930], "pos_max": [3130, 1950, 8890], "source": "BV1Yh4y1A7XT?p=9 00:40 Fill code; 08:35 position code; 09:06 final controls", "status": "candidate", "inferred_geometry": {"circle_diameter": 300, "rectangle_size": 270, "triangle_base": 311.7691453624, "triangle_height": 270}, "inferred_background": "224/255 gray sampled from compressed tutorial viewport, not read from source color dialog", "scope": "Source-method random 3D arrays, scalar drift in X only, and +value manual offset; exact source random pattern not guaranteed; PNG generalization, not source vector geometry", "asset_sha256": "3130efd93a8d60694178091ed3dc6cd54c043917c6e2668a25a51effe8198600"},out="E:/自媒体/video-skills-lab/samples/course-reproduction-005/p09-typography-001";
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Course comp missing');}
function slider(l,n,v){var fx=l.effect.addProperty('ADBE Slider Control');fx.name=n;fx.property(1).setValue(v);}
function point(l,n,v){var fx=l.effect.addProperty('ADBE Point3D Control');fx.name=n;fx.property(1).setValue(v);}
try{
 if(app.project&&app.project.numItems>0){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing project');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;
 var comp=app.project.items.addComp(cfg.name,1920,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[224/255,224/255,224/255];
 var ctrl=null;if(cfg.stage==='final'){ctrl=comp.layers.addNull();ctrl.name='controls';slider(ctrl,'seed',cfg.seed);slider(ctrl,'driftSpeed',cfg.drift_speed);point(ctrl,'Position Min',cfg.pos_min);point(ctrl,'Position Max',cfg.pos_max);}
 var originalAsset=null,assetComp=null;
 if(cfg.asset){originalAsset=app.project.importFile(new ImportOptions(new File(cfg.asset)));assetComp=app.project.items.addComp('ORIGINAL_INPUT',300,300,1,5,30);assetComp.comment='video-skills-lab:course-reproduction';var al=assetComp.layers.add(originalAsset),fit=100*300/Math.max(originalAsset.width,originalAsset.height);al.transform.scale.setValue([fit,fit]);al.transform.position.setValue([150,150]);}
 var expression='seed=thisComp.layer("controls").effect("seed")(1);\nseedRandom(seed,1);\nposMin=thisComp.layer("controls").effect("Position Min")(1);\nposMax=thisComp.layer("controls").effect("Position Max")(1);\npos=random(posMin,posMax);\n\n// add drift\ndrift=time*random(thisComp.layer("controls").effect("driftSpeed")(1));\npos+drift+value;';
 for(var i=0;i<cfg.count;i++){
  var layer=assetComp?comp.layers.add(assetComp):comp.layers.addShape();layer.name='ELEMENT_'+(i+1);layer.moveToEnd();
  if(!assetComp){var kind=i%3,group=layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');group.name=kind===0?'Circle':kind===1?'Square':'Triangle';var v=group.property('ADBE Vectors Group');
   if(kind===0){var shape=v.addProperty('ADBE Vector Shape - Ellipse');shape.property('ADBE Vector Ellipse Size').setValue([300,300]);}
   else if(kind===1){var shape=v.addProperty('ADBE Vector Shape - Rect');shape.property('ADBE Vector Rect Size').setValue([270,270]);shape.property('ADBE Vector Rect Roundness').setValue(0);}
   else{var path=v.addProperty('ADBE Vector Shape - Group'),s=new Shape();s.vertices=[[0,-135],[155.8845726812,135],[-155.8845726812,135]];s.inTangents=[[0,0],[0,0],[0,0]];s.outTangents=[[0,0],[0,0],[0,0]];s.closed=true;path.property('ADBE Vector Shape').setValue(s);}
   var fill=v.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').expression='seedRandom(5,1);\nrandom([1,1,1,1])';
  }
  if(cfg.stage==='final'){layer.threeDLayer=true;layer.transform.position.setValue([0,0,0]);layer.transform.position.expression=expression;}
  else layer.transform.position.setValue([[600,540],[950,540],[1295,540]][i]);
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='';for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();ctrl=cfg.stage==='final'?comp.layer('controls'):null;
 var errors=[],trace=[],maxError=0,maxColorDrift=0,manualEdit=null,speedEdit=null;
 if(cfg.stage==='final'){
  for(var i=2;i<=comp.numLayers;i++){
   var layer=comp.layer(i),p=layer.transform.position,original=p.expression;
   p.expression=original.replace(/pos\+drift\+value;$/,'pos;');var initial=p.valueAtTime(0,false);
   p.expression=original.replace(/pos\+drift\+value;$/,'[drift,0,0];');var velocity=p.valueAtTime(1,false)[0];p.expression=original;
   for(var axis=0;axis<3;axis++)if(initial[axis]<cfg.pos_min[axis]-1e-6||initial[axis]>cfg.pos_max[axis]+1e-6)errors.push('Random bounds failed '+layer.name);
   for(var f=0;f<150;f++){var actual=p.valueAtTime(f/30,false),want=[initial[0]+velocity*f/30,initial[1],initial[2]];for(var axis=0;axis<3;axis++)maxError=Math.max(maxError,Math.abs(actual[axis]-want[axis]));}
   if(p.expressionError)errors.push(layer.name+':'+p.expressionError);
   var rgba=null;if(!cfg.asset){var color=layer.property('ADBE Root Vectors Group').property(1).property('ADBE Vectors Group').property('ADBE Vector Graphic - Fill').property('ADBE Vector Fill Color');rgba=color.valueAtTime(0,false);for(var f=1;f<150;f++){var col=color.valueAtTime(f/30,false);for(var k=0;k<4;k++)maxColorDrift=Math.max(maxColorDrift,Math.abs(col[k]-rgba[k]));}if(color.expressionError)errors.push(color.expressionError);}
   trace.push({layer:layer.name,position_at_zero:initial,x_velocity:velocity,color_rgba:rgba});
  }
  if(maxError>1e-5||maxColorDrift>1e-6)errors.push('Source drift/color invariant failed');
  // Actual manual +value edit, save/reopen, restore; original AEP is never overwritten.
  var p=comp.layer(2).transform.position,before=p.valueAtTime(1,false);p.setValue([186,0,0]);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var after=comp.layer(2).transform.position.valueAtTime(1,false);manualEdit={before:before,after:after};
  if(Math.abs(after[0]-before[0]-186)>1e-5||Math.abs(after[1]-before[1])>1e-5||Math.abs(after[2]-before[2])>1e-5)errors.push('Manual +value offset failed');comp.layer(2).transform.position.setValue([0,0,0]);
  comp.layer('controls').effect('driftSpeed')(1).setValue(cfg.drift_speed===0?100:cfg.drift_speed*2);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var altered=comp.layer(2).transform.position.valueAtTime(1,false);speedEdit={original_speed:cfg.drift_speed,changed_speed:comp.layer('controls').effect('driftSpeed')(1).value,before:before,after:altered};
  var expectedShift=cfg.drift_speed===0?null:trace[0].x_velocity;if(expectedShift!==null&&Math.abs(altered[0]-before[0]-expectedShift)>1e-5)errors.push('Speed doubling failed');
  comp.layer('controls').effect('driftSpeed')(1).setValue(cfg.drift_speed);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var restored=comp.layer(2).transform.position.valueAtTime(1,false);for(var k=0;k<3;k++)if(Math.abs(restored[k]-before[k])>1e-5)errors.push('Restored project differs');manualEdit.restored_and_reopened=true;speedEdit.restored_and_reopened=true;
 }
 var missing=[];for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof FootageItem&&app.project.item(i).footageMissing)missing.push(app.project.item(i).name);if(missing.length)errors.push('Missing input media');
 var cameraCount=0;for(var i=1;i<=comp.numLayers;i++)if(comp.layer(i) instanceof CameraLayer)cameraCount++;
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,bits_per_channel:app.project.bitsPerChannel,default_camera:cameraCount===0,explicit_camera_layers:cameraCount,background:comp.bgColor,max_native_position_error:maxError,max_native_color_drift:maxColorDrift,trace:trace,manual_offset_edit:manualEdit,drift_speed_edit:speedEdit,missing_footage:missing,course_fidelity_status:'candidate_pending_reference_and_visual_review',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());