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

var out="E:/自媒体/video-skills-lab/samples/course-reproduction-008/p12-mirror-coordinate-probe-002",errors=[],records=[],exports=[];
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 if(!app.project)app.newProject();var centers=[0,540,1080];
 for(var k=0;k<centers.length;k++){
  var comp=app.project.items.addComp('MIRROR_'+centers[k],1080,1080,1,1,30);comp.comment='video-skills-lab:course-reproduction';comp.bgColor=[.88,.88,.88];var layer=comp.layers.addShape();layer.name='MARKERS';layer.transform.position.setValue([540,0]);var root=layer.property('ADBE Root Vectors Group'),positions=[[0,100],[100,200],[-100,300]];
  for(var i=0;i<positions.length;i++){var vectors=root.addProperty('ADBE Vector Group').property('ADBE Vectors Group'),circle=vectors.addProperty('ADBE Vector Shape - Ellipse');circle.property('ADBE Vector Ellipse Size').setValue([20,20]);circle.property('ADBE Vector Ellipse Position').setValue(positions[i]);var fill=vectors.addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').setValue([1,0,0]);}
  var mirror=layer.effect.addProperty('ADBE Mirror');mirror.property('ADBE Mirror-0001').setValue([centers[k],540]);mirror.property('ADBE Mirror-0002').setValue(0);records.push({name:comp.name,reflection_center:mirror.property(1).value,position:layer.transform.position.value,anchor:layer.transform.anchorPoint.value});
 }
 app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
 for(var k=0;k<centers.length;k++){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name==='MIRROR_'+centers[k]){var name='mirror-'+centers[k]+'.png';app.project.item(i).saveFrameToPng(0,new File(out+'/'+name));exports.push(name);}}
 write({status:'built',project_reopened:true,expression_errors:[],records:records,native_png_exports:exports,scope:'Actual native coordinate-space probe; no fitted output axis'});
}catch(e){write({status:'failed',error:e.toString(),line:e.line});}
}());