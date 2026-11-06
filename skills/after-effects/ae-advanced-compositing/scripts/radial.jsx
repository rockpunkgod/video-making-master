(function(){
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,stage='ownership';
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(){for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem&&c.name==='P15_RADIAL')return c;}throw Error('Missing P15_RADIAL');}
try{
 if(app.project&&app.project.numItems){
  if(app.project.dirty)throw Error('Preserve unsaved work');var owned=false;
  for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated work');owned=true;}
  if(!owned)throw Error('No lab composition');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
 }
 app.newProject();app.project.bitsPerChannel=16;stage='import own template';
 app.project.importFile(new ImportOptions(new File(cfg.template)));var c=find();
 while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();
 c.duration=cfg.duration;c.workAreaStart=0;c.workAreaDuration=cfg.duration;c.layer(1).outPoint=cfg.duration;
 var l=c.layer(1);l.effect('evolution_speed')(1).setValue(cfg.speed);
 l.effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0027').setValue(cfg.seed);
 if(l.effect('CC Radial Fast Blur')(3).value!==2)throw Error('Template must retain GUI-confirmed Brightest enum2');
 if(l.effect.numProperties!==6)throw Error('Course six-effect chain differs');
 var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),selected='';
 for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}
 if(!selected)throw Error('Tested native H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();
 stage='controller edit reopen restore';var old=c.layer(1).effect('evolution_speed')(1).value;
 c.layer(1).effect('evolution_speed')(1).setValue(old+1);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();
 var changed=c.layer(1).effect('evolution_speed')(1).value;if(changed!==old+1)throw Error('Native controller edit lost');
 c.layer(1).effect('evolution_speed')(1).setValue(old);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find();
 var errors=[],ev=c.layer(1).effect('ADBE Fractal Noise').property('ADBE Fractal Noise-0023'),trace=[],media=[];
 for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof FootageItem&&item.file){media.push(item.file.fsName);if(item.footageMissing)errors.push('Missing media '+item.name);}}
 for(var f=0;f<Math.round(cfg.duration*cfg.fps);f++){var v=ev.valueAtTime(f/cfg.fps,false);trace.push(v);if(Math.abs(v-f/cfg.fps*cfg.speed)>1e-6)errors.push('Evolution differs '+f);}
 if(ev.expressionError)errors.push(ev.expressionError);
 // A prior loop left only the first PNG despite a successful host receipt.
 // The cause is unproven; check real exports instead of trusting the return.
 function exportStill(frame){var path=out+'/native-still-'+frame+'.png';c.saveFrameToPng(frame/cfg.fps,new File(path));var deadline=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<deadline)$.sleep(100);if(!(new File(path)).exists)throw Error('Native PNG export missing '+frame);}
 exportStill(0);exportStill(Math.min(Math.round(cfg.fps),trace.length-1));exportStill(Math.floor(trace.length/2));exportStill(trace.length-1);
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',
  evolution_frames_checked:trace.length,evolution_trace:trace,controller_edit:{original:old,changed:changed,restored:c.layer(1).effect('evolution_speed')(1).value},
  media:media,missing_media:[],course_fidelity:'candidate; native template preserves own GUI curve reconstruction; exact course curves and noise identity unverified',rendered:false});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
