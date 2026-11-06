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

var paths=["E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-004/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-geometry-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-typography-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-texture-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-baseline-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-algorithm-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-motion2026-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-ai-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-002/p06-final-003/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-002/p06-delay5-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-generalization-001/geometry/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-generalization-001/typography/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-generalization-001/texture/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-003/p07-tint-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-003/p07-seed7-isolated-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-004/p08-disappear-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-004/p08-appear-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-004/p08-geometry-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-004/p08-typography-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-004/p08-texture-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-005/p09-final-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-005/p09-seed165-speed310-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-005/p09-geometry-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-005/p09-typography-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-005/p09-texture-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-006/p10-reference-replay-006/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-006/p10-reference-variation-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-006/p10-reference-standalone-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-007/p11-baseline-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-007/p11-variation-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-007/p11-geometry-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-007/p11-typography-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-007/p11-texture-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-008/p12-baseline-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-008/p12-seed0-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-008/p12-sparse-002/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/composite-001/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-fixture-001/solve-calibrated-001/composite-typography/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-gallery-001/solve-001/composite-pixel-sized/project.aep", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/tracking-corridor-001/solve-calibrated-001/composite-pixel-sized/project.aep"],out="E:/\u81ea\u5a92\u4f53/video-skills-lab/reports/native-media-dependencies.json",rows=[],restore=null;
function write(result){var f=new File(out);f.encoding='UTF-8';f.open('w');f.write(encode(result));f.close();}
function closeOwned(){
 if(!app.project||!app.project.numItems)return;
 if(app.project.dirty)throw Error('Dirty Adobe project preserved');
 for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Unowned Adobe project preserved');
 app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}
try{
 if(app.project&&app.project.file)restore=app.project.file.fsName;
 for(var pi=0;pi<paths.length;pi++){
  closeOwned();app.open(new File(paths[pi]));var media=[];
  for(var j=1;j<=app.project.numItems;j++){var item=app.project.item(j);if(item instanceof FootageItem&&item.file)media.push({name:item.name,path:item.file.fsName,exists:item.file.exists,missing:item.footageMissing});}
  rows.push({project:paths[pi],media:media});write({status:'running',completed:rows.length,total:paths.length,projects:rows});
 }
 closeOwned();if(restore)app.open(new File(restore));write({status:'completed',completed:rows.length,total:paths.length,projects:rows,projects_modified:false,previous_project_restored:restore});
}catch(e){write({status:'failed',error:e.toString(),line:e.line,completed:rows.length,total:paths.length,projects:rows});}
}());