// Character-wise escaping avoids this Premiere host's replacement-string backslash behavior.
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

(function(){var out='E:/自媒体/video-skills-lab/evaluations/course-p06-final-001/inspect-final';function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}try{if(app.project&&app.project.numItems>0){var own=true;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;if(!own||app.project.dirty)throw Error('Preserve existing project');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}app.open(new File('E:/自媒体/video-skills-lab/samples/course-reproduction-002/p06-final-003/project.aep'));var c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name==='COURSE_P06_TRIM_FINAL')c=app.project.item(i);if(!c)throw Error('Missing exact course comp');c.openInViewer();write({status:'probed',project:app.project.file.fsName,renderer:c.renderer,available_renderers:c.renderers,working_space:app.project.workingSpace,bits_per_channel:app.project.bitsPerChannel});}catch(e){write({status:'failed',error:e.toString()});}}());
