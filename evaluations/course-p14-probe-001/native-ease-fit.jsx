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

var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-ease-fit-001",result;
try{
if(!app.project||app.project.dirty)throw Error('Dirty project preserved');
for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment!=='video-skills-lab:course-reproduction')throw Error('Other project preserved');
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.newProject();
var c=app.project.items.addComp('P14_EASE_FIT',1280,720,1,151/30,30);c.comment='video-skills-lab:course-reproduction';
var l=c.layers.addText('FIT'),a=l.property('ADBE Text Properties').property('ADBE Text Animators').addProperty('ADBE Text Animator');a.property('ADBE Text Animator Properties').addProperty('ADBE Text Opacity').setValue(0);
var p=a.property('ADBE Text Selectors').addProperty('ADBE Text Selector').property('ADBE Text Percent End');p.setValueAtTime(0,100);p.setValueAtTime(29/30,0);
for(var k=1;k<=2;k++){p.setTemporalAutoBezierAtKey(k,false);p.setTemporalContinuousAtKey(k,false);p.setInterpolationTypeAtKey(k,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);}
var target=[[.05,-152],[.1,-156],[.2,-149],[.3,-139],[.4,-125],[.5,-110],[.6,-91],[.7,-72],[.8,-48],[.9,-25]],rows=[];
for(var oi=1;oi<=81;oi+=2)for(var ii=1;ii<=91;ii+=2){
 p.setTemporalEaseAtKey(1,[new KeyframeEase(0,33.333)],[new KeyframeEase(-104.23,oi)]);p.setTemporalEaseAtKey(2,[new KeyframeEase(0,ii)],[new KeyframeEase(0,33.333)]);
 var score=0,speeds=[];for(var j=0;j<target.length;j++){var t=target[j][0]*29/30,v=(p.valueAtTime(t+.0001,false)-p.valueAtTime(t-.0001,false))/.0002;score+=Math.pow(v-target[j][1],2);speeds.push(v);}
 rows.push({outgoing:oi,incoming:ii,rms:Math.sqrt(score/target.length),speeds:speeds});
}
rows.sort(function(a,b){return a.rms-b.rms;});result={status:'built',project_reopened:true,targets:target,target_provenance:'Manual approximate readings of final source speed graph at06:00; source keyframe influences not directly read',top:rows.slice(0,10)};
app.project.save(new File(out+'/project.aep'));
}catch(e){result={status:'failed',error:e.toString(),line:e.line};}
var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(result));f.close();
}());