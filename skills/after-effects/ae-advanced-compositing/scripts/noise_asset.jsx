(function(){
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,stage='ownership';
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(){for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem&&c.name===cfg.name)return c;}throw Error('Missing target comp');}
function offset(layer){return layer.effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0013');}
try{
 if(app.project&&app.project.numItems){
  if(app.project.dirty)throw Error('Preserve dirty work');var owned=false;
  for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated work');owned=true;}
  if(!owned)throw Error('No lab composition');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
 }
 app.newProject();app.project.bitsPerChannel=16;stage='import';
 var imported=app.project.importFile(new ImportOptions(new File(cfg.input_project))),c=null;
 function visit(folder){for(var i=1;i<=folder.numItems;i++){var item=folder.item(i);if(item instanceof FolderItem)visit(item);else if(item instanceof CompItem&&item.name===cfg.input_comp)c=item;}}
 visit(imported);if(!c||c.width!==1080||c.height!==1080||c.frameRate!==30)throw Error('Unexpected input rig');c.name=cfg.name;
 var ctrl=c.layer('controls'),base=c.layer('FN 7');
 for(var i=c.numLayers;i>=1;i--){var layer=c.layer(i);if(layer instanceof CameraLayer){layer.enabled=false;continue;}if(layer!==ctrl&&layer!==base)layer.remove();}
 ctrl.effect('Position Z spacing')(1).setValue(350);var rot=ctrl.effect('Rotation Z spacing')(1);rot.expressionEnabled=false;rot.setValue(0);ctrl.effect('Scale interval')(1).setValue(0);
 base.moveAfter(ctrl);base.name='FN 7';base.solo=false;base.enabled=true;base.outPoint=cfg.duration;
 var noise=base.effect('ADBE Fractal Noise');noise.property('ADBE Fractal Noise-0009').setValue(0);noise.property('ADBE Fractal Noise-0011').setValue(500);noise.property('ADBE Fractal Noise-0012').setValue(cfg.noise_height);
 offset(base).setValue([540,540]);offset(base).expression='value+[0,time*'+cfg.offset_speed+']';
 if(cfg.seed!==null)noise.property('ADBE Fractal Noise-0027').expression='seedRandom('+cfg.seed+',true);\nrandom(1000)';
 if(noise.property('ADBE Fractal Noise-0001').value!==19||noise.property('ADBE Fractal Noise-0002').value!==1||noise.property('ADBE Fractal Noise-0004').value!==2000)throw Error('Inherited Strings/Block/Contrast differs');
 // This host stores GUI Interpolation100% as1, with native bounds0..1.
 var polar=base.effect.addProperty('ADBE Polar Coordinates');polar(1).setValue(1);polar(2).setValue(1);
 for(var i=1;i<cfg.count;i++){var d=base.duplicate();d.name='FN '+(7+i);d.moveAfter(ctrl);}
 while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),selected='';
 for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}
 if(!selected)throw Error('Known output template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 stage='save and reopen';app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();
 stage='editable expression';var original=offset(c.layer(3)).expression,before=offset(c.layer(3)).valueAtTime(1,false);
 offset(c.layer(3)).expression='value+[0,time*'+(cfg.offset_speed+1)+']';app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();var changed=offset(c.layer(3)).valueAtTime(1,false);
 if(Math.abs(changed[1]-before[1]-1)>1e-6)throw Error('Offset edit failed');offset(c.layer(3)).expression=original;app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();
 stage='per frame invariants';var errors=[],records=[],media=[],frames=Math.round(cfg.fps*cfg.duration),maxOffset=0,maxEvolution=0,maxZ=0;
 for(var i=3;i<=c.numLayers;i++){var l=c.layer(i),fx=l.effect('ADBE Fractal Noise'),p=offset(l),e=fx.property('ADBE Fractal Noise-0023');
  if(!l.threeDLayer||l.blendingMode!==BlendingMode.MULTIPLY||l.effect('ADBE Polar Coordinates')(2).value!==1)errors.push('Layer structure differs '+l.name);
  for(var f=0;f<frames;f++){var t=f/cfg.fps,v=p.valueAtTime(t,false);maxOffset=Math.max(maxOffset,Math.abs(v[0]-540),Math.abs(v[1]-(540+t*cfg.offset_speed)));maxEvolution=Math.max(maxEvolution,Math.abs(e.valueAtTime(t,false)-t*5));maxZ=Math.max(maxZ,Math.abs(l.transform.position.valueAtTime(t,false)[2]-(500+(i-3)*350)));}
  if(p.expressionError||e.expressionError||l.transform.position.expressionError)errors.push('Expression error '+l.name);
  records.push({name:l.name,index:i,position:l.transform.position.valueAtTime(0,false),offset_expression:p.expression,evolution_expression:e.expression,seed_expression:fx.property('ADBE Fractal Noise-0027').expression,height:fx.property('ADBE Fractal Noise-0012').value});
 }
 for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof FootageItem&&item.file){media.push({path:item.file.fsName,missing:item.footageMissing});if(item.footageMissing)errors.push('Missing footage');}}
 if(records.length!==cfg.count||maxOffset>1e-5||maxEvolution>1e-5||maxZ>1e-5)errors.push('Polar native invariants differ');
 function still(frame){var path=out+'/native-still-'+frame+'.png';c.saveFrameToPng(frame/cfg.fps,new File(path));var deadline=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<deadline)$.sleep(100);if(!(new File(path)).exists)throw Error('Native PNG missing '+frame);}
 still(0);still(30);still(Math.floor(frames/2));still(frames-1);
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',native_frames_checked:frames,layers:records,media:media,max_offset_error:maxOffset,max_evolution_error:maxEvolution,max_z_error:maxZ,native_offset_edit:{before:before,changed:changed,restored:offset(c.layer(3)).valueAtTime(1,false)},conversion_enum:1,course_fidelity:'candidate; conversion enum pending native UI confirmation; exact random identities unproven',rendered:false});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
