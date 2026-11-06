"""Execute reviewed Premiere JSX through Adobe BridgeTalk in the running AE host.

No CEP service or replacement application: the native target must already be running.
The exact active project is checked before the payload, and a fresh native journal
prevents accidental replay. A transport ACK alone never counts as production success.
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

def execute(jsx,ae,project,out,timeout=120,target='premierepro-26.0'):
    jsx=Path(jsx).resolve();ae=Path(ae).resolve();project=Path(project).resolve();out=Path(out).resolve()
    if not all(p.is_file() for p in [jsx,ae,project]):raise FileNotFoundError('Reviewed JSX, AE executable and expected native project required')
    out.mkdir(parents=True,exist_ok=False)
    encoder=(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')
    native=r'''(function(){__ENCODER__
var out=__OUT__,expected=new File(__PROJECT__);
function write(n,v){var f=new File(out+'/'+n);f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write native receipt: '+f.error);f.write(encode(v));f.close();}
try{
if(!app.project||new File(app.project.path).fsName!==expected.fsName)throw Error('Different active Premiere project; no payload executed');
var journal=new File(out+'/native-phase.json');if(journal.exists)throw Error('Refusing replay');
write('native-phase.json',{status:'claimed',project:expected.fsName});
var payloadFile=new File(__PAYLOAD_PATH__);payloadFile.encoding='UTF-8';
if(!payloadFile.open('r'))throw Error('Cannot read reviewed payload: '+payloadFile.error);
var payloadText=payloadFile.read();payloadFile.close();var result=eval(payloadText);
write('native-result.json',{status:'executed',result:result});
write('native-phase.json',{status:'finished'});return 'lab_payload_finished';
}catch(e){var failure={status:'failed',error:e.toString(),line:e.line};try{write('native-result.json',failure);}catch(io){failure.receipt_error=io.toString();}return encode(failure);}
}());'''
    native=native.replace('__ENCODER__',encoder).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__PROJECT__',json.dumps(project.as_posix(),ensure_ascii=False)).replace('__PAYLOAD_PATH__',json.dumps(jsx.as_posix(),ensure_ascii=False))
    native_script=out/'native.jsx';native_script.write_text(native,encoding='utf-8')
    host=r'''(function(){__ENCODER__
var out=__OUT__;
function write(v){var f=new File(out+'/transport.json');f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
try{
 var bt=new BridgeTalk();bt.target=__TARGET__;
 if(!BridgeTalk.isRunning(bt.target))throw Error('Premiere target is not running; no automatic launch');
 var source=new File(__NATIVE_PATH__);source.encoding='UTF-8';if(!source.open('r'))throw Error('Cannot read reviewed native wrapper');bt.body=source.read();source.close();bt.timeout=30;
 bt.onResult=function(m){write({status:'returned',body:m.body});};
 bt.onError=function(m){write({status:'transport_error',body:m.body});};
 bt.onTimeout=function(m){write({status:'observation_timeout',do_not_replay:true});};
 bt.send(30);
}catch(e){write({status:'not_sent',error:e.toString()});}
}());'''
    host=host.replace('__ENCODER__',encoder).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__TARGET__',json.dumps(target)).replace('__NATIVE_PATH__',json.dumps(native_script.as_posix(),ensure_ascii=False))
    script=out/'dispatch.jsx';script.write_text(host,encoding='utf-8')
    (out/'request.json').write_text(json.dumps({'reviewed_payload':str(jsx),'expected_project':str(project),'target':target},indent=2),encoding='utf-8')
    subprocess.Popen([str(ae),'-r',str(script)],cwd=ae.parent)
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        result_path=out/'native-result.json'
        if result_path.is_file():
            try:result=json.loads(result_path.read_text(encoding='utf-8-sig'))
            except (ValueError,OSError):time.sleep(.25);continue
            return result
        transport=out/'transport.json'
        if transport.is_file():
            try:status=json.loads(transport.read_text(encoding='utf-8-sig'))
            except (ValueError,OSError):time.sleep(.25);continue
            if status.get('status') in ['not_sent','transport_error']:return status
            if status.get('status')=='returned':
                try:failure=json.loads(status.get('body',''))
                except ValueError:failure={}
                if failure.get('status')=='failed':return failure
        time.sleep(.25)
    report={'status':'observation_timeout','do_not_replay':True,'native_phase_exists':(out/'native-phase.json').exists(),'reason':'Inspect the same live Adobe processes and journal; the target may still be executing'}
    (out/'observation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('jsx');ap.add_argument('--ae',required=True);ap.add_argument('--project',required=True);ap.add_argument('--out',required=True);ap.add_argument('--timeout',type=int,default=120);a=ap.parse_args()
    r=execute(a.jsx,a.ae,a.project,a.out,a.timeout);print(json.dumps(r,ensure_ascii=True,indent=2));raise SystemExit(0 if r.get('status')=='executed' else 2)
