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

var out="E:/自媒体/video-skills-lab/samples/course-reproduction-007/p11-baseline-001",cfg={"name": "COURSE_P11_ALGORITHMIC_LAYOUT", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "count": 176, "phase": 106, "phase_step": 63, "z_step": 35, "radius": 73, "motion_expectation": "static_layout", "asset": null, "status": "candidate", "source": "BV1Yh4y1A7XT?p=11 07:20 final+value,09:20 corrected multiplication,09:42 ellipse size edit,11:14 controls", "observed": "Phase106,Phase increment63,Z increment35,Radius73; r=Radius*PI*2; myIndex=index-controls.index; [x,y,z]+value", "inferred": "176 layers selected by actual AE silhouette comparison (not directly read); ellipse100 from narration and path-size edit; fill100/255,bg224/255 inferred", "animation_scope": "The source reference is paused. This output documents a static procedural rig; no animation acceptance claim or invented time/keyframes."},errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function slider(layer,name,value){var e=layer.effect.addProperty('ADBE Slider Control');e.name=name;e.property(1).setValue(value);}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing main comp');}
function ctrl(comp,name){return comp.layer('controls').effect(name)(1);}
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;
 var base=app.project.items.addComp('baseShape',300,300,1,5,30);base.comment='video-skills-lab:course-reproduction';
 if(cfg.asset){var footage=app.project.importFile(new ImportOptions(new File(cfg.asset)));var sourceLayer=base.layers.add(footage);sourceLayer.name='ORIGINAL_INPUT';sourceLayer.transform.position.setValue([150,150]);var fit=100*100/Math.max(footage.width,footage.height);sourceLayer.transform.scale.setValue([fit,fit]);}
 else{var shape=base.layers.addShape();shape.transform.position.setValue([150,150]);var vectors=shape.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group').property('ADBE Vectors Group'),circle=vectors.addProperty('ADBE Vector Shape - Ellipse');circle.property('ADBE Vector Ellipse Size').setValue([100,100]);var fill=vectors.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').setValue([100/255,100/255,100/255]);}
 var comp=app.project.items.addComp(cfg.name,1080,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[224/255,224/255,224/255];var controls=comp.layers.addNull();controls.name='controls';slider(controls,'Phase',cfg.phase);slider(controls,'Phase increment',cfg.phase_step);slider(controls,'Z increment',cfg.z_step);slider(controls,'Radius',cfg.radius);
 for(var i=1;i<=cfg.count;i++){
  var layer=comp.layers.add(base);layer.name='baseShape_'+i;layer.threeDLayer=true;layer.moveAfter(controls);slider(layer,'myIndex',0);layer.effect('myIndex')(1).expression='index-thisComp.layer("controls").index';
  layer.transform.position.expression='myIndex=effect("myIndex")(1);\nphaseInc=thisComp.layer("controls").effect("Phase increment")(1);\noffset=myIndex*phaseInc;\nphase=degreesToRadians(thisComp.layer("controls").effect("Phase")(1)+offset);\nzInc=thisComp.layer("controls").effect("Z increment")(1);\nr=thisComp.layer("controls").effect("Radius")(1)*Math.PI*2;\nx=r*Math.cos(phase);\ny=r*Math.sin(phase);\nz=zInc*myIndex;\n[x,y,z]+value;';
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),selected='',templates=om.templates;for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();
 var maxError=0,indexError=0;for(var f=0;f<150;f++)for(var i=2;i<=comp.numLayers;i++){var layer=comp.layer(i),n=i-1,angle=(cfg.phase+n*cfg.phase_step)*Math.PI/180,wanted=[540+cfg.radius*Math.PI*2*Math.cos(angle),540+cfg.radius*Math.PI*2*Math.sin(angle),cfg.z_step*n],actual=layer.transform.position.valueAtTime(f/30,false);indexError=Math.max(indexError,Math.abs(layer.effect('myIndex')(1).valueAtTime(f/30,false)-n));for(var d=0;d<3;d++)maxError=Math.max(maxError,Math.abs(actual[d]-wanted[d]));if(layer.transform.position.expressionError)errors.push(layer.transform.position.expressionError);}
 if(maxError>1e-8||indexError!==0)errors.push('Expression mismatch');
 var first=comp.layer(2).transform.position.valueAtTime(0,false);ctrl(comp,'Phase').setValue(cfg.phase+20);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var edited=comp.layer(2).transform.position.valueAtTime(0,false),editedPhase=ctrl(comp,'Phase').value;if(editedPhase!==cfg.phase+20||Math.abs(edited[0]-first[0])+Math.abs(edited[1]-first[1])<1)errors.push('Phase edit/reopen failed');
 ctrl(comp,'Phase').setValue(cfg.phase);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var restored=comp.layer(2).transform.position.valueAtTime(0,false);for(var d=0;d<3;d++)if(Math.abs(restored[d]-first[d])>1e-8)errors.push('Restore mismatch');
 var exports=[];for(var f=0;f<5;f++){var name='native-still-'+f+'.png';comp.saveFrameToPng(f,new File(out+'/'+name));exports.push(name);}
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,max_position_error:maxError,max_index_error:indexError,static_layout_validated_frames:150,native_png_exports:exports,native_phase_edit:{original:cfg.phase,changed:editedPhase,restored:ctrl(comp,'Phase').value},course_fidelity_status:'candidate_static_layout_only_not_animation_verified',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());