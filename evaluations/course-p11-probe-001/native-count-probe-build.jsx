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

var out="E:/自媒体/video-skills-lab/samples/course-reproduction-007/p11-count-probe-002",results=[],errors=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function slider(layer,name,value){var e=layer.effect.addProperty('ADBE Slider Control');e.name=name;e.property(1).setValue(value);}
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();app.project.bitsPerChannel=16;
 var base=app.project.items.addComp('baseShape',300,300,1,5,30);base.comment='video-skills-lab:course-reproduction';var shape=base.layers.addShape();shape.transform.position.setValue([150,150]);var group=shape.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group'),vectors=group.property('ADBE Vectors Group');var circle=vectors.addProperty('ADBE Vector Shape - Ellipse');circle.property('ADBE Vector Ellipse Size').setValue([100,100]);var fill=vectors.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').setValue([100/255,100/255,100/255]);
 var counts=[44,88,176];
 for(var c=0;c<counts.length;c++){
  var count=counts[c],comp=app.project.items.addComp('COUNT_'+count,1080,1080,1,5,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[224/255,224/255,224/255];var ctrl=comp.layers.addNull();ctrl.name='controls';slider(ctrl,'Phase',106);slider(ctrl,'Phase increment',63);slider(ctrl,'Z increment',35);slider(ctrl,'Radius',73);
  for(var i=1;i<=count;i++){
   var layer=comp.layers.add(base);layer.name='baseShape_'+i;layer.threeDLayer=true;layer.moveAfter(ctrl);slider(layer,'myIndex',0);layer.effect('myIndex')(1).expression='index-thisComp.layer("controls").index';
   layer.transform.position.expression='myIndex=effect("myIndex")(1);\nphaseInc=thisComp.layer("controls").effect("Phase increment")(1);\noffset=myIndex*phaseInc;\nphase=degreesToRadians(thisComp.layer("controls").effect("Phase")(1)+offset);\nzInc=thisComp.layer("controls").effect("Z increment")(1);\nr=thisComp.layer("controls").effect("Radius")(1)*Math.PI*2;\nx=r*Math.cos(phase);\ny=r*Math.sin(phase);\nz=zInc*myIndex;\n[x,y,z]+value;';
  }
  var maxError=0;for(var i=2;i<=comp.numLayers;i++){var layer=comp.layer(i),n=i-ctrl.index,angle=(106+n*63)*Math.PI/180,wanted=[540+73*Math.PI*2*Math.cos(angle),540+73*Math.PI*2*Math.sin(angle),35*n],actual=layer.transform.position.valueAtTime(0,false);for(var d=0;d<3;d++)maxError=Math.max(maxError,Math.abs(actual[d]-wanted[d]));if(layer.transform.position.expressionError)errors.push(layer.transform.position.expressionError);}
  if(maxError>1e-8)errors.push('Position mismatch');comp.saveFrameToPng(0,new File(out+'/count-'+count+'.png'));results.push({count:count,layers:comp.numLayers,max_position_error:maxError,rendered_native_png:'count-'+count+'.png'});
 }
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));var compCount=0;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){compCount++;var reopened=app.project.item(i);if(reopened.name.indexOf('COUNT_')===0&&reopened.numLayers!==Number(reopened.name.substring(6))+1)errors.push('Layer count mismatch on reopen');}if(compCount!==4)errors.push('Comp count mismatch on reopen');
 write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,results:results,source:'BV1Yh4y1A7XT p11 11:14',status_scope:'Actual AE hypothesis probe, not confirmed tutorial layer count or accepted skill',inferred:['circle100 based on narration/change of ellipse size','gray100/255','background224/255','count hypotheses44/88/176']});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());