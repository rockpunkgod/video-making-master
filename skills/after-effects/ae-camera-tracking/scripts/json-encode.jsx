    function encode(value) {
        if(value===null)return 'null';
        if(typeof value==='string')return '"'+value.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';
        if(typeof value==='number'||typeof value==='boolean')return String(value);
        var entries=[],key;
        if(value instanceof Array){for(var z=0;z<value.length;z++)entries.push(encode(value[z]));return '['+entries.join(',')+']';}
        for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
        return '{'+entries.join(',')+'}';
    }
