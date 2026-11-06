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

var cfg={"name": "COURSE_P08_THRESHOLD", "width": 1080, "height": 1080, "fps": 30, "duration": 5, "direction": "appear", "end_frame": 113, "seed": 1, "asset": "E:/自媒体/video-skills-lab/samples/course-reproduction-004/p08-geometry-001/assets/input.png", "source": "BV1Yh4y1A7XT?p=8 07:00–10:51", "status": "candidate", "layout_provenance": "5x5 white circles observed; diameter100, centers240..840 at150 spacing inferred from square viewport", "timing_provenance": "38 frames inferred from source composition frame36 threshold5.26; final reversed/extended endpoint frame113 observed at 10:48–10:51", "asset_sha256": "f4e0b0064871dc9f639959b72cecbcfb2e3414f940166c5f21f40d1552dc5009", "scope": "PNG generalization using unchanged course opacity expression; not circle baseline"},out="E:/自媒体/video-skills-lab/samples/course-reproduction-004/p08-geometry-001";
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing course composition');}
try{
 if(app.project&&app.project.numItems>0){var owned=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')owned=false;}if(!owned||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;
 var comp=app.project.items.addComp(cfg.name,1080,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[0,0,0];
 var ctrl=comp.layers.addNull();ctrl.name='controls';
 var seed=ctrl.effect.addProperty('ADBE Slider Control');seed.name='seed';seed.property(1).setValue(cfg.seed);
 var threshold=ctrl.effect.addProperty('ADBE Slider Control');threshold.name='threshold';threshold=threshold.property(1);
 threshold.setValueAtTime(0,cfg.direction==='disappear'?100:0);threshold.setValueAtTime(cfg.end_frame/30,cfg.direction==='disappear'?0:100);
 for(var i=1;i<=2;i++)threshold.setInterpolationTypeAtKey(i,KeyframeInterpolationType.LINEAR,KeyframeInterpolationType.LINEAR);
 var expression='seed = thisComp.layer("controls").effect("seed")(1);\nthreshold = thisComp.layer("controls").effect("threshold")(1);\nseedRandom(seed,true);\nmyRandValue=random(100);\nmyOpacity=100;\n\n//conditional\nif(myRandValue>=threshold) {myOpacity=0};\nmyOpacity;';
 var imported=null;if(cfg.asset)imported=app.project.importFile(new ImportOptions(new File(cfg.asset)));
 for(var row=0;row<5;row++)for(var col=0;col<5;col++){
  var layer=imported?comp.layers.add(imported):comp.layers.addShape();layer.name='CELL_'+row+'_'+col;layer.moveToEnd();
  layer.transform.position.setValue([240+150*col,240+150*row]);
  if(imported){var fit=100*100/Math.max(imported.width,imported.height);layer.transform.scale.setValue([fit,fit]);}
  else{var group=layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');group.name='Ellipse 1';var vectors=group.property('ADBE Vectors Group');var ellipse=vectors.addProperty('ADBE Vector Shape - Ellipse');ellipse.property('ADBE Vector Ellipse Size').setValue([100,100]);var fill=vectors.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').setValue([1,1,1]);}
  layer.transform.opacity.expression=expression;
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='';
 for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=find();ctrl=comp.layer('controls');threshold=ctrl.effect('threshold')(1);
 var samples=[],errors=[],expectedFrames=[],maxError=0;
 // Read the random sample on the same native property identity, then restore the exact course expression.
 for(var i=2;i<=comp.numLayers;i++){var p=comp.layer(i).transform.opacity,original=p.expression;p.expression=original.replace(/myOpacity;$/,'myRandValue;');var v=p.valueAtTime(0,false);for(var f=1;f<150;f++)if(Math.abs(p.valueAtTime(f/30,false)-v)>1e-6)errors.push('Timeless sample changed');samples.push(v);p.expression=original;if(p.expressionError)errors.push(p.expressionError);}
 for(var f=0;f<150;f++){var t=f/30,h=threshold.valueAtTime(t,false),expected=[];for(var i=2;i<=comp.numLayers;i++){var want=samples[i-2]>=h?0:100;expected.push(want);maxError=Math.max(maxError,Math.abs(comp.layer(i).transform.opacity.valueAtTime(t,false)-want));}expectedFrames.push(expected);}
 if(maxError>1e-6)errors.push('Conditional threshold mismatch');
 var seedControl=ctrl.effect('seed')(1),before=[],changed=[];for(var i=2;i<=comp.numLayers;i++)before.push(comp.layer(i).transform.opacity.valueAtTime(cfg.end_frame/60,false));seedControl.setValue(cfg.seed+1);
 app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=find();for(var i=2;i<=comp.numLayers;i++)changed.push(comp.layer(i).transform.opacity.valueAtTime(cfg.end_frame/60,false));
 var changedCells=0;for(var i=0;i<before.length;i++)if(before[i]!==changed[i])changedCells++;if(!changedCells)errors.push('Seed edit did not alter the pattern');
 comp.layer('controls').effect('seed')(1).setValue(cfg.seed);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=find();
 var restored=true;for(var i=2;i<=comp.numLayers;i++)if(comp.layer(i).transform.opacity.valueAtTime(cfg.end_frame/60,false)!==before[i-2])restored=false;if(!restored)errors.push('Seed restore failed');
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,bits_per_channel:app.project.bitsPerChannel,native_samples:samples,maximum_conditional_error:maxError,expected_opacity_frames:expectedFrames,native_seed_edit:{changed_cells:changedCells,restored_and_reopened:restored},threshold_at_frame36:comp.layer('controls').effect('threshold')(1).valueAtTime(36/30,false),course_fidelity_status:'candidate_pending_reference_review',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());