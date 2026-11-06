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

var paths=["E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-003", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-geometry-001", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-typography-001", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-texture-001"],reports=[];
if(app.project&&app.project.dirty)throw Error('Dirty project preserved');
for(var ci=0;ci<paths.length;ci++){
 if(app.project&&app.project.numItems){for(var j=1;j<=app.project.numItems;j++)if(app.project.item(j) instanceof CompItem&&app.project.item(j).comment!=='video-skills-lab:course-reproduction')throw Error('Other project preserved');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.open(new File(paths[ci]+'/project.aep'));var main=null;
 for(var j=1;j<=app.project.numItems;j++)if(app.project.item(j).name==='COURSE_P13_COMPOSITE')main=app.project.item(j);
 if(!main)throw Error('Wrong case');var p=main.layer('Camera 1').transform.position,keys=[];
 for(var k=1;k<=p.numKeys;k++)keys.push({time:p.keyTime(k),value:p.keyValue(k),in_type:String(p.keyInInterpolationType(k)),out_type:String(p.keyOutInterpolationType(k))});
 var result={status:'read_from_real_saved_aep',project:app.project.file.fsName,native_camera_keys:keys};
 var f=new File(paths[ci]+'/camera-keys.json');f.encoding='UTF-8';f.open('w');f.write(encode(result));f.close();reports.push(result);
}
var f=new File("E:/\u81ea\u5a92\u4f53/video-skills-lab/evaluations/course-p13-probe-001/native-camera-key-audit.json");f.encoding='UTF-8';f.open('w');f.write(encode({status:'completed',cases:reports}));f.close();
}());