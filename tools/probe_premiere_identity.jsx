(function(){
var bt=new BridgeTalk();bt.target='premierepro-26.0';
bt.body="(function(){var p=app.project;var path=p?String(p.path):'';var lab=path.indexOf('video-skills-lab')>=0;return 'version='+app.version+';project_type='+typeof p+';path_type='+(p?typeof p.path:'none')+';path_length='+path.length+';lab_path='+lab+(lab?';path='+path:'');}());";
bt.onResult=function(m){var f=new File('E:/自媒体/video-skills-lab/reports/premiere-identity.txt');f.encoding='UTF-8';f.open('w');f.write(m.body);f.close();};
bt.onError=function(m){var f=new File('E:/自媒体/video-skills-lab/reports/premiere-identity-error.txt');f.open('w');f.write(m.body);f.close();};
if(BridgeTalk.isRunning(bt.target))bt.send(15);
}());
