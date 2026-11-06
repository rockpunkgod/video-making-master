(function () {
__ENCODER__
var cfg=__CONFIG__, out=__OUTPUT__, errors=[], stage='start';
function write(value) {
    var f=new File(out+'/receipt.json'); f.encoding='UTF-8';
    f.open('w'); f.write(encode(value)); f.close();
}
function compByName() {
    for(var i=1;i<=app.project.numItems;i++)
        if(app.project.item(i).name===cfg.name)return app.project.item(i);
    throw Error('Composition missing after reopen');
}
function anim(comp,name) {return comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Animators').property(name);}
function position(comp) {return anim(comp,'pos').property('ADBE Text Animator Properties').property('ADBE Text Position 3D');}
function end(comp) {return anim(comp,'opacity').property('ADBE Text Selectors').property(1).property('ADBE Text Percent End');}
function keys(p,from,to,startSpeed,outInfluence,inInfluence) {
    var endTime=cfg.reveal_frames/cfg.fps;
    p.setValueAtTime(0,from); p.setValueAtTime(endTime,to);
    for(var k=1;k<=2;k++) {
        p.setTemporalAutoBezierAtKey(k,false);
        p.setTemporalContinuousAtKey(k,false);
        p.setInterpolationTypeAtKey(k,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
    }
    p.setTemporalEaseAtKey(1,[new KeyframeEase(0,33.333)],[new KeyframeEase(startSpeed,outInfluence)]);
    p.setTemporalEaseAtKey(2,[new KeyframeEase(0,inInfluence)],[new KeyframeEase(0,33.333)]);
}
function keyRecord(p) {
    var result=[];
    for(var k=1;k<=p.numKeys;k++)result.push({time:p.keyTime(k),value:p.keyValue(k),
        incoming:{speed:p.keyInTemporalEase(k)[0].speed,influence:p.keyInTemporalEase(k)[0].influence},
        outgoing:{speed:p.keyOutTemporalEase(k)[0].speed,influence:p.keyOutTemporalEase(k)[0].influence}});
    return result;
}
try {
    if(app.project&&app.project.numItems) {
        var owned=true,hasComp=false;
        for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem) {
            hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')owned=false;
        }
        if(!owned||!hasComp||app.project.dirty)throw Error('Preserve existing work');
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    }
    if(!app.project)app.newProject();app.project.bitsPerChannel=16;
    var comp=app.project.items.addComp(cfg.name,cfg.width,cfg.height,1,cfg.duration,cfg.fps);
    comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[0,0,0];
    var layer=comp.layers.addText(cfg.text);layer.name='TITLE';
    var source=layer.property('ADBE Text Properties').property('ADBE Text Document'),doc=source.value;
    doc.font='DMSans-Bold';doc.fontSize=cfg.font_size;doc.applyFill=true;doc.fillColor=[1,1,1];doc.applyStroke=false;
    doc.tracking=0;doc.baselineShift=4;doc.justification=ParagraphJustification.LEFT_JUSTIFY;source.setValue(doc);
    if(source.value.font!=='DMSans-Bold')throw Error('Required course font unavailable');
    layer.transform.anchorPoint.setValue([0,0]);layer.transform.position.setValue(cfg.position);
    stage='position animator';
    var animators=layer.property('ADBE Text Properties').property('ADBE Text Animators');
    var pa=animators.addProperty('ADBE Text Animator');pa.name='pos';
    var pos=pa.property('ADBE Text Animator Properties').addProperty('ADBE Text Position 3D');
    keys(pos,[0,cfg.offset_y,0],[0,0,0],Math.abs(cfg.offset_y)/(cfg.reveal_frames/cfg.fps),14.5,36.2);
    var selectors=pa.property('ADBE Text Selectors');
    while(selectors.numProperties)selectors.property(1).remove();
    var ex=selectors.addProperty('ADBE Text Expressible Selector');
    ex.property('ADBE Text Range Type2').setValue(1);
    ex.property('ADBE Text Expressible Amount').expression='if(textIndex%2) -100; else 100';
    stage='opacity animator';
    var oa=animators.addProperty('ADBE Text Animator');oa.name='opacity';
    oa.property('ADBE Text Animator Properties').addProperty('ADBE Text Opacity').setValue(0);
    var rs=oa.property('ADBE Text Selectors').addProperty('ADBE Text Selector');
    rs.property('ADBE Text Percent Start').setValue(0);rs.property('ADBE Text Percent Offset').setValue(0);
    var advanced=rs.property('ADBE Text Range Advanced');
    var values={'ADBE Text Range Units':1,'ADBE Text Range Type2':1,'ADBE Text Selector Mode':1,
        'ADBE Text Selector Max Amount':100,'ADBE Text Range Shape':1,'ADBE Text Selector Smoothness':100,
        'ADBE Text Levels Max Ease':0,'ADBE Text Levels Min Ease':0,'ADBE Text Randomize Order':1,'ADBE Text Random Seed':cfg.random_seed};
    for(var n in values)if(values.hasOwnProperty(n))advanced.property(n).setValue(values[n]);
    keys(rs.property('ADBE Text Percent End'),100,0,-104.23*29/cfg.reveal_frames,9,45);
    stage='render queue';
    var rq=app.project.renderQueue.items.add(comp),om=rq.outputModule(1),selected='',templates=om.templates;
    for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}
    if(!selected)throw Error('Tested H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
    app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=compByName();
    stage='native checks';
    var p=position(comp),e=end(comp),samples=[],previousPos=cfg.offset_y,previousEnd=100;
    for(var f=0;f<151;f++) {
        var t=f/cfg.fps,v=p.valueAtTime(t,false),opacityEnd=e.valueAtTime(t,false);
        if(!isFinite(v[1])||!isFinite(opacityEnd)||v[1]<cfg.offset_y-0.001||v[1]>0.001||opacityEnd<-.001||opacityEnd>100.001)errors.push('Out of range curve');
        if(v[1]<previousPos-.001||opacityEnd>previousEnd+.001)errors.push('Reversed reveal curve');
        if(f>=cfg.reveal_frames&&(Math.abs(v[1])>.001||Math.abs(opacityEnd)>.001))errors.push('Unsettled end state');
        previousPos=v[1];previousEnd=opacityEnd;samples.push({frame:f,position_y:v[1],range_end:opacityEnd});
    }
    var expr=anim(comp,'pos').property('ADBE Text Selectors').property(1).property('ADBE Text Expressible Amount');
    if(expr.expressionError||expr.expression!=='if(textIndex%2) -100; else 100')errors.push('Expression failure');
    var before=comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Document').value.text;
    source=comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Document');doc=source.value;doc.text='EDIT TEST';source.setValue(doc);
    app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=compByName();
    var edited=comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Document').value.text;
    if(edited!=='EDIT TEST')errors.push('Text edit/reopen failed');
    source=comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Document');doc=source.value;doc.text=before;source.setValue(doc);
    app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));comp=compByName();
    source=comp.layer('TITLE').property('ADBE Text Properties').property('ADBE Text Document');
    if(source.value.text!==before||source.value.font!=='DMSans-Bold')errors.push('Text/font restore failed');
    var r=comp.layer('TITLE').sourceRectAtTime(1.5,false),x=cfg.position[0]+r.left,y=cfg.position[1]+r.top;
    if(x<0||x+r.width>cfg.width||y-Math.abs(cfg.offset_y)<0||y+r.height+Math.abs(cfg.offset_y)>cfg.height)errors.push('Text may be cropped; change explicit typography input');
    var exports=[],frames=[0,3,6,12,20,29,45,90,150];
    for(var i=0;i<frames.length;i++){var file='native-still-'+frames[i]+'.png';comp.saveFrameToPng(frames[i]/cfg.fps,new File(out+'/'+file));exports.push(file);}
    write({status:errors.length?'failed':'built',stage:stage,project_reopened:true,expression_errors:errors,selected_template:selected,
        output_format:'mp4',native_png_exports:exports,validated_frames:151,native_text_edit:{original:before,changed:edited,restored:source.value.text},
        native_font:source.value.font,final_bounds:{left:x,top:y,width:r.width,height:r.height},
        position_keys:keyRecord(position(comp)),end_keys:keyRecord(end(comp)),samples:samples,
        course_fidelity_status:cfg.fidelity,random_seed_provenance:'Native default0 retained for baseline; source seed unread',rendered:false});
}catch(error){write({status:'failed',error:error.toString(),line:error.line,stage:stage});}
}());
