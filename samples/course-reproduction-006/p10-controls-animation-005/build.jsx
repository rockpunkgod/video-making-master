(function(){// Character-wise escaping avoids this Premiere host's replacement-string backslash behavior.
function encode(value) {
    if(value===null)return 'null';
    if(typeof value==='string'){
        var out=String.fromCharCode(34);
        for(var i=0;i<value.length;i++){
            var c=value.charCodeAt(i);
            if(c===34||c===92)out+=String.fromCharCode(92,c);
            else if(c<32){var hex=c.toString(16);while(hex.length<4)hex='0'+hex;out+=String.fromCharCode(92)+'u'+hex;}
            else out+=value.charAt(i);
        }
        return out+String.fromCharCode(34);
    }
    if(typeof value==='number'){if(!isFinite(value))throw Error('Non-finite JSON number');return String(value);}
    if(typeof value==='boolean')return String(value);
    var entries=[],key;
    if(value instanceof Array){for(var i=0;i<value.length;i++)entries.push(encode(value[i]));return '['+entries.join(',')+']';}
    for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
    return '{'+entries.join(',')+'}';
}

var cfg={"name": "P10_CONTROLLER_ANIMATION_ADAPTATION", "width": 1080, "height": 1080, "fps": 30, "duration": 8, "seed": 10, "num": 300, "columns": 30, "font": "DMSans-Bold", "font_size": 35, "source": "BV1Yh4y1A7XT?p=10 09:32 complete decimal loop, 10:50 binary variant", "status": "candidate", "observed": "seed201,num262,columns30,DM Sans Bold35,1080square30fps5s16bpc; loop seedRandom(seed+i) without true", "inferred": "Intro full-canvas black/white appearance observed; box650px centered atx215 inferred from viewport, not source AEP property; positionsy138/592 retained as inferred. Intro35-column wrapping failure is not used as a production keyframe.", "timeless": true, "animation": "controls-demo", "motion_expectation": "required", "box_width": 650, "box_left": 215, "adaptation": "Intro00:43\u201301:20 manually changes seed10\u219289\u2192122 and num300\u2192198\u2192201 at fixed comp time. Editable HOLD keyframes at output1/2/3.5/5s are our temporal adaptation, not demonstrated tutorial keyframes. Timeless prevents unintended full-frame random changes between these keys.", "binary_seed": 158},out="E:/自媒体/video-skills-lab/samples/course-reproduction-006/p10-controls-animation-005";
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function locate(){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===cfg.name)return app.project.item(i);throw Error('Missing composition');}
function slider(l,n,v){var e=l.effect.addProperty('ADBE Slider Control');e.name=n;e.property(1).setValue(v);}
function editAtZero(prop,value){if(prop.numKeys)prop.setValueAtKey(1,value);else prop.setValue(value);}
try{
 var fonts=app.fonts.getFontsByPostScriptName(cfg.font);if(!fonts||!fonts.length)throw Error('Required course font DMSans-Bold missing; inspect bundled font/license and session load helper, then native font probe; no substitution');
 if(app.project&&app.project.numItems>0){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;var comp=app.project.items.addComp(cfg.name,1080,1080,1,cfg.duration,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=cfg.animation==='controls-demo'?[0,0,0]:[224/255,224/255,224/255];
 var names=['num','num 2'];
 for(var i=0;i<2;i++){
  var layer=comp.layers.addBoxText([cfg.box_width,420]);layer.name=names[i];layer.transform.anchorPoint.setValue([0,0]);
  var source=layer.property('ADBE Text Properties').property('ADBE Text Document'),doc=source.value;doc.text='0';doc.font=cfg.font;doc.fontSize=cfg.font_size;doc.applyFill=true;doc.fillColor=[0,0,0];doc.applyStroke=false;doc.autoLeading=true;doc.justification=ParagraphJustification.FULL_JUSTIFY_LASTLINE_FULL;source.setValue(doc);
  if(cfg.animation==='controls-demo'){doc.fillColor=[1,1,1];source.setValue(doc);}
  var boxOrigin=source.value.boxTextPos;layer.transform.position.setValue([cfg.box_left-boxOrigin[0],(i===0?138:592)-boxOrigin[1]]);
  slider(layer,'seed',cfg.seed);slider(layer,'num',cfg.num);slider(layer,'columns',cfg.columns);
  if(cfg.animation==='controls-demo'){
   if(i===1)layer.effect('seed')(1).setValue(cfg.binary_seed);
   else{
    var seedKeys=[[0,10],[1,89],[2,122]],numKeys=[[0,300],[3.5,198],[5,201]];
    for(var k=0;k<seedKeys.length;k++)layer.effect('seed')(1).setValueAtTime(seedKeys[k][0],seedKeys[k][1]);
    for(var k=0;k<numKeys.length;k++)layer.effect('num')(1).setValueAtTime(numKeys[k][0],numKeys[k][1]);
    for(var nameIndex=0;nameIndex<2;nameIndex++){var prop=layer.effect(nameIndex===0?'seed':'num')(1);for(var k=1;k<=prop.numKeys;k++)prop.setInterpolationTypeAtKey(k,KeyframeInterpolationType.HOLD,KeyframeInterpolationType.HOLD);}
   }
  }
  source.expression='s="";\nn=effect("num")(1);\nseed=effect("seed")(1);\ncol=effect("columns")(1);\n\nfor(i=1;i<=n;i++){\n seedRandom(seed+i'+(cfg.timeless?',true':'')+');\n // generate a random number\n randValue=Math.round(random('+(i===0?'9':'')+'));\n // add to string\n s+=randValue;\n // add linebreak at last column\n if(i%col==0) s+="\\n";\n}\ns;';
 }
 var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),templates=om.templates,selected='';for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}if(!selected)throw Error('Tested H264 output template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();
 var errors=[],layers=[];
 for(var i=0;i<2;i++){
  var layer=comp.layer(names[i]),source=layer.property('ADBE Text Properties').property('ADBE Text Document'),seen={},frame0='',last='',changed=0,fontRecord=null,minX=1080,minY=1080,maxX=0,maxY=0;
  var previousControls='',unexpectedChanges=0;
  for(var f=0;f<cfg.duration*30;f++){
   var doc=source.valueAtTime(f/30,false),text=doc.text,flat=text.replace(/[\r\n]/g,'');seen[text]=true;
   if(f===0){frame0=text;fontRecord={font:doc.font,font_family:doc.fontFamily,font_style:doc.fontStyle,font_size:doc.fontSize,box_text:doc.boxText,justification:String(doc.justification)};}
   var expectedNum=Math.floor(layer.effect('num')(1).valueAtTime(f/30,false)),expectedColumns=Math.floor(layer.effect('columns')(1).valueAtTime(f/30,false));
   if(flat.length!==expectedNum|| (i===0?/[^0-9]/:/[^01]/).test(flat))errors.push(names[i]+': wrong digit count or alphabet at frame'+f);
   var rows=text.replace(/\r\n/g,'\n').replace(/\r/g,'\n').split('\n');if(rows[rows.length-1]==='')rows.pop();
   if(rows.length!==Math.ceil(expectedNum/expectedColumns))errors.push(names[i]+': line count');
   for(var row=0;row<rows.length;row++)if(rows[row].length!==Math.min(expectedColumns,expectedNum-row*expectedColumns))errors.push(names[i]+': column count');
   var controls=expectedNum+'|'+expectedColumns+'|'+layer.effect('seed')(1).valueAtTime(f/30,false);
   if(f&&text!==last){changed++;if(cfg.timeless&&controls===previousControls)unexpectedChanges++;}last=text;previousControls=controls;if(doc.font!==cfg.font)errors.push('Font substitution');
   var bounds=layer.sourceRectAtTime(f/30,false),position=layer.transform.position.value;minX=Math.min(minX,bounds.left+position[0]);minY=Math.min(minY,bounds.top+position[1]);maxX=Math.max(maxX,bounds.left+bounds.width+position[0]);maxY=Math.max(maxY,bounds.top+bounds.height+position[1]);
  }
  var unique=0;for(var key in seen)if(seen.hasOwnProperty(key))unique++;if(cfg.animation==='static'&&(changed!==0||unique!==1))errors.push('Stable typography changed over time');if(cfg.animation==='controls-demo'&&(unexpectedChanges!==0||(i===0&&changed!==4)||(i===1&&changed!==0)))errors.push('Controller animation has unintended changes or missing key transitions');if(cfg.animation==='course'&&changed<1)errors.push('Time-varying source seed unexpectedly frozen');if(source.expressionError)errors.push(source.expressionError);
  var seed=layer.effect('seed')(1),originalSeed=seed.valueAtTime(0,false),editText=frame0,seedDelta=0;while(editText===frame0&&seedDelta<32){seedDelta++;editAtZero(seed,originalSeed+seedDelta);editText=source.valueAtTime(0,false).text;}editAtZero(seed,originalSeed);if(editText===frame0||source.valueAtTime(0,false).text!==frame0)errors.push('Seed edit/restore failed');
  if(minX<0||minY<0||maxX>1080||maxY>1080)errors.push('Text clipped outside course canvas');
  var rect=layer.sourceRectAtTime(0,false);layers.push({name:names[i],font:fontRecord,frame0_text:frame0,unique_frame_strings:unique,consecutive_changes:changed,unexpected_changes_with_same_controls:unexpectedChanges,seed_edit_changed:editText!==frame0,seed_edit_delta:seedDelta,canvas_bounds_all_frames:{min_x:minX,min_y:minY,max_x:maxX,max_y:maxY},source_rect:{left:rect.left,top:rect.top,width:rect.width,height:rect.height}});
 }
 // A real num edit, saved/reopened and checked, then restored and reopened.
 var layer=comp.layer('num'),newNum=cfg.num>1?cfg.num-1:2;editAtZero(layer.effect('num')(1),newNum);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var changedLength=comp.layer('num').text.sourceText.valueAtTime(0,false).text.replace(/[\r\n]/g,'').length;if(changedLength!==newNum)errors.push('Saved num edit not evaluated');
 editAtZero(comp.layer('num').effect('num')(1),cfg.num);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=locate();var restoredLength=comp.layer('num').text.sourceText.valueAtTime(0,false).text.replace(/[\r\n]/g,'').length;if(restoredLength!==cfg.num)errors.push('Num restore not saved');
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',layers:comp.numLayers,bits_per_channel:app.project.bitsPerChannel,text_layers:layers,native_num_edit:{original:cfg.num,changed:newNum,read_after_reopen:changedLength,restored_after_reopen:restoredLength},font_available:true,course_fidelity_status:'candidate_pending_layout_comparison',rendered:false});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());