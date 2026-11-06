"""Render a measured number-rig update profile with editable native controllers.

The profile records evidence and inference. No tutorial video is a runtime input.
"""
import argparse,json,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--profile',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seed-base',type=int);a=ap.parse_args();p=json.loads(a.profile.read_text(encoding='utf-8'));out=a.out.resolve()
if out.exists():raise FileExistsError('Fresh output required')
if p.get('schema_version')!=1 or p['fps']!=30 or not 1<=p['duration']<=30:raise ValueError('Unsupported bounded native profile')
style=p['typography'];times=p['update_times'];quantities=p['quantity_keys'];seed=p['seed_base'] if a.seed_base is None else a.seed_base
if times[0]!=0 or times!=sorted(set(times)) or any(not 0<=t<p['duration'] for t in times):raise ValueError('Unique sorted update times required')
if quantities[0][0]!=0 or any(not 0<=t<p['duration'] or not 1<=n<=1000 or int(n)!=n for t,n in quantities):raise ValueError('Invalid quantity keys')
if not -10000<=seed<=10000 or not 1<=style['columns']<=40 or not 100<=style['box_width']<=1080 or not 50<=style['box_height']<=1080:raise ValueError('Invalid layout/seed')
cfg=dict(p,name='SAMPLED_P10_NUMBER_RIG',width=1080,height=1080,seed_base=seed,animation='reference-sampled',motion_expectation='required',status='candidate',reference_profile=str(a.profile.resolve()),source_scope='Measured source update timing; inferred seed event IDs, not exact source seed values')
out.mkdir(parents=True);(out/'request.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
body=r'''(function(){__ENCODER__
var cfg=__CFG__,out=__OUT__,style=cfg.typography,errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing composition');}
function slider(l,n,v){var e=l.effect.addProperty('ADBE Slider Control');e.name=n;e.property(1).setValue(v);}
function edit(prop,v){if(prop.numKeys)prop.setValueAtKey(1,v);else prop.setValue(v);}
try{
 var fonts=app.fonts.getFontsByPostScriptName(style.font);if(!fonts||!fonts.length)throw Error('Required course font missing; no substitution');
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;var comp=app.project.items.addComp(cfg.name,1080,1080,1,cfg.duration,cfg.fps);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[0,0,0];
 for(var j=0;j<2;j++){
  var layer=comp.layers.addBoxText([style.box_width,style.box_height]);layer.name=j===0?'num':'binary_hidden';layer.transform.anchorPoint.setValue([0,0]);
  var source=layer.text.sourceText,doc=source.value;doc.text='0';doc.font=style.font;doc.fontSize=style.font_size;doc.applyFill=true;doc.fillColor=[1,1,1];doc.applyStroke=false;doc.autoLeading=true;doc.baselineShift=style.baseline_shift;doc.justification=ParagraphJustification.FULL_JUSTIFY_LASTLINE_FULL;source.setValue(doc);var box=source.value.boxTextPos;layer.transform.position.setValue([style.left-box[0],(j===0?style.top:592)-box[1]]);
  slider(layer,'seed',j===0?cfg.seed_base:158);slider(layer,'num',cfg.quantity_keys[0][1]);slider(layer,'columns',style.columns);
  if(j===0){
   var prop=layer.effect('seed')(1);for(var k=0;k<cfg.update_times.length;k++)prop.setValueAtTime(cfg.update_times[k],cfg.seed_base+k);for(var k=1;k<=prop.numKeys;k++)prop.setInterpolationTypeAtKey(k,KeyframeInterpolationType.HOLD,KeyframeInterpolationType.HOLD);
   prop=layer.effect('num')(1);for(var k=0;k<cfg.quantity_keys.length;k++)prop.setValueAtTime(cfg.quantity_keys[k][0],cfg.quantity_keys[k][1]);for(var k=1;k<=prop.numKeys;k++)prop.setInterpolationTypeAtKey(k,KeyframeInterpolationType.HOLD,KeyframeInterpolationType.HOLD);
  }else layer.enabled=false;
  source.expression='s="";\nn=effect("num")(1);\nseed=effect("seed")(1);\ncol=effect("columns")(1);\nfor(i=1;i<=n;i++){\nseedRandom(seed+i,true);\nrandValue=Math.round(random('+(j===0?'9':'')+'));\ns+=randValue;\nif(i%col==0)s+="\\n";\n}\ns;';
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='';for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var layer=comp.layer('num'),source=layer.text.sourceText,previousText='',previousControls='',changeFrames=[],unexpected=[],frameData=[];
 for(var f=0;f<cfg.duration*cfg.fps;f++){
  var t=f/cfg.fps,doc=source.valueAtTime(t,false),text=doc.text,num=layer.effect('num')(1).valueAtTime(t,false),seed=layer.effect('seed')(1).valueAtTime(t,false),col=layer.effect('columns')(1).valueAtTime(t,false),flat=text.replace(/[\r\n]/g,''),controls=num+'|'+seed+'|'+col;
  if(flat.length!==num||/[^0-9]/.test(flat)||doc.font!==style.font)errors.push('Wrong native number content/font');
  if(f&&text!==previousText){changeFrames.push(f);if(controls===previousControls)unexpected.push(f);}else if(f&&controls!==previousControls)errors.push('Controller change did not affect text');
  previousText=text;previousControls=controls;frameData.push({frame:f,num:num,seed:seed,composed_lines:typeof doc.composedLineCount==='undefined'?null:doc.composedLineCount});
 }
 if(unexpected.length||source.expressionError)errors.push('Unexpected per-frame randomness');if(comp.layer('binary_hidden').enabled)errors.push('Reference segment hides binary');
 var first=source.valueAtTime(0,false).text;edit(layer.effect('seed')(1),cfg.seed_base+1000);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var edited=comp.layer('num').text.sourceText.valueAtTime(0,false).text;if(edited===first)errors.push('Seed edit/reopen failed');edit(comp.layer('num').effect('seed')(1),cfg.seed_base);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();if(comp.layer('num').text.sourceText.valueAtTime(0,false).text!==first)errors.push('Restore failed');
 comp.saveFrameToPng(0,new File(out+'/reference-first-native.png'));
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,binary_hidden:!comp.layer('binary_hidden').enabled,native_frames:frameData,native_change_frames:changeFrames,unexpected_change_frames:unexpected,native_seed_edit:{original:cfg.seed_base,changed:cfg.seed_base+1000,restored:comp.layer('num').effect('seed')(1).valueAtTime(0,false)},course_fidelity_status:'candidate_measured_timing_inferred_seed_values_and_layout',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());'''
body=body.replace('__ENCODER__',(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__CFG__',json.dumps(cfg,ensure_ascii=False)).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False));(out/'build.jsx').write_text(body,encoding='utf-8');print(out/'build.jsx')
