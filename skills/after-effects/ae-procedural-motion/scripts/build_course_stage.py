"""Reproduce the explicitly observed p06 04:20 opacity stage, before Trim Paths.

This is a course fragment candidate. Unknown final-course settings are not guessed.
"""
import argparse,json,hashlib,shutil
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--stage',choices=['opacity','trim-linear','trim-final'],default='opacity');ap.add_argument('--delay-frames',type=int,default=2);ap.add_argument('--asset',type=Path);a=ap.parse_args();out=a.out.resolve()
if not 1<=a.delay_frames<=10:raise ValueError('Delay must be 1–10 whole frames in this course profile')
if a.asset and (a.stage!='opacity' or not a.asset.is_file() or a.asset.suffix.lower()!='.png'):raise ValueError('PNG still inputs are a separate opacity/transform generalization; Trim Paths applies to the native vector branch only')
if out.exists():raise FileExistsError('Use a fresh course reproduction directory')
out.mkdir(parents=True)
cfg={'name':'COURSE_P06_OPACITY_STAGE','width':1080,'height':1080,'fps':30,'duration':7,'count':11,'source':'BV1Yh4y1A7XT?p=6 02:12-04:20','scope':'Intermediate opacity-stagger stage, camera disabled, before Trim Paths; not the final lesson effect','color_status':'FF0000 explicitly visible in p5 09:22 color dialog','bits_per_channel':16,'course_fidelity_status':'candidate_pending_visual_comparison'}
cfg['final_stage']=a.stage!='opacity';cfg['apply_ease_in']=a.stage=='trim-final';cfg['master_fade_seconds']=1 if a.stage=='trim-final' else 10/30
cfg['delay_frames']=a.delay_frames
cfg['asset']=None
if a.asset:
    (out/'assets').mkdir();target=out/'assets/input.png';shutil.copy2(a.asset,target);cfg['asset']=target.as_posix();cfg['asset_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();cfg['scope']+='; original PNG opacity/transform generalization, not a tutorial vector reproduction'
if cfg['final_stage']:
    cfg.update(name='COURSE_P06_TRIM_FINAL',count=18,source='BV1Yh4y1A7XT?p=6 05:00-07:25 plus inherited p5 camera',scope='Final Trim Paths and opacity staggering, one-node moving camera, native Easy Ease In',trim_end_seconds=31/30,camera_zoom=1866.6666666667,camera_speed=1000,parameter_provenance={'trim_end_seconds':'inferred from source frame 3 showing linear Trimpath 9.68 before easing; validate native eased value against visible 11.62','camera_zoom':'inferred from visible initial Z=-1866.7 and camera dialog angle 32.27 / focal length 62.22mm','exact_RGB':'FF0000 explicitly visible in p5 09:22','bits_per_channel':'16-bit inferred from color dialog maximum channel value 32768'})
if a.stage=='trim-linear':cfg.update(name='COURSE_P06_TRIM_LINEAR',trim_end_seconds=10/30,source='BV1Yh4y1A7XT?p=6 06:50–06:55 before duration extension',scope='Intermediate linear Trim Paths before extending master keyframe durations and applying Ease In')
if a.delay_frames!=2:cfg['scope']+='; explicit delay variation, not the course final setting'
(out/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
encoder=(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')
body=r'''(function(){__ENCODER__
var out=__OUT__,cfg=__CONFIG__;
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function slider(layer,name,value){var e=layer.property('ADBE Effect Parade').addProperty('ADBE Slider Control');e.name=name;e.property(1).setValue(value);}
try{
 if(app.project&&app.project.numItems>0){var owned=true,hasComp=false;for(var q=1;q<=app.project.numItems;q++)if(app.project.item(q) instanceof CompItem){hasComp=true;if(app.project.item(q).comment!=='video-skills-lab:course-reproduction')owned=false;}if(owned&&hasComp&&!app.project.dirty)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);else throw Error('This course baseline requires a fresh empty AE project; preserve existing work');}
 if(!app.project)app.newProject();
 app.project.bitsPerChannel=16;
 var comp=app.project.items.addComp(cfg.name,1080,1080,1,7,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[0,0,0];
 var ctrl=comp.layers.addNull();ctrl.name='controls';ctrl.threeDLayer=true;
 ctrl.property('ADBE Transform Group').property('ADBE Position').setValue([540,540,500]);
 slider(ctrl,'Size',1080);slider(ctrl,'Stroke Width',5);slider(ctrl,'Position Z spacing',1000);slider(ctrl,'Rotation Z spacing',0);slider(ctrl,'Scale interval',10);slider(ctrl,'Time offset',cfg.delay_frames);
 ctrl.property('ADBE Effect Parade').property('Rotation Z spacing').property(1).expression='time*5';
 var color=ctrl.property('ADBE Effect Parade').addProperty('ADBE Color Control');color.name='Stroke Color';color.property(1).setValue([1,0,0]);
 if(cfg.final_stage)slider(ctrl,'Trimpath',0);
 var opacity=ctrl.property('ADBE Transform Group').property('ADBE Opacity');opacity.setValueAtTime(0,0);opacity.setValueAtTime(cfg.master_fade_seconds,100);
 for(var k=1;k<=opacity.numKeys;k++)opacity.setInterpolationTypeAtKey(k,KeyframeInterpolationType.LINEAR,KeyframeInterpolationType.LINEAR);
 var delayed='ref=thisComp.layer("controls").transform.opacity;\nmyTime=framesToTime(thisComp.layer("controls").effect("Time offset")("Slider"));\nmyIndex=index-thisComp.layer("controls").index;\noffset=myTime*myIndex;\nref.valueAtTime(time-offset);';
 var assetComp=null;
 if(cfg.asset){var imported=app.project.importFile(new ImportOptions(new File(cfg.asset)));assetComp=app.project.items.addComp('SOURCE_ASSET',1080,1080,1,7,30);assetComp.comment='video-skills-lab:course-reproduction';var original=assetComp.layers.add(imported);original.name='ORIGINAL_INPUT';original.property('ADBE Transform Group').property('ADBE Position').setValue([540,540]);var fit=100*1080/Math.max(imported.width,imported.height);original.property('ADBE Transform Group').property('ADBE Scale').setValue([fit,fit]);}
 for(var i=1;i<=cfg.count;i++){
  var shape=cfg.asset?comp.layers.add(assetComp):comp.layers.addShape();shape.name=String(i);shape.threeDLayer=true;shape.moveAfter(ctrl);
  if(!cfg.asset){
  var root=shape.property('ADBE Root Vectors Group');var group=root.addProperty('ADBE Vector Group');group.name='Rectangle 1';
  var rect=group.property('ADBE Vectors Group').addProperty('ADBE Vector Shape - Rect');
  rect.property('ADBE Vector Rect Size').expression='temp=thisComp.layer("controls").effect("Size")("Slider");[temp,temp];';rect.property('ADBE Vector Rect Roundness').setValue(0);
  var stroke=group.property('ADBE Vectors Group').addProperty('ADBE Vector Graphic - Stroke');stroke.property('ADBE Vector Stroke Width').expression='thisComp.layer("controls").effect("Stroke Width")("Slider");';stroke.property('ADBE Vector Stroke Color').expression='thisComp.layer("controls").effect("Stroke Color")("Color");';
  if(cfg.final_stage){var trim=group.property('ADBE Vectors Group').addProperty('ADBE Vector Filter - Trim');trim.property('ADBE Vector Trim End').expression=delayed.replace('transform.opacity','effect("Trimpath")(1)');}
  }
  var transform=shape.property('ADBE Transform Group');
  var common='myIndex=index-thisComp.layer("controls").index-1;\n';
  transform.property('ADBE Position').expression='ref=thisComp.layer("controls").transform.position;\n'+common+'spacing=thisComp.layer("controls").effect("Position Z spacing")("Slider");\noffset=myIndex*spacing;\nref+[0,0,offset];';
  transform.property('ADBE Scale').expression='ref=thisComp.layer("controls").transform.scale;\n'+common+'spacing=thisComp.layer("controls").effect("Scale interval")("Slider");\noffset=myIndex*spacing;\nref+[offset,offset,offset];';
  transform.property('ADBE Rotate Z').expression='ref=thisComp.layer("controls").transform.zRotation;\n'+common+'spacing=thisComp.layer("controls").effect("Rotation Z spacing")("Slider");\noffset=myIndex*spacing;\nref+offset;';
  transform.property('ADBE Opacity').expression=delayed;
 }
 var camera=comp.layers.addCamera('Camera 1',[540,540]);camera.enabled=false;camera.moveToBeginning();ctrl.moveAfter(camera);
 var easeCommand=0;
 if(cfg.final_stage){
  camera.enabled=true;camera.autoOrient=AutoOrientType.NO_AUTO_ORIENT;
  camera.property('ADBE Camera Options Group').property('ADBE Camera Zoom').setValue(cfg.camera_zoom);
  var cp=camera.property('ADBE Transform Group').property('ADBE Position');cp.setValue([540,540,-cfg.camera_zoom]);cp.dimensionsSeparated=true;
  cp.getSeparationFollower(2).expression='value+time*1000';
  var trimControl=ctrl.property('ADBE Effect Parade').property('Trimpath').property(1);trimControl.setValueAtTime(0,0);trimControl.setValueAtTime(cfg.trim_end_seconds,100);
  for(var k=1;k<=2;k++)trimControl.setInterpolationTypeAtKey(k,KeyframeInterpolationType.LINEAR,KeyframeInterpolationType.LINEAR);
  comp.openInViewer();for(var q=1;q<=comp.numLayers;q++)comp.layer(q).selected=false;ctrl.selected=true;
  opacity.selected=true;trimControl.selected=true;for(var k=1;k<=2;k++){opacity.setSelectedAtKey(k,true);trimControl.setSelectedAtKey(k,true);}
  if(cfg.apply_ease_in){easeCommand=app.findMenuCommandId('缓入');if(easeCommand!==2510)throw Error('Native Easy Ease In command differs from inspected host');app.executeCommand(easeCommand);}
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='',format='';
 for(var i=0;i<templates.length;i++)if(/PNG/.test(templates[i])&&!/alpha|Alpha/.test(templates[i])){selected=templates[i];format='png';break;}
 if(selected){new Folder(out+'/render').create();om.applyTemplate(selected);om.file=new File(out+'/render/frame_[#####].png');}
 else{for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];format='mp4';break;}if(!selected)throw Error('No tested native export template');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');}
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
 comp=app.project.item(1);for(var q=1;q<=app.project.numItems;q++)if(app.project.item(q).name===cfg.name)comp=app.project.item(q);
 ctrl=comp.layer('controls');var errors=[],maxOpacity=0,maxPosition=0,maxRotation=0;
 // Actual live edit, then restore, save and reopen the self-owned course project.
 var delayControl=ctrl.property('ADBE Effect Parade').property('Time offset').property(1),originalDelay=delayControl.value,probeDelay=originalDelay===2?5:2;
 var probeTime=cfg.final_stage?20/30:5/30;
 var probeLayer=comp.layer(3).property('ADBE Transform Group').property('ADBE Opacity'),before=probeLayer.valueAtTime(probeTime,false);
 delayControl.setValue(probeDelay);var after=probeLayer.valueAtTime(probeTime,false);
 if(Math.abs(after-before)<.001)errors.push('Native delay parameter edit did not alter animation');
 delayControl.setValue(originalDelay);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
 for(var q=1;q<=app.project.numItems;q++)if(app.project.item(q).name===cfg.name)comp=app.project.item(q);ctrl=comp.layer('controls');
 if(ctrl.property('ADBE Effect Parade').property('Time offset').property(1).value!==originalDelay)errors.push('Restored native delay was not saved');
 var maxTrim=0;opacity=ctrl.property('ADBE Transform Group').property('ADBE Opacity');
 for(var i=3;i<=cfg.count+2;i++){var layer=comp.layer(i),tr=layer.property('ADBE Transform Group'),n=i-ctrl.index;
  for(var f=0;f<210;f++){var t=f/30,expected=cfg.final_stage?opacity.valueAtTime(t-n*cfg.delay_frames/30,false):Math.max(0,Math.min(100,(t-n*cfg.delay_frames/30)*300));
   maxOpacity=Math.max(maxOpacity,Math.abs(tr.property('ADBE Opacity').valueAtTime(t,false)-expected));
   maxPosition=Math.max(maxPosition,Math.abs(tr.property('ADBE Position').valueAtTime(t,false)[2]-(500+(n-1)*1000)));
   maxRotation=Math.max(maxRotation,Math.abs(tr.property('ADBE Rotate Z').valueAtTime(t,false)-(n-1)*t*5));
   if(cfg.final_stage){var nativeTrim=layer.property('ADBE Root Vectors Group').property(1).property('ADBE Vectors Group').property('ADBE Vector Filter - Trim').property('ADBE Vector Trim End');var masterTrim=ctrl.property('ADBE Effect Parade').property('Trimpath').property(1);maxTrim=Math.max(maxTrim,Math.abs(nativeTrim.valueAtTime(t,false)-masterTrim.valueAtTime(t-n*cfg.delay_frames/30,false)));}
  }
  for(var j=1;j<=tr.numProperties;j++)if(tr.property(j).canSetExpression&&tr.property(j).expressionError)errors.push(layer.name+':'+tr.property(j).expressionError);
 }
 var easedTrimAt3Frames=null,easeIncoming=null,easeType=null,missingMedia=[];
 for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof FootageItem&&app.project.item(i).footageMissing)missingMedia.push(app.project.item(i).name);
 if(missingMedia.length)errors.push('Missing original PNG input');
 if(cfg.final_stage){var masterTrim=ctrl.property('ADBE Effect Parade').property('Trimpath').property(1);easedTrimAt3Frames=masterTrim.valueAtTime(3/30,false);easeIncoming=masterTrim.keyInTemporalEase(2)[0].influence;easeType=String(masterTrim.keyInInterpolationType(2));if(cfg.apply_ease_in&&Math.abs(easedTrimAt3Frames-11.62)>.03)errors.push('Eased value does not match visible course 11.62 at frame 3');}
 if(maxOpacity>1e-5||maxPosition>1e-5||maxRotation>1e-5||maxTrim>1e-5)errors.push('Course formula mismatch');
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:format,output_templates:templates,layers:comp.numLayers,camera_enabled:comp.layer('Camera 1').enabled,bits_per_channel:app.project.bitsPerChannel,stroke_color:ctrl.property('ADBE Effect Parade').property('Stroke Color').property(1).value,renderer:comp.renderer,maximum_opacity_error:maxOpacity,maximum_z_error:maxPosition,maximum_rotation_error:maxRotation,maximum_trim_error:maxTrim,native_delay_edit:{original:originalDelay,changed:probeDelay,opacity_before:before,opacity_after:after,restored_and_reopened:true},native_ease_command:easeCommand,eased_trim_at_3_frames:easedTrimAt3Frames,last_key_incoming_influence:easeIncoming,last_key_incoming_type:easeType,course_scope:cfg.scope,course_fidelity_status:'candidate_pending_final_playback_comparison',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());'''
body=body.replace('__ENCODER__',encoder).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__CONFIG__',json.dumps(cfg,ensure_ascii=False))
# The course uses English Slider/Color display names. Keep the same property and
# expression logic but address its first parameter on the Chinese AE installation.
body=body.replace('("Slider")','(1)').replace('("Color")','(1)')
(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
