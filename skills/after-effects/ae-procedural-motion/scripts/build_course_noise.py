"""Candidate p7 extension of a real course-stage AEP. Does not change verified p6."""
import argparse, hashlib, json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--base',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
ap.add_argument('--seed',type=int,default=1)
ap.add_argument('--course-tint',action='store_true',help='Observed p7 final Tint on FN15 and FN18, black mapped to 0057FF')
a=ap.parse_args()
base=a.base.resolve();out=a.out.resolve()
if not base.is_file() or base.suffix.lower()!='.aep':raise ValueError('Native course trim-final project required')
if not 0<=a.seed<=10000:raise ValueError('Seed out of supported range')
if out.exists():raise FileExistsError('Use a fresh directory')
out.mkdir(parents=True)
cfg=dict(name='COURSE_P07_DIGITAL_BLOCKS',width=1080,height=1080,fps=30,duration=7,count=20,seed=a.seed,
         source='BV1Yh4y1A7XT?p=7 00:39–05:09; before optional Tint experiments',
         base_project=str(base),base_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),course_tint=a.course_tint,
         course_fidelity_status='candidate_pending_render_and_visual_comparison',
         verified_scope='none; p7 candidate extension, not covered by p6 verified status')
(out/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
body=r'''(function(){__ENCODER__
var out=__OUT__,cfg=__CFG__;
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
 var tintProperties=[];
 if(cfg.course_tint){
  var tintNames=['FN 15','FN 18'];for(var j=0;j<tintNames.length;j++){
   var tint=comp.layer(tintNames[j]).effect.addProperty('ADBE Tint');
   var black=tint.property(1),white=tint.property(2),amount=tint.property(3);
   if(black.propertyValueType!==PropertyValueType.COLOR||white.propertyValueType!==PropertyValueType.COLOR||Math.abs(black.value[0])>1e-6||Math.abs(white.value[0]-1)>1e-6||amount.value!==100)throw Error('Tint native layout differs; inspect before proceeding');
   tintProperties.push({layer:tintNames[j],black_match:black.matchName,white_match:white.matchName,amount_match:amount.matchName});black.setValue([0,87/255,1]);
  }
 }
 while(app.project.renderQueue.numItems>0)app.project.renderQueue.item(1).remove();
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='',format='png';
 for(var j=0;j<templates.length;j++)if(/PNG/.test(templates[j])&&!/alpha|Alpha/.test(templates[j])){selected=templates[j];break;}
 if(selected){new Folder(out+'/render').create();om.applyTemplate(selected);om.file=new File(out+'/render/frame_[#####].png');}
 else{for(var j=0;j<templates.length;j++)if(/H\.264/.test(templates[j])&&/15 Mbps/.test(templates[j])){selected=templates[j];break;}if(!selected)throw Error('No tested native output template');format='mp4';om.applyTemplate(selected);om.file=new File(out+'/native.mp4');}
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();ctrl=comp.layer('controls');
 var errors=[],seeds=[],maxSeedDrift=0,maxEvolutionError=0,maxZError=0,maxScaleError=0,tintValues=[];
 if(cfg.course_tint){var targets=['FN 15','FN 18'];for(var j=0;j<targets.length;j++){var v=comp.layer(targets[j]).effect('ADBE Tint').property(1).value;tintValues.push({layer:targets[j],black_maps_to:v});if(Math.abs(v[0])>1e-6||Math.abs(v[1]-87/255)>1e-6||Math.abs(v[2]-1)>1e-6)errors.push('Tint value did not survive reopen');}}
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
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:format,layers:comp.numLayers,bits_per_channel:app.project.bitsPerChannel,distinct_layer_seeds:distinct,layer_seeds:seeds,max_seed_temporal_drift:maxSeedDrift,max_evolution_error:maxEvolutionError,max_z_error:maxZError,max_scale_error:maxScaleError,native_seed_edit:{before:before,changed:changed,restored:restored,saved_reopened:true},native_tint_properties:tintProperties,reopened_tint_values:tintValues,course_fidelity_status:'candidate_pending_visual_comparison',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());'''
body=body.replace('__ENCODER__',(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__CFG__',json.dumps(cfg,ensure_ascii=False))
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
