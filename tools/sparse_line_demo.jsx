__ENCODER__
(function(){var cfg=__CONFIG__,out=__OUTPUT__,stage='guard';
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function reopen(){app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='ONE_LINE')return app.project.item(i);throw Error('Missing comp');}
function sample(c,t){var shape=c.layer('CONTINUOUS_LINE').property('ADBE Root Vectors Group').property('ADBE Vector Shape - Group').property('ADBE Vector Shape').valueAtTime(t,false);return shape.vertices;}
function png(c,t,n){c.saveFrameToPng(t,new File(out+'/native-still-'+n+'.png'));var end=Date.now()+30000,last=0,stable=0;while(Date.now()<end){var f=new File(out+'/native-still-'+n+'.png'),size=f.exists?f.length:0;if(size&&size===last)stable++;else stable=0;if(stable>=3)return;last=size;$.sleep(100);}throw Error('PNG flush timeout');}
try{
 if(typeof $.global.__vslCloudTick==='function')throw Error('Other native render active');
 if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Dirty work preserved');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){owned=true;if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Unowned project preserved');}if(!owned)throw Error('Ownership missing');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.newProject();app.project.bitsPerChannel=16;
 var c=app.project.items.addComp('ONE_LINE',1920,1080,1,cfg.duration,30);c.comment='video-skills-lab:video-art-direction single-line original variant';
 c.layers.addSolid([242/255,237/255,227/255],'PAPER',1920,1080,1,cfg.duration);
 var ctrl=c.layers.addNull(cfg.duration);ctrl.name='LINE_CONTROLS';ctrl.enabled=false;
 var amp=ctrl.property('ADBE Effect Parade').addProperty('ADBE Slider Control');amp.name='Amplitude';amp.property(1).setValue(cfg.amplitude);
 stage='native editable path expression';
 var line=c.layers.addShape();line.name='CONTINUOUS_LINE';line.transform.position.setValue([0,0]);
 var vectors=line.property('ADBE Root Vectors Group');vectors.addProperty('ADBE Vector Shape - Group');
 var stroke=vectors.addProperty('ADBE Vector Graphic - Stroke');stroke.property('ADBE Vector Stroke Width').setValue(3.2);
 stroke.property('ADBE Vector Stroke Color').expression='ease(time,13,17,[36/255,37/255,34/255,1],[185/255,91/255,56/255,1])';
 var path=vectors.property('ADBE Vector Shape - Group').property('ADBE Vector Shape');path.expression=cfg.path_expression;
 var before=sample(c,2);if(path.expressionError)throw Error(path.expressionError);
 stage='title and native audio';var fonts=[];
 if(cfg.duration>17){var title=c.layers.addText('共振');title.name='FINAL_TITLE';var source=title.property('ADBE Text Properties').property('ADBE Text Document'),doc=source.value;doc.font='MicrosoftYaHei';doc.fontSize=112;doc.fillColor=[36/255,37/255,34/255];doc.tracking=140;source.setValue(doc);fonts.push({requested:'MicrosoftYaHei',actual:source.value.font});title.transform.position.setValue([435,420]);title.transform.opacity.expression='ease(time,17,18.1,0,100)';}
 for(var i=0;i<cfg.audio_assets.length;i++){var media=app.project.importFile(new ImportOptions(new File(cfg.audio_assets[i]))),audio=c.layers.add(media);audio.name=i?'FINAL_HARMONY':'SPARSE_IMPULSES';audio.moveToEnd();}
 stage='native queue';var rq=app.project.renderQueue.items.add(c),om=rq.outputModule(1),template='';for(var i=0;i<om.templates.length;i++)if(/TIFF/.test(om.templates[i])){template=om.templates[i];break;}if(!template)throw Error('TIFF unavailable');om.applyTemplate(template);new Folder(out+'/render').create();om.file=new File(out+'/render/frame_[#####].tif');app.project.save(new File(out+'/project.aep'));c=reopen();
 stage='edit save reopen restore test';var p=c.layer('LINE_CONTROLS').property('ADBE Effect Parade').property('Amplitude').property(1);p.setValue(cfg.amplitude*.5);c=reopen();var half=sample(c,2);p=c.layer('LINE_CONTROLS').property('ADBE Effect Parade').property('Amplitude').property(1);p.setValue(cfg.amplitude);c=reopen();var restored=sample(c,2);
 stage='native trace';var trace=[],errors=[];for(var f=0;f<cfg.duration*30;f++){var points=sample(c,f/30);trace.push({frame:f,vertices:points});}
 function walk(g){for(var j=1;j<=g.numProperties;j++){var p=g.property(j);if(p.propertyType===PropertyType.PROPERTY){if(p.canSetExpression&&p.expressionEnabled&&p.expressionError)errors.push(p.name+':'+p.expressionError);}else walk(p);}}for(var i=1;i<=c.numLayers;i++)walk(c.layer(i));
 var color=c.layer('CONTINUOUS_LINE').property('ADBE Root Vectors Group').property('ADBE Vector Graphic - Stroke').property('ADBE Vector Stroke Color').valueAtTime(2,false);
 stage='native evidence stills';var times=[0,1.4,2.5,4.8,Math.min(5.8,cfg.duration-1/30)];if(cfg.duration>17)times=times.concat([8.8,11,13.5,16,18.5,19.9]);for(var i=0;i<times.length;i++)png(c,times[i],Math.round(times[i]*30));
 var media=[];for(var i=1;i<=app.project.numItems;i++){var it=app.project.item(i);if(it instanceof FootageItem&&it.file)media.push({path:it.file.fsName,missing:it.footageMissing});}app.project.save();
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,native_color:color,fonts:fonts,main_layers:c.numLayers,output_format:'tiff',selected_template:template,native_edit:{amplitude:cfg.amplitude,before:before,half:half,restored:restored},trace:trace,media:media,scope:'Original art-direction variant; sampled createPath support and amplitude edit verified in actual AE; no course reproduction or listening claim'});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
}());
