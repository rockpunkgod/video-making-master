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

var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-camera-precision-001",report;
try{
if(!app.project||app.project.dirty)throw Error('Preserve existing work');
for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment!=='video-skills-lab:course-reproduction')throw Error('Other project');
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.newProject();
var times=[23/24*.85,47/24*.85,81/24*.85,91/24*.85,144/24*.85,161/24*.85],zs=[-1866.6666666667,-7500,-8500,-12500,-12500,-21000],rows=[];
function expected(t){if(t<=times[0])return zs[0];for(var i=1;i<times.length;i++)if(t<=times[i]){var a=(t-times[i-1])/(times[i]-times[i-1]);return zs[i-1]*(1-a)+zs[i]*a;}return zs[zs.length-1];}
for(var mode=0;mode<3;mode++){
 var c=app.project.items.addComp('PRECISION_'+mode,1920,1080,1,20,24);c.comment='video-skills-lab:course-reproduction';
 var camera=c.layers.addCamera('CAMERA',[960,540]),p=camera.transform.position;
 if(mode===1){p.dimensionsSeparated=true;p=p.getSeparationFollower(2);}
 if(mode===2){var effect=c.layers.addNull().effect.addProperty('ADBE Slider Control');p=effect.property(1);}
 for(var i=0;i<times.length;i++)p.setValueAtTime(times[i],mode===0?[960,540,zs[i]]:zs[i]);
 for(var k=1;k<=p.numKeys;k++){p.setTemporalAutoBezierAtKey(k,false);p.setInterpolationTypeAtKey(k,KeyframeInterpolationType.LINEAR,KeyframeInterpolationType.LINEAR);if(mode===0){p.setSpatialAutoBezierAtKey(k,false);p.setSpatialTangentsAtKey(k,[0,0,0],[0,0,0]);}}
 var max=0,worst=null,keys=[];
 for(var k=1;k<=p.numKeys;k++)keys.push({time:p.keyTime(k),requested:times[k-1],value:p.keyValue(k)});
 for(var f=0;f<480;f++){var value=p.valueAtTime(f/24,false);if(mode===0)value=value[2];var error=Math.abs(value-expected(f/24));if(error>max){max=error;worst={frame:f,value:value,expected:expected(f/24)};}}
 rows.push({mode:mode===0?'combined_spatial':mode===1?'separated_Z':'slider_reference',max_error:max,worst:worst,keys:keys});
}
app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));report={status:'built',project_reopened:true,rows:rows};
}catch(e){report={status:'failed',error:e.toString(),line:e.line};}
var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(report));f.close();
}());