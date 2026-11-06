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

(function(){var dirs=["E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-014/p15-assembly-003", "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-014/p15-assembly-variation-001"];if(app.project&&app.project.numItems){if(app.project.dirty)throw Error('Dirty work');var owned=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){owned=true;if(app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Unowned');}if(!owned)throw Error('Unowned');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}for(var n=0;n<dirs.length;n++){var out=dirs[n];app.open(new File(out+'/project.aep'));var c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='COURSE_P15_ASSEMBLY')c=app.project.item(i);if(!c)throw Error('Missing assembly');var g=c.layer('ROLE_BACKGROUND').effect('ADBE 4ColorGradient'),media=[];for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);if(item instanceof FootageItem&&item.file)media.push({path:item.file.fsName,exists:item.file.exists,missing:item.footageMissing});}var v={status:'passed',project_reopened:true,project:app.project.file.fsName,blend:g.property('ADBE 4ColorGradient-0009').value,point2:g.property('ADBE 4ColorGradient-0003').value,media:media,effect_chain:[c.layer('ROLE_BACKGROUND').effect(1).matchName,c.layer('ROLE_BACKGROUND').effect(2).matchName]};var f=new File(out+'/native-bg-audit.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}var f=new File("E:/\u81ea\u5a92\u4f53/video-skills-lab/cache/p15-bg-config-001/audit-complete.txt");f.open('w');f.write('completed');f.close();})();