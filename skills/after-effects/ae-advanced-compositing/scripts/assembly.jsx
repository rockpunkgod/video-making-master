(function(){
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,stage='ownership',errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function find(name){for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem&&c.name===name)return c;}throw Error('Missing '+name);}
function imported(role){var spec=cfg.inputs[role],folder=app.project.importFile(new ImportOptions(new File(spec.project))),comp=null;
 if(!(folder instanceof FolderItem))throw Error('Expected project folder');folder.name='ASSEMBLY_INPUT_'+role;
 function visit(group){for(var i=1;i<=group.numItems;i++){var item=group.item(i);if(item instanceof FolderItem)visit(item);else if(item instanceof CompItem&&item.name===spec.composition)comp=item;else if(item instanceof FootageItem&&item.file)throw Error('Unpackaged external media '+item.file.name);}}
 visit(folder);if(!comp)throw Error('Missing component '+role);return comp;
}
function still(c,f){var path=out+'/native-still-'+f+'.png';c.saveFrameToPng(f/cfg.fps,new File(path));var deadline=new Date().getTime()+10000;while(!(new File(path)).exists&&new Date().getTime()<deadline)$.sleep(100);if(!(new File(path)).exists)throw Error('Native PNG missing '+f);}
try{
 if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Preserve dirty work');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){owned=true;if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Preserve unrelated work');}if(!owned)throw Error('No owned comp');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.newProject();app.project.bitsPerChannel=16;stage='import';var main=imported('main');main.name=cfg.name;
 var components={title:imported('title'),radial:imported('radial'),polar:imported('polar'),streaks:imported('streaks'),background:imported('background')};
 while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();
 stage='assemble';var roles=['core','lines','polar','streaks','contours','noise','dots','title'],records=[];
 for(var i=0;i<roles.length;i++){var role=roles[i],spec=cfg.layers[role],l;
  if(components[role]){l=main.layers.add(components[role]);l.name='ROLE_'+role.toUpperCase();}else l=main.layer('ROLE_'+role.toUpperCase());
  l.threeDLayer=true;l.collapseTransformation=spec.collapse;l.transform.position.setValue([960,540,spec.z]);
  l.startTime=spec.start_frame/cfg.fps;l.inPoint=l.startTime;l.outPoint=Math.min(cfg.duration,l.startTime+l.source.duration);l.moveToBeginning();
  if(role==='polar'||role==='streaks'){var key=l.effect.addProperty('ADBE Linear Color Key2');key.property('ADBE Linear Color Key2-0003').setValue([1,1,1,1]);key.property('ADBE Linear Color Key2-0005').setValue(0);key.property('ADBE Linear Color Key2-0006').setValue(10);}
 }
 var radial=main.layers.add(components.radial);radial.name='ROLE_RADIAL';radial.threeDLayer=true;radial.transform.position.setValue([960,540,0]);radial.transform.scale.setValue([159,159,159]);radial.moveToEnd();
 radial.transform.opacity.setValueAtTime(28/24,100);radial.transform.opacity.setValueAtTime(37/24,0);
 var bg=components.background.layer('bg');bg.copyToComp(main);bg=main.layer('bg');if(!bg||!bg.effect('ADBE 4ColorGradient'))throw Error('Copied native background missing');bg.name='ROLE_BACKGROUND';bg.moveToEnd();bg.effect('ADBE 4ColorGradient').property('ADBE 4ColorGradient-0009').setValue(cfg.background_blend);
 main.layer('Camera 1').moveToBeginning();
 var rq=app.project.renderQueue.items.add(main),om=rq.outputModule(1),selected='';
 for(var i=0;i<om.templates.length;i++)if(/H\.264/.test(om.templates[i])&&/15 Mbps/.test(om.templates[i])){selected=om.templates[i];break;}
 if(!selected)throw Error('Native H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 stage='save reopen';app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
 var point=main.layer('ROLE_BACKGROUND').effect('ADBE 4ColorGradient').property('ADBE 4ColorGradient-0003'),before=point.value;
 point.setValue([before[0]+1,before[1]]);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
 point=main.layer('ROLE_BACKGROUND').effect('ADBE 4ColorGradient').property('ADBE 4ColorGradient-0003');var changed=point.value;if(changed[0]!==before[0]+1)errors.push('Gradient edit lost');point.setValue(before);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
 var restored=main.layer('ROLE_BACKGROUND').effect('ADBE 4ColorGradient').property('ADBE 4ColorGradient-0003').value;if(restored[0]!==before[0])errors.push('Gradient restore failed');
 stage='native checks';var expressionCount=0,media=[],cameraTrace=[],fadeTrace=[];
 function inspect(p){if(p.propertyType===PropertyType.PROPERTY){if(p.canSetExpression&&p.expressionEnabled){expressionCount++;p.valueAtTime(1,false);if(p.expressionError)errors.push(p.expressionError);}}else for(var j=1;j<=p.numProperties;j++)inspect(p.property(j));}
 for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof CompItem)for(var j=1;j<=item.numLayers;j++)inspect(item.layer(j));else if(item instanceof FootageItem&&item.file){media.push({path:item.file.fsName,missing:item.footageMissing});if(item.footageMissing)errors.push('Missing media');}}
 if(media.length)errors.push('Unexpected external media');
 for(var f=0;f<480;f++){cameraTrace.push(main.layer('Camera 1').transform.position.valueAtTime(f/24,false));fadeTrace.push(main.layer('ROLE_RADIAL').transform.opacity.valueAtTime(f/24,false));}
 if(fadeTrace[28]!==100||fadeTrace[37]!==0||fadeTrace[0]!==100)errors.push('Radial fade differs');
 for(var i=1;i<=main.numLayers;i++){var l=main.layer(i);var row={index:i,name:l.name,inPoint:l.inPoint,outPoint:l.outPoint,threeD:l.threeDLayer};if(l instanceof AVLayer){row.source=l.source?l.source.name:null;row.collapse=l.collapseTransformation;row.position=l.transform.position.value;row.scale=l.transform.scale.value;var key=l.effect('ADBE Linear Color Key2');if(key)row.white_key={color:key.property('ADBE Linear Color Key2-0003').value,tolerance:key.property('ADBE Linear Color Key2-0005').value,softness:key.property('ADBE Linear Color Key2-0006').value};}records.push(row);}
 if(main.numLayers!==11)errors.push('Main layer count differs');
 // Camera points toward increasing Z. The inherited end camera is in front of the title.
 // Preserve the observed title depth; expose the unresolved layout instead of silently repairing it.
 var title=main.layer('ROLE_TITLE'),titleBehind=[];
 for(var f=Math.ceil(title.inPoint*24);f<Math.min(480,Math.ceil(title.outPoint*24));f++)if(title.transform.position.value[2]<=cameraTrace[f][2])titleBehind.push(f);
 still(main,0);still(main,24);still(main,240);still(main,479);still(main,96);still(main,144);still(main,216);
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,expressions_checked:expressionCount,selected_template:selected,output_format:'mp4',native_frames_checked:480,
  native_png_exports:['native-still-0.png','native-still-24.png','native-still-240.png','native-still-479.png','native-still-96.png','native-still-144.png','native-still-216.png'],
  layers:records,camera_trace:cameraTrace,radial_opacity_trace:fadeTrace,background_edit:{before:before,changed:changed,restored:restored},media:media,missing_media:[],
  gradient:{blend:main.layer('ROLE_BACKGROUND').effect('ADBE 4ColorGradient').property('ADBE 4ColorGradient-0009').value},
  unresolved_title_behind_camera_frames:titleBehind,course_fidelity:'candidate; estimated timing and inherited component limits; title projection unresolved; not a finished title film',rendered:false});
}catch(e){write({status:'failed',stage:stage,error:e.toString(),line:e.line});}
})();
