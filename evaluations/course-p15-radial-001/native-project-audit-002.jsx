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

var paths=["E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-011/p15-radial-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-011/p15-radial-slow-002/project.aep"],out="E:/\u81ea\u5a92\u4f53/video-skills-lab/evaluations/course-p15-radial-001/native-project-audit-002.json",report={status:'failed'};
try{if(app.project.dirty)throw Error('Preserve dirty work');if(app.project.numItems&&(!app.project.file||app.project.file.fsName.indexOf('video-skills-lab')<0))throw Error('Preserve unrelated work');var rows=[];
for(var ix=0;ix<paths.length;ix++){app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(paths[ix]));var c;for(var k=1;k<=app.project.numItems;k++)if(app.project.item(k).name==='P15_RADIAL')c=app.project.item(k);if(c.comment!=='video-skills-lab:course-reproduction')throw Error('Unowned composition');var media=[];for(var k=1;k<=app.project.numItems;k++){var item=app.project.item(k);if(item instanceof FootageItem&&item.file)media.push({path:item.file.fsName,missing:item.footageMissing});}
var n=Math.round(c.duration*c.frameRate),parent=new File(paths[ix]).parent;
function still(frame){var target=new File(parent.fsName+'/native-still-'+frame+'.png');if(!target.exists)c.saveFrameToPng(frame/c.frameRate,target);var deadline=new Date().getTime()+10000;while(!(new File(target.fsName)).exists&&new Date().getTime()<deadline)$.sleep(100);if(!(new File(target.fsName)).exists)throw Error('PNG missing '+frame);}
still(24);still(Math.floor(n/2));still(n-1);var chain=[];for(var k=1;k<=c.layer(1).effect.numProperties;k++)chain.push(c.layer(1).effect(k).matchName);
rows.push({project:paths[ix],media:media,frames:n,effect_chain:chain,curve_channel:c.layer(1).effect('ADBE CurvesCustom').property('ADBE CurvesCustom-0002').value,dirty_after_export:app.project.dirty});}
report={status:'completed',projects:rows};}catch(e){report={status:'failed',error:e.toString(),line:e.line};}
var f=new File(out);f.encoding='UTF-8';f.open('w');f.write(encode(report));f.close();})();