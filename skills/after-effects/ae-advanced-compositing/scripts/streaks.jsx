(function(){
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,stage='ownership';
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(){for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem&&c.name===cfg.name)return c;}throw Error('Target missing');}
function slider(l,n,v){var fx=l.effect.addProperty('ADBE Slider Control');fx.name=n;fx(1).setValue(v);}
function point(l,n,v){var fx=l.effect.addProperty('ADBE Point3D Control');fx.name=n;fx(1).setValue(v);}
try{
 if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Preserve dirty work');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated work');owned=true;}if(!owned)throw Error('No lab composition');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.newProject();app.project.bitsPerChannel=16;stage='import';var folder=app.project.importFile(new ImportOptions(new File(cfg.input_project))),c=null;
 function visit(g){for(var i=1;i<=g.numItems;i++){var item=g.item(i);if(item instanceof FolderItem)visit(item);else if(item instanceof CompItem&&item.name===cfg.input_comp)c=item;}}
 visit(folder);if(!c||c.width!==1080||c.height!==1080||c.frameRate!==30)throw Error('Unexpected input rig');c.name=cfg.name;
 var ctrl=c.layer('controls'),base=c.layer('FN');
 for(var i=c.numLayers;i>=1;i--){var l=c.layer(i);if(l instanceof CameraLayer){l.enabled=false;continue;}if(l!==ctrl&&l!==base)l.remove();}
 while(ctrl.effect.numProperties)ctrl.effect(1).remove();slider(ctrl,'seed',cfg.seed);slider(ctrl,'driftSpeed',0);point(ctrl,'Position Min',[-1084,540,0]);point(ctrl,'Position Max',[3130,540,cfg.depth]);
 base.moveAfter(ctrl);base.solo=false;base.enabled=true;
 var tr=base.transform;tr.position.expressionEnabled=false;tr.position.setValue([0,0,0]);
 tr.scale.expressionEnabled=false;tr.scale.setValue([cfg.scale,cfg.scale,cfg.scale]);tr.zRotation.expressionEnabled=false;tr.zRotation.setValue(0);tr.opacity.expressionEnabled=false;tr.opacity.setValue(100);
 tr.position.expression='seed=thisComp.layer("controls").effect("seed")(1);\nseedRandom(seed,1);\nposMin=thisComp.layer("controls").effect("Position Min")(1);\nposMax=thisComp.layer("controls").effect("Position Max")(1);\npos=random(posMin,posMax);\n\n// add drift\ndrift=time*random(thisComp.layer("controls").effect("driftSpeed")(1));\npos+drift+value;';
 var fx=base.effect('ADBE Fractal Noise');fx.property('ADBE Fractal Noise-0009').setValue(0);fx.property('ADBE Fractal Noise-0011').setValue(24.6);fx.property('ADBE Fractal Noise-0012').setValue(2270);
 if(fx.property('ADBE Fractal Noise-0001').value!==19||fx.property('ADBE Fractal Noise-0004').value!==2000)throw Error('Inherited Strings/Contrast differs');
 for(var i=1;i<cfg.count;i++){var d=base.duplicate();d.name='FN '+(i+1);d.moveAfter(ctrl);}
 while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),selected='';
 for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}
 if(!selected)throw Error('Native output template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 stage='native edit';app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();var before=c.layer(3).transform.position.valueAtTime(0,false);
 c.layer('controls').effect('seed')(1).setValue(cfg.seed+1);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();var changed=c.layer(3).transform.position.valueAtTime(0,false);
 var moved=0;for(var j=0;j<3;j++)moved+=Math.abs(changed[j]-before[j]);if(moved<1e-3)throw Error('Seed edit had no effect');
 c.layer('controls').effect('seed')(1).setValue(cfg.seed);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();var restored=c.layer(3).transform.position.valueAtTime(0,false);
 for(var j=0;j<3;j++)if(Math.abs(restored[j]-before[j])>1e-6)throw Error('Seed restore differs');
 stage='per-frame native checks';var errors=[],records=[],media=[],frames=Math.round(cfg.duration*cfg.fps),maxPositionDrift=0,maxEvolutionError=0,maxScaleError=0;
 for(var i=3;i<=c.numLayers;i++){var l=c.layer(i),p=l.transform.position,v0=p.valueAtTime(0,false),noise=l.effect('ADBE Fractal Noise');
  if(!l.threeDLayer||l.blendingMode!==BlendingMode.MULTIPLY||Math.abs(v0[1]-540)>1e-6||v0[0]<-1084||v0[0]>3130||v0[2]<0||v0[2]>cfg.depth)errors.push('Spatial bounds differ '+l.name);
  for(var f=0;f<frames;f++){var t=f/cfg.fps,v=p.valueAtTime(t,false),sc=l.transform.scale.valueAtTime(t,false);for(var j=0;j<3;j++){maxPositionDrift=Math.max(maxPositionDrift,Math.abs(v[j]-v0[j]));maxScaleError=Math.max(maxScaleError,Math.abs(sc[j]-cfg.scale));}maxEvolutionError=Math.max(maxEvolutionError,Math.abs(noise.property('ADBE Fractal Noise-0023').valueAtTime(t,false)-t*5));}
  if(p.expressionError||noise.property('ADBE Fractal Noise-0023').expressionError||noise.property('ADBE Fractal Noise-0027').expressionError)errors.push('Expression error '+l.name);
  records.push({name:l.name,position:v0,scale:l.transform.scale.value,width:noise.property('ADBE Fractal Noise-0011').value,height:noise.property('ADBE Fractal Noise-0012').value,position_expression:p.expression,evolution_expression:noise.property('ADBE Fractal Noise-0023').expression});
 }
 if(records.length!==cfg.count||maxPositionDrift>1e-6||maxEvolutionError>1e-6||maxScaleError>1e-6)errors.push('Temporal invariants differ');
 for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof FootageItem&&item.file){media.push({path:item.file.fsName,missing:item.footageMissing});if(item.footageMissing)errors.push('Missing media');}}
 function still(frame){var path=out+'/native-still-'+frame+'.png';c.saveFrameToPng(frame/cfg.fps,new File(path));var deadline=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<deadline)$.sleep(100);if(!(new File(path)).exists)throw Error('Native PNG missing '+frame);}
 still(0);still(30);still(Math.floor(frames/2));still(frames-1);
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',native_frames_checked:frames,layers:records,media:media,max_position_drift:maxPositionDrift,max_evolution_error:maxEvolutionError,max_scale_error:maxScaleError,native_seed_edit:{before:before,changed:changed,restored:restored},course_fidelity:'candidate; visible settings reproduced, Position base0 and constant scale reconstruction remain inferred',rendered:false});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
