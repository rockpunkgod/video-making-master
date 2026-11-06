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

var out="E:/自媒体/video-skills-lab/samples/course-reproduction-008/p12-baseline-001",cfg={"name": "COURSE_P12_CYBER_LINES", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "points": 50, "paths": 12, "seed": 55, "step_min": 50, "step_max": 139, "motion_expectation": "static_layout", "status": "candidate", "observed": "09:22 complete createPath expression;09:54 Path1\u201312 + Stroke1; stroke2px;11:34 numPts50,min50,max139,seed55; Mirror540/540 angle0", "inferred": "LayerPosition[540,0], redFF0000 and background224/255 inferred from viewport, not read source Transform/color values", "scope": "Editable static path rig; no invented Trim Paths or time animation; course says animation is added in later final project"},errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function slider(l,n,v){var e=l.effect.addProperty('ADBE Slider Control');e.name=n;e.property(1).setValue(v);}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing composition');}
function prop(comp,n){return comp.layer('CYBER_LINES').property('ADBE Root Vectors Group').property(n).property('ADBE Vector Shape');}
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;var comp=app.project.items.addComp(cfg.name,1080,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[224/255,224/255,224/255];var layer=comp.layers.addShape();layer.name='CYBER_LINES';layer.transform.position.setValue([540,0]);slider(layer,'numPts',cfg.points);slider(layer,'Pos min',cfg.step_min);slider(layer,'Pos max',cfg.step_max);slider(layer,'seed',cfg.seed);
 var root=layer.property('ADBE Root Vectors Group');
 var expression='pts=effect("numPts")(1);\npos=[effect("Pos min")(1),effect("Pos max")(1)];\nseed=effect("seed")(1);\nvar x,y;\nvar c,mul;\nvar vertices=[[0,0]];\nfor(i=1;i<=pts;i++){\n seedRandom(i+seed,true);\n c=random();\n c>0.5?mul=1:mul=-1;\n oldEle=vertices[i-1];\n y=random(pos[0],pos[1]);\n x=y*mul;\n if(i%2==0){vertices[i]=oldEle+[x,y];}\n else{vertices[i]=oldEle+[0,y];}\n}\ncreatePath(vertices,[],[],0);';
 for(var i=1;i<=cfg.paths;i++){var path=root.addProperty('ADBE Vector Shape - Group');path.name='Path '+i;path.property('ADBE Vector Shape').expression=expression;}
 var stroke=root.addProperty('ADBE Vector Graphic - Stroke');stroke.property('ADBE Vector Stroke Color').setValue([1,0,0]);stroke.property('ADBE Vector Stroke Width').setValue(2);
 var mirror=layer.effect.addProperty('ADBE Mirror');mirror.property('ADBE Mirror-0001').setValue([540,540]);mirror.property('ADBE Mirror-0002').setValue(0);
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),selected='',templates=om.templates;for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();layer=comp.layer('CYBER_LINES');
 var storedMin=layer.effect('Pos min')(1).value,storedMax=layer.effect('Pos max')(1).value,unique={},records=[],maxGeometryError=0,maxPositionError=0;
 for(var j=1;j<=cfg.paths;j++){
  var path=prop(comp,j),first=path.valueAtTime(0,false),signature=encode(first.vertices);unique[signature]=true;var changes=0,maxError=0;
  for(var f=0;f<150;f++){
   var shape=path.valueAtTime(f/30,false),vertices=shape.vertices;if(encode(vertices)!==signature)changes++;
   if(shape.closed||vertices.length!==cfg.points+1)errors.push('Path closed or wrong point count');
   if(vertices[0][0]!==0||vertices[0][1]!==0)errors.push('Wrong starting vertex');
   for(var v=1;v<vertices.length;v++){
    var dx=vertices[v][0]-vertices[v-1][0],dy=vertices[v][1]-vertices[v-1][1],error=v%2===0?Math.abs(Math.abs(dx)-dy):Math.abs(dx);maxError=Math.max(maxError,error);
    var eps=Math.max(0.0001,Math.abs(vertices[v][0])*Math.pow(2,-21),Math.abs(vertices[v][1])*Math.pow(2,-21));
    if(error>eps||dy<storedMin-eps||dy>storedMax+eps)errors.push('Direction or segment length invariant failed');
    for(var d=0;d<2;d++)if(shape.inTangents[v][d]!==0||shape.outTangents[v][d]!==0)errors.push('Unexpected curved tangent');
   }
   var position=layer.transform.position.valueAtTime(f/30,false);maxPositionError=Math.max(maxPositionError,Math.abs(position[0]-540),Math.abs(position[1]));
  }
  if(changes||path.expressionError)errors.push('Temporal change or expression error');maxGeometryError=Math.max(maxGeometryError,maxError);records.push({path:j,points:first.vertices.length,closed:first.closed,temporal_changes:changes,max_direction_error:maxError,first_vertices:first.vertices.slice(0,6)});
 }
 var uniqueCount=0;for(var key in unique)if(unique.hasOwnProperty(key))uniqueCount++;if(uniqueCount!==cfg.paths)errors.push('Duplicated path randomness');
 var original=encode(prop(comp,1).valueAtTime(0,false).vertices);layer.effect('seed')(1).setValue(cfg.seed+1);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var changed=encode(prop(comp,1).valueAtTime(0,false).vertices);if(changed===original)errors.push('Seed edit/reopen did not change path');comp.layer('CYBER_LINES').effect('seed')(1).setValue(cfg.seed);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();if(encode(prop(comp,1).valueAtTime(0,false).vertices)!==original)errors.push('Seed restoration mismatch');
 layer=comp.layer('CYBER_LINES');var contents=layer.property('ADBE Root Vectors Group');if(contents.numProperties!==cfg.paths+1)errors.push('Unexpected shape structure');var mirror=layer.effect('ADBE Mirror'),center=mirror.property('ADBE Mirror-0001').value;if(center[0]!==540||center[1]!==540||mirror.property('ADBE Mirror-0002').value!==0)errors.push('Mirror not restored');
 var exports=[];for(var f=0;f<5;f++){var name='native-still-'+f+'.png';comp.saveFrameToPng(f,new File(out+'/'+name));exports.push(name);}
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,shape_paths:cfg.paths,unique_paths:uniqueCount,stroke_width:2,mirror_center:center,mirror_angle:0,max_geometry_error:maxGeometryError,max_position_error:maxPositionError,static_layout_validated_frames:150,native_png_exports:exports,native_seed_edit:{original:cfg.seed,changed:cfg.seed+1,restored:comp.layer('CYBER_LINES').effect('seed')(1).value,changed_path:changed!==original},path_records:records,course_fidelity_status:'candidate_static_rig_only_animation_deferred_to_final_project',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());