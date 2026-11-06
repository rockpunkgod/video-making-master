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

var out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-009/p14-native-probe-004",stage='start';
if(app.project&&app.project.numItems===1&&app.project.item(1).name==='P14_NATIVE_PROBE'&&app.project.dirty){app.project.save(new File(out+'/retained-probe001.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
function write(v){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
function tree(p){try{var o={name:p.name,matchName:p.matchName};if(p.propertyType===PropertyType.PROPERTY){try{var v=p.value;if(v instanceof Array||typeof v==='number'||typeof v==='string'||typeof v==='boolean')o.value=v;else o.hostValue='omitted live host object';}catch(e){o.error=e.toString();}o.valueType=p.propertyValueType;}else{o.children=[];for(var i=1;i<=p.numProperties;i++)o.children.push(tree(p.property(i)));}return o;}catch(e){return {read_error:e.toString()};}}
try{
if(app.project&&app.project.numItems){var own=true,has=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){has=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!has||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
if(!app.project)app.newProject();var c=app.project.items.addComp('P14_NATIVE_PROBE',1280,720,1,151/30,30);c.comment='video-skills-lab:course-reproduction';var l=c.layers.addText('SUBPRIME'),t=l.property('ADBE Text Properties'),a=t.property('ADBE Text Animators');
var pa=a.addProperty('ADBE Text Animator');pa.name='pos';var prop=pa.property('ADBE Text Animator Properties').addProperty('ADBE Text Position 3D');prop.setValue([0,-79,0]);
var selectors=pa.property('ADBE Text Selectors');stage='position selectors';var initial=tree(selectors);while(selectors.numProperties)selectors.property(1).remove();var ex=selectors.addProperty('ADBE Text Expressible Selector');ex.property('ADBE Text Expressible Amount').expression='if(textIndex%2) -100; else 100';
stage='opacity animator';var oa=a.addProperty('ADBE Text Animator');oa.name='opacity';oa.property('ADBE Text Animator Properties').addProperty('ADBE Text Opacity').setValue(0);var rs=oa.property('ADBE Text Selectors').addProperty('ADBE Text Selector');
stage='tree';t=l.property('ADBE Text Properties');var result={status:'built',host:app.version,initial_position_selectors:initial,text_properties:tree(t),project_reopened:false};app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));result.project_reopened=true;write(result);
}catch(e){write({status:'failed',error:e.toString(),line:e.line,stage:stage});}
}());