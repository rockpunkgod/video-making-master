"""Course p11 spatial equation rig. Static reference layout, not invented animation."""
import argparse,json,hashlib,shutil
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--count',type=int,default=176);ap.add_argument('--phase',type=float,default=106);ap.add_argument('--phase-step',type=float,default=63);ap.add_argument('--z-step',type=float,default=35);ap.add_argument('--radius',type=float,default=73);ap.add_argument('--asset',type=Path);ap.add_argument('--background',choices=['course','black'],default='course');a=ap.parse_args();out=a.out.resolve()
if out.exists():raise FileExistsError('Fresh output required')
if not 1<=a.count<=300 or not -3600<=a.phase<=3600 or not .1<=a.phase_step<=360 or not 1<=a.z_step<=1000 or not 1<=a.radius<=150:raise ValueError('Outside the bounded candidate profile')
if a.asset and (not a.asset.is_file() or a.asset.suffix.lower()!='.png'):raise ValueError('Only caller-owned PNG inputs supported by this variation')
out.mkdir(parents=True);cfg=dict(name='COURSE_P11_ALGORITHMIC_LAYOUT',width=1080,height=1080,fps=30,duration=5,count=a.count,phase=a.phase,phase_step=a.phase_step,z_step=a.z_step,radius=a.radius,motion_expectation='static_layout',asset=None,status='candidate',
 background=a.background,source='BV1Yh4y1A7XT?p=11 07:20 final+value,09:20 corrected multiplication,09:43 ellipse100,11:14 controls',
 observed='Phase106,Phase increment63,Z increment35,Radius73; r=Radius*PI*2; myIndex=index-controls.index; [x,y,z]+value',
 inferred='176 layers selected by actual AE silhouette comparison (not directly read); fill100/255,bg224/255 inferred. Black background is an explicit contrast variation, not tutorial gray baseline.',
 animation_scope='The source reference is paused. This output documents a static procedural rig; no animation acceptance claim or invented time/keyframes.')
if a.asset:
 (out/'assets').mkdir();target=out/'assets/input.png';shutil.copy2(a.asset,target);cfg.update(asset=target.as_posix(),asset_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),asset_scope='Original PNG baseShape substitution, not the tutorial circle')
(out/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
body=r'''(function(){__ENCODER__
var out=__OUT__,cfg=__CFG__,errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function slider(layer,name,value){var e=layer.effect.addProperty('ADBE Slider Control');e.name=name;e.property(1).setValue(value);}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing main comp');}
function ctrl(comp,name){return comp.layer('controls').effect(name)(1);}
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;
 var base=app.project.items.addComp('baseShape',300,300,1,5,30);base.comment='video-skills-lab:course-reproduction';
 if(cfg.asset){var footage=app.project.importFile(new ImportOptions(new File(cfg.asset)));var sourceLayer=base.layers.add(footage);sourceLayer.name='ORIGINAL_INPUT';sourceLayer.transform.position.setValue([150,150]);var fit=100*100/Math.max(footage.width,footage.height);sourceLayer.transform.scale.setValue([fit,fit]);}
 else{var shape=base.layers.addShape();shape.transform.position.setValue([150,150]);var vectors=shape.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group').property('ADBE Vectors Group'),circle=vectors.addProperty('ADBE Vector Shape - Ellipse');circle.property('ADBE Vector Ellipse Size').setValue([100,100]);var fill=vectors.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').setValue([100/255,100/255,100/255]);}
 var comp=app.project.items.addComp(cfg.name,1080,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=cfg.background==='black'?[0,0,0]:[224/255,224/255,224/255];var controls=comp.layers.addNull();controls.name='controls';slider(controls,'Phase',cfg.phase);slider(controls,'Phase increment',cfg.phase_step);slider(controls,'Z increment',cfg.z_step);slider(controls,'Radius',cfg.radius);
 for(var i=1;i<=cfg.count;i++){
  var layer=comp.layers.add(base);layer.name='baseShape_'+i;layer.threeDLayer=true;layer.moveAfter(controls);slider(layer,'myIndex',0);layer.effect('myIndex')(1).expression='index-thisComp.layer("controls").index';
  layer.transform.position.expression='myIndex=effect("myIndex")(1);\nphaseInc=thisComp.layer("controls").effect("Phase increment")(1);\noffset=myIndex*phaseInc;\nphase=degreesToRadians(thisComp.layer("controls").effect("Phase")(1)+offset);\nzInc=thisComp.layer("controls").effect("Z increment")(1);\nr=thisComp.layer("controls").effect("Radius")(1)*Math.PI*2;\nx=r*Math.cos(phase);\ny=r*Math.sin(phase);\nz=zInc*myIndex;\n[x,y,z]+value;';
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),selected='',templates=om.templates;for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();
 var stored={phase:ctrl(comp,'Phase').value,phase_step:ctrl(comp,'Phase increment').value,z_step:ctrl(comp,'Z increment').value,radius:ctrl(comp,'Radius').value};
 var maxError=0,indexError=0;for(var f=0;f<150;f++)for(var i=2;i<=comp.numLayers;i++){var layer=comp.layer(i),n=i-1,angle=(stored.phase+n*stored.phase_step)*Math.PI/180,wanted=[540+stored.radius*Math.PI*2*Math.cos(angle),540+stored.radius*Math.PI*2*Math.sin(angle),stored.z_step*n],actual=layer.transform.position.valueAtTime(f/30,false);indexError=Math.max(indexError,Math.abs(layer.effect('myIndex')(1).valueAtTime(f/30,false)-n));for(var d=0;d<3;d++)maxError=Math.max(maxError,Math.abs(actual[d]-wanted[d]));if(layer.transform.position.expressionError)errors.push(layer.transform.position.expressionError);}
 if(maxError>1e-8||indexError!==0)errors.push('Expression mismatch');
 var first=comp.layer(2).transform.position.valueAtTime(0,false);ctrl(comp,'Phase').setValue(cfg.phase+20);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var edited=comp.layer(2).transform.position.valueAtTime(0,false),editedPhase=ctrl(comp,'Phase').value;if(editedPhase!==cfg.phase+20||Math.abs(edited[0]-first[0])+Math.abs(edited[1]-first[1])<1)errors.push('Phase edit/reopen failed');
 ctrl(comp,'Phase').setValue(cfg.phase);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var restored=comp.layer(2).transform.position.valueAtTime(0,false);for(var d=0;d<3;d++)if(Math.abs(restored[d]-first[d])>1e-8)errors.push('Restore mismatch');
 var exports=[];for(var f=0;f<5;f++){var name='native-still-'+f+'.png';comp.saveFrameToPng(f,new File(out+'/'+name));exports.push(name);}
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,stored_controls:stored,max_position_error:maxError,max_index_error:indexError,static_layout_validated_frames:150,native_png_exports:exports,native_phase_edit:{original:cfg.phase,changed:editedPhase,restored:ctrl(comp,'Phase').value},course_fidelity_status:'candidate_static_layout_only_not_animation_verified',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());'''
body=body.replace('__ENCODER__',(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__CFG__',json.dumps(cfg));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
