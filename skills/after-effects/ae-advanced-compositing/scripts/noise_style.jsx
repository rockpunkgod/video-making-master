__ENCODER__
(function(){var cfg=__CONFIG__,out=__OUTPUT__,stage='guard',errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(name){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name===name)return app.project.item(i);throw Error('Missing '+name);}
function imported(role){var s=cfg.inputs[role],folder=app.project.importFile(new ImportOptions(new File(s.project))),c=null;
 function visit(g){for(var i=1;i<=g.numItems;i++){var x=g.item(i);if(x instanceof FolderItem)visit(x);else if(x instanceof CompItem&&x.name===s.composition)c=x;else if(x instanceof FootageItem&&x.file)throw Error('External media not packaged');}}
 if(!(folder instanceof FolderItem))throw Error('Expected imported project');visit(folder);if(!c)throw Error('Missing input '+role);return c;
}
function reopen(){app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));return find(cfg.name);}
try{
 if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Preserve dirty work');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){owned=true;if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated project');}if(!owned)throw Error('No lab ownership');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.newProject();app.project.bitsPerChannel=16;stage='import';var old=imported('main'),palette=imported('palette');
 var c=app.project.items.addComp(cfg.name,cfg.width,cfg.height,1,cfg.duration,cfg.fps);c.comment='video-skills-lab:course-reproduction';
 var source=old.layer('ROLE_NOISE').source,disabled=[],sourceLayers=[];
 for(var i=1;i<=source.numLayers;i++){var l=source.layer(i);if(/^fn\s*[67]$/i.test(l.name)){l.enabled=false;disabled.push(l.name);}sourceLayers.push({name:l.name,enabled:l.enabled});}
 if(disabled.length!==2)throw Error('Expected source fN6/7 identities; inspect instead of guessing');
 stage='style';palette.layer('P16_NATIVE_COLORAMA_NOISE').copyToComp(c);var noise=c.layer('P16_NATIVE_COLORAMA_NOISE');noise.name='ROLE_NOISE';noise.replaceSource(source,false);
 noise.effect('ADBE Ramp').remove();var key=noise.effect.addProperty('ADBE Linear Color Key2');key.property('ADBE Linear Color Key2-0003').setValue([1,1,1,1]);key.property('ADBE Linear Color Key2-0005').setValue(0);key.property('ADBE Linear Color Key2-0006').setValue(10);key.moveTo(1);
 noise.threeDLayer=true;noise.collapseTransformation=true;noise.transform.anchorPoint.setValue([source.width/2,source.height/2,0]);noise.transform.position.setValue([960,540,-5000]);noise.transform.orientation.setValue([0,0,90]);noise.transform.scale.setValue(cfg.noise_scale);
 noise.startTime=.5;noise.inPoint=.5;noise.outPoint=cfg.duration;noise.transform.opacity.setValueAtTime(cfg.fade_start_frame/cfg.fps,100);noise.transform.opacity.setValueAtTime(cfg.fade_end_frame/cfg.fps,0);
 noise.effect('ADBE Glo2').property('ADBE Glo2-0004').setValue(cfg.glow_intensity);
 old.layer('Camera 1').copyToComp(c);c.layer('Camera 1').outPoint=cfg.duration;
 app.project.reduceProject([c]);while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();
 var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),selected='';for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}if(!selected)throw Error('Native H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));stage='edit reopen';c=reopen();var glow=c.layer('ROLE_NOISE').effect('ADBE Glo2');glow.property('ADBE Glo2-0003').setValue(123);c=reopen();var changed=c.layer('ROLE_NOISE').effect('ADBE Glo2').property('ADBE Glo2-0003').value;if(changed!==123)throw Error('Native edit lost');c.layer('ROLE_NOISE').effect('ADBE Glo2').property('ADBE Glo2-0003').setValue(122);c=reopen();var restored=c.layer('ROLE_NOISE').effect('ADBE Glo2').property('ADBE Glo2-0003').value;if(restored!==122)throw Error('Native restore lost');
 stage='checks';noise=c.layer('ROLE_NOISE');var chain=[],expressions=0,fade=[],maxFadeError=0,media=[];
 for(var i=1;i<=noise.effect.numProperties;i++)chain.push(noise.effect(i).matchName);
 function inspect(p){if(p.propertyType===PropertyType.PROPERTY){if(p.canSetExpression&&p.expressionEnabled){expressions++;for(var f=0;f<cfg.duration*cfg.fps;f++)p.valueAtTime(f/cfg.fps,false);if(p.expressionError)errors.push(p.expressionError);}}else for(var j=1;j<=p.numProperties;j++)inspect(p(j));}
 for(var i=1;i<=app.project.numItems;i++){var x=app.project.item(i);if(x instanceof CompItem)for(var j=1;j<=x.numLayers;j++)inspect(x.layer(j));else if(x instanceof FootageItem&&x.file)media.push(x.file.fsName);}
 if(media.length)errors.push('Unexpected media');
 for(var f=0;f<cfg.duration*cfg.fps;f++){var expected=100;if(f>=cfg.fade_end_frame)expected=0;else if(f>cfg.fade_start_frame)expected=100*(cfg.fade_end_frame-f)/(cfg.fade_end_frame-cfg.fade_start_frame);var actual=noise.transform.opacity.valueAtTime(f/cfg.fps,false);fade.push(actual);maxFadeError=Math.max(maxFadeError,Math.abs(actual-expected));}
 if(maxFadeError>1e-5)errors.push('Fade trace differs');
 var frames=[0,cfg.fps,39,Math.floor(cfg.duration*cfg.fps/2),60,80,cfg.duration*cfg.fps-1];for(var i=0;i<frames.length;i++){var path=out+'/native-still-'+frames[i]+'.png';c.saveFrameToPng(frames[i]/cfg.fps,new File(path));var until=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<until)$.sleep(100);if(!(new File(path)).exists)throw Error('PNG missing');}
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,expressions_checked:expressions,selected_template:selected,output_format:'mp4',native_frames_checked:cfg.duration*cfg.fps,evolution_frames_checked:cfg.duration*cfg.fps,source_layers:sourceLayers,disabled_layers:disabled,effect_chain:chain,max_fade_error:maxFadeError,opacity_trace:fade,native_glow_radius_edit:{original:122,changed:changed,restored:restored},scale:noise.transform.scale.value,orientation:noise.transform.orientation.value,glow:{threshold:noise.effect('ADBE Glo2').property('ADBE Glo2-0002').value,radius:restored,intensity:noise.effect('ADBE Glo2').property('ADBE Glo2-0004').value},media:media,rendered:false,course_fidelity:'Candidate component only; inherited approximate camera and random identity; not finished assembly'});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
