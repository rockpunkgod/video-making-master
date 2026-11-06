(function(){
var root='E:/自媒体/video-skills-lab/reports';
function write(name,value){var f=new File(root+'/'+name);f.encoding='UTF-8';f.open('w');f.write(value);f.close();}
try{
 var target='premierepro-26.0';
 var running=BridgeTalk.isRunning(target);write('premiere-message-state.txt','running='+running+';status='+BridgeTalk.getStatus(target));
 if(!running)throw Error('Target is not running; no message sent');
 var bt=new BridgeTalk();bt.target=target;
 bt.body="(function(){var expected=new File('E:/自媒体/video-skills-lab/samples/pr-sound-001/project.prproj');if(!app.project||new File(app.project.path).fsName!==expected.fsName)return 'different_project_no_action';return 'lab_project_confirmed|version='+app.version;}());";
 bt.onResult=function(m){write('premiere-message-result.txt',m.body);};
 bt.onError=function(m){write('premiere-message-error.txt',m.body);};
 bt.onTimeout=function(m){write('premiere-message-timeout.txt','Target timed out');};bt.timeout=15;
 var sent=bt.send(15);write('premiere-message-dispatch.txt','sent='+sent+'; receipt required');
}catch(e){write('premiere-message-error.txt',e.toString());}
}());
