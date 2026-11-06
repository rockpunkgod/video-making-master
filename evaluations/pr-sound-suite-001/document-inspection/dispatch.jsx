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

var out="E:/自媒体/video-skills-lab/evaluations/pr-sound-suite-001/document-inspection";
function write(v){var f=new File(out+'/transport.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
try{
 var bt=new BridgeTalk();bt.target="premierepro-26.0";
 if(!BridgeTalk.isRunning(bt.target))throw Error('Premiere target is not running; no automatic launch');
 var source=new File("E:/自媒体/video-skills-lab/evaluations/pr-sound-suite-001/document-inspection/native.jsx");source.encoding='UTF-8';if(!source.open('r'))throw Error('Cannot read reviewed native wrapper');bt.body=source.read();source.close();bt.timeout=30;
 bt.onResult=function(m){write({status:'returned',body:m.body});};
 bt.onError=function(m){write({status:'transport_error',body:m.body});};
 bt.onTimeout=function(m){write({status:'observation_timeout',do_not_replay:true});};
 bt.send(30);
}catch(e){write({status:'not_sent',error:e.toString()});}
}());