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

(function(){var out='E:/自媒体/video-skills-lab/evaluations/course-p07-probe-001';function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}try{if(app.project&&app.project.numItems>0){var own=true;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;if(!own||app.project.dirty)throw Error('Preserve existing project');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}if(!app.project)app.newProject();app.project.bitsPerChannel=16;var c=app.project.items.addComp('COURSE_P07_EFFECT_PROBE',1080,1080,1,7,30);c.comment='video-skills-lab:course-reproduction';var l=c.layers.addSolid([1,1,1],'ORIGINAL_NOISE_SOLID',1080,1080,1,7),fx=l.property('ADBE Effect Parade').addProperty('ADBE Fractal Noise'),rows=[];function inspect(group,path){for(var i=1;i<=group.numProperties;i++){var p=group.property(i),row={index:i,path:path+'/'+i,name:p.name,match_name:p.matchName,type:String(p.propertyType)};if(p.propertyType===PropertyType.PROPERTY){try{row.value=p.value;}catch(e){row.value_error=e.toString();}try{if(p.hasMin)row.minimum=p.minValue;if(p.hasMax)row.maximum=p.maxValue;}catch(e){}rows.push(row);}else{rows.push(row);inspect(p,row.path);}}}inspect(fx,'effect');app.project.save(new File(out+'/probe-project.aep'));write({status:'probed',effect_name:fx.name,effect_match_name:fx.matchName,properties:rows,scope:'Native property inspection only; no effect reproduction or enum-label mapping verified'});}catch(e){write({status:'failed',error:e.toString(),line:e.line});}}());
