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

var out="E:/自媒体/video-skills-lab/samples/course-reproduction-003/p07-blocks-002",cfg={"name": "COURSE_P07_DIGITAL_BLOCKS", "width": 1080, "height": 1080, "fps": 30, "duration": 7, "count": 20, "seed": 1, "source": "BV1Yh4y1A7XT?p=7 00:39–05:09; before optional Tint experiments", "base_project": "E:\\自媒体\\video-skills-lab\\samples\\course-reproduction-002\\p06-final-003\\project.aep", "base_sha256": "1096b70a15213deeb87f9b4e2bfda15b7afd1b8312e3c1582c0173910d4710ca", "course_fidelity_status": "candidate_pending_render_and_visual_comparison", "verified_scope": "none; p7 candidate extension, not covered by p6 verified status"};
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function locate(){for(var j=1;j<=app.project.numItems;j++)if(app.project.item(j).name===cfg.name)return app.project.item(j);throw Error('Course composition missing');}
try{
 if(app.project&&app.project.numItems>0){var own=true,hasComp=false;for(var j=1;j<=app.project.numItems;j++)if(app.project.item(j) instanceof CompItem){hasComp=true;if(app.project.item(j).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing project');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.open(new File(cfg.base_project));
 var comp=null;for(var j=1;j<=app.project.numItems;j++)if(app.project.item(j).name==='COURSE_P06_TRIM_FINAL')comp=app.project.item(j);
 if(!comp||comp.width!==1080||comp.height!==1080||comp.frameRate!==30||comp.duration!==7||comp.numLayers!==20)throw Error('Base must be course p6 trim-final profile');
 comp.name=cfg.name;var ctrl=comp.layer('controls'),camera=comp.layer('Camera 1'),source=comp.layer(3),expressions={},names=['ADBE Position','ADBE Scale','ADBE Rotate Z','ADBE Opacity'];
 for(var j=0;j<names.length;j++){expressions[names[j]]=source.transform.property(names[j]).expression;if(!expressions[names[j]])throw Error('Missing inherited expression');}
 while(comp.numLayers>2)comp.layer(comp.numLayers).remove();
 var rotation=ctrl.effect('Rotation Z spacing')(1);rotation.expressionEnabled=false;rotation.setValue(0);ctrl.effect('Scale interval')(1).setValue(0);
 function noise(layer,seed){var fx=layer.property('ADBE Effect Parade').addProperty('ADBE Fractal Noise');
  fx.property('ADBE Fractal Noise-0001').setValue(19); // Native UI confirms 字符串 (Strings), not old enum 16 (Terrain).
  fx.property('ADBE Fractal Noise-0002').setValue(1); // Native UI confirms 块 (Block).
  fx.property('ADBE Fractal Noise-0003').setValue(1);fx.property('ADBE Fractal Noise-0004').setValue(2000);fx.property('ADBE Fractal Noise-0015').setValue(1);
  fx.property('ADBE Fractal Noise-0023').expression='time*5';fx.property('ADBE Fractal Noise-0027').expression='seedRandom('+seed+',true);\nrandom(1000)';return fx;}
 var tex=app.project.items.addComp('tex_FN',1080,1080,1,7,30);tex.comment='video-skills-lab:course-reproduction';noise(tex.layers.addSolid([1,1,1],'FN_source_seed5',1080,1080,1,7),5);
 var first=comp.layers.addSolid([1,1,1],'FN',1080,1080,1,7);first.threeDLayer=true;first.moveAfter(ctrl);noise(first,cfg.seed);
 for(var j=0;j<names.length;j++)first.transform.property(names[j]).expression=expressions[names[j]];
 first.transform.opacity.expressionEnabled=false;first.transform.opacity.setValue(100);first.blendingMode=BlendingMode.MULTIPLY;
 for(var j=2;j<=cfg.count;j++){var dup=first.duplicate();dup.name='FN '+j;dup.moveAfter(ctrl);}
 while(app.project.renderQueue.numItems>0)app.project.renderQueue.item(1).remove();
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='',format='png';
 for(var j=0;j<templates.length;j++)if(/PNG/.test(templates[j])&&!/alpha|Alpha/.test(templates[j])){selected=templates[j];break;}
 if(selected){new Folder(out+'/render').create();om.applyTemplate(selected);om.file=new File(out+'/render/frame_[#####].png');}
 else{for(var j=0;j<templates.length;j++)if(/H\.264/.test(templates[j])&&/15 Mbps/.test(templates[j])){selected=templates[j];break;}if(!selected)throw Error('No tested native output template');format='mp4';om.applyTemplate(selected);om.file=new File(out+'/native.mp4');}
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();ctrl=comp.layer('controls');
 var errors=[],seeds=[],maxSeedDrift=0,maxEvolutionError=0,maxZError=0,maxScaleError=0;
 for(var i=3;i<=comp.numLayers;i++){var layer=comp.layer(i),fx=layer.effect('ADBE Fractal Noise'),seed=fx.property('ADBE Fractal Noise-0027'),s=seed.valueAtTime(0,false);seeds.push(s);
  if(layer.transform.opacity.expressionEnabled||!layer.transform.opacity.expression||layer.blendingMode!==BlendingMode.MULTIPLY)errors.push(layer.name+': opacity or blend differs');
  for(var f=0;f<210;f++){var t=f/30;maxSeedDrift=Math.max(maxSeedDrift,Math.abs(seed.valueAtTime(t,false)-s));maxEvolutionError=Math.max(maxEvolutionError,Math.abs(fx.property('ADBE Fractal Noise-0023').valueAtTime(t,false)-t*5));maxZError=Math.max(maxZError,Math.abs(layer.transform.position.valueAtTime(t,false)[2]-(500+(i-3)*1000)));maxScaleError=Math.max(maxScaleError,Math.abs(layer.transform.scale.valueAtTime(t,false)[0]-100));}
  for(var j=0;j<names.length;j++)if(layer.transform.property(names[j]).expressionError)errors.push(layer.name+':'+layer.transform.property(names[j]).expressionError);
  if(seed.expressionError||fx.property('ADBE Fractal Noise-0023').expressionError)errors.push(layer.name+': noise expression error');
 }
 var unique={};for(var i=0;i<seeds.length;i++)unique[String(seeds[i])]=true;var distinct=0;for(var key in unique)distinct++;
 if(distinct!==cfg.count||maxSeedDrift>1e-5||maxEvolutionError>1e-5||maxZError>1e-5||maxScaleError>1e-5)errors.push('Course noise temporal/spatial invariant failed');
 // Real native edit, save/reopen, then restore and save/reopen; never edit the base project.
 var seedProp=comp.layer(3).effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0027'),original=seedProp.expression,before=seedProp.valueAtTime(0,false);
 seedProp.expression='seedRandom('+(cfg.seed+1)+',true);\nrandom(1000)';app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();seedProp=comp.layer(3).effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0027');var changed=seedProp.valueAtTime(0,false);
 if(Math.abs(before-changed)<.001)errors.push('Native seed edit had no effect');seedProp.expression=original;app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var restored=comp.layer(3).effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0027').valueAtTime(0,false);if(Math.abs(restored-before)>1e-5)errors.push('Seed restore failed');
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:format,layers:comp.numLayers,bits_per_channel:app.project.bitsPerChannel,distinct_layer_seeds:distinct,layer_seeds:seeds,max_seed_temporal_drift:maxSeedDrift,max_evolution_error:maxEvolutionError,max_z_error:maxZError,max_scale_error:maxScaleError,native_seed_edit:{before:before,changed:changed,restored:restored,saved_reopened:true},course_fidelity_status:'candidate_pending_visual_comparison',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());