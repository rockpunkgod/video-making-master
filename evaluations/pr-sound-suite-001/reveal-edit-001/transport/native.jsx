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

var out="E:/自媒体/video-skills-lab/evaluations/pr-sound-suite-001/reveal-edit-001/transport",expected=new File("E:/自媒体/video-skills-lab/evaluations/pr-sound-suite-001/variation-edit-001/edited-project.prproj");
function write(n,v){var f=new File(out+'/'+n);f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write native receipt: '+f.error);f.write(encode(v));f.close();}
try{
if(!app.project||new File(app.project.path).fsName!==expected.fsName)throw Error('Different active Premiere project; no payload executed');
var journal=new File(out+'/native-phase.json');if(journal.exists)throw Error('Refusing replay');
write('native-phase.json',{status:'claimed',project:expected.fsName});
var payloadFile=new File("E:/自媒体/video-skills-lab/evaluations/pr-sound-suite-001/reveal-edit-001/audit.jsx");payloadFile.encoding='UTF-8';
if(!payloadFile.open('r'))throw Error('Cannot read reviewed payload: '+payloadFile.error);
var payloadText=payloadFile.read();payloadFile.close();var result=eval(payloadText);
write('native-result.json',{status:'executed',result:result});
write('native-phase.json',{status:'finished'});return 'lab_payload_finished';
}catch(e){var failure={status:'failed',error:e.toString(),line:e.line};try{write('native-result.json',failure);}catch(io){failure.receipt_error=io.toString();}return encode(failure);}
}());