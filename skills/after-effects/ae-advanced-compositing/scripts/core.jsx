(function(){
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,stage='ownership',errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(name){for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem&&c.name===name)return c;}throw Error('Missing '+name);}
function ctrl(c,name){return c.layer('controls').effect(name)(1);}
function animate(p,start,end,from,to){p.setValueAtTime(start/30,from);p.setValueAtTime(end/30,to);for(var k=1;k<=p.numKeys;k++){var a=[],b=[],n=p.keyValue(k) instanceof Array?p.keyValue(k).length:1;for(var j=0;j<n;j++){a.push(new KeyframeEase(0,33.333333));b.push(new KeyframeEase(0,.1));}p.setTemporalEaseAtKey(k,a,b);p.setInterpolationTypeAtKey(k,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.LINEAR);}}
function still(c,frame){var path=out+'/native-still-'+frame+'.png';c.saveFrameToPng(frame/30,new File(path));var end=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<end)$.sleep(100);if(!(new File(path)).exists)throw Error('PNG missing '+frame);}
try{
 if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Preserve dirty work');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){owned=true;if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated work');}if(!owned)throw Error('No owned comp');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.newProject();app.project.bitsPerChannel=16;stage='import';app.project.importFile(new ImportOptions(new File(cfg.input_project)));var c=find('COURSE_P11_ALGORITHMIC_LAYOUT'),base=find('baseShape');c.name=cfg.name;c.duration=cfg.duration;c.workAreaStart=0;c.workAreaDuration=cfg.duration;c.bgColor=[0,0,0];base.duration=cfg.duration;
 while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();
 while(c.numLayers>cfg.count+1)c.layer(c.numLayers).remove();for(var i=1;i<=c.numLayers;i++)c.layer(i).outPoint=cfg.duration;
 stage='gradient stroke matte';var shape=base.layer(1),v=shape.property('ADBE Root Vectors Group').property(1).property('ADBE Vectors Group');v.property('ADBE Vector Graphic - Fill').remove();
 var stroke=v.addProperty('ADBE Vector Graphic - Stroke');stroke.property('ADBE Vector Stroke Color').setValue([1,0,0]);stroke.property('ADBE Vector Stroke Width').setValue(cfg.stroke);
 var ramp=shape.effect.addProperty('ADBE Ramp');ramp.property('ADBE Ramp-0001').setValue([150,71]);ramp.property('ADBE Ramp-0003').setValue([150,300]);shape.outPoint=cfg.duration;
 var matte=base.layers.addShape();matte.name='matte';matte.transform.position.setValue([150,150]);matte.outPoint=cfg.duration;var mv=matte.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group').property('ADBE Vectors Group');mv.addProperty('ADBE Vector Shape - Ellipse').property('ADBE Vector Ellipse Size').setValue([134,134]);mv.addProperty('ADBE Vector Graphic - Fill').property('ADBE Vector Fill Color').setValue([1,1,1]);
 animate(matte.transform.scale,0,26,[0,0],[100,100]);if(typeof shape.setTrackMatte!=='function')throw Error('Native setTrackMatte unavailable');shape.setTrackMatte(matte,TrackMatteType.ALPHA);matte.enabled=false;
 stage='controls';ctrl(c,'Phase').expression='time*'+cfg.speed;ctrl(c,'Phase increment').setValue(63);animate(ctrl(c,'Z increment'),16,43,0,18);animate(ctrl(c,'Radius'),17,43,0,61);
 stage='stylize';var adj=c.layers.addSolid([1,1,1],'stylize',1080,1080,1,cfg.duration);adj.adjustmentLayer=true;
 var tri=adj.effect.addProperty('ADBE Tritone');tri.property('ADBE Tritone-0002').setValue([12/255,246/255,240/255,0]);
 var blur=adj.effect.addProperty('CC Vector Blur');blur.property('CC Vector Blur-0001').setValue(3);blur.property('CC Vector Blur-0002').setValue(35);
 var lens=adj.effect.addProperty('CC Lens');lens.property('CC Lens-0002').setValue(73);
 var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),selected='';for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}if(!selected)throw Error('Native H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 stage='save reopen';app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find(cfg.name);base=find('baseShape');
 var original=ctrl(c,'Phase increment').value;ctrl(c,'Phase increment').setValue(original+1);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find(cfg.name);var changed=ctrl(c,'Phase increment').value;if(changed!==original+1)errors.push('Edit lost');ctrl(c,'Phase increment').setValue(original);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));c=find(cfg.name);base=find('baseShape');
 stage='native checks';var maxError=0,phaseError=0,traces=[],media=[];for(var f=0;f<151;f++){var t=f/30,phase=ctrl(c,'Phase').valueAtTime(t,false),radius=ctrl(c,'Radius').valueAtTime(t,false),z=ctrl(c,'Z increment').valueAtTime(t,false);phaseError=Math.max(phaseError,Math.abs(phase-t*cfg.speed));traces.push({frame:f,phase:phase,radius:radius,z:z,matte_scale:base.layer('matte').transform.scale.valueAtTime(t,false)});
  for(var i=3;i<=c.numLayers;i++){var l=c.layer(i),n=i-c.layer('controls').index,angle=(phase+n*63)*Math.PI/180,actual=l.transform.position.valueAtTime(t,false),expected=[540+radius*Math.PI*2*Math.cos(angle),540+radius*Math.PI*2*Math.sin(angle),z*n];for(var j=0;j<3;j++)maxError=Math.max(maxError,Math.abs(actual[j]-expected[j]));if(l.transform.position.expressionError||l.effect('myIndex')(1).expressionError)errors.push('Expression failure '+i);}}
 for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof FootageItem&&item.file)media.push(item.file.fsName);}if(media.length)errors.push('Unexpected external media');if(maxError>1e-5||phaseError>1e-5)errors.push('Native equation differs');
 shape=base.layer(2);var matteLinked=shape.trackMatteLayer===base.layer('matte')&&shape.trackMatteType===TrackMatteType.ALPHA;if(!matteLinked)errors.push('Alpha matte not retained');
 still(c,0);still(c,30);still(c,75);still(c,150);still(c,17);still(c,43);
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',native_frames_checked:151,layer_count:c.numLayers,shape_count:c.numLayers-2,
  max_position_error:maxError,max_phase_error:phaseError,native_trace:traces,media:media,missing_media:[],alpha_matte_linked:matteLinked,
  effect_chain:[c.layer('stylize').effect(1).matchName,c.layer('stylize').effect(2).matchName,c.layer('stylize').effect(3).matchName],native_phase_increment_edit:{original:original,changed:changed,restored:ctrl(c,'Phase increment').value},
  course_fidelity:'candidate; exact curve influences and key frame estimates remain unproven; native Perpendicular enum3 GUI confirmed; optional Box Blur removed as source06:22',rendered:false});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
