(function(){
var f=new File('E:/自媒体/video-skills-lab/reports/adobe-messaging-probe.txt');f.encoding='UTF-8';f.open('w');
try{f.writeln('BridgeTalk_type='+typeof BridgeTalk);if(typeof BridgeTalk!=='undefined'){f.writeln('targets='+BridgeTalk.getTargets(0).join('|'));f.writeln('premiere_running='+BridgeTalk.isRunning('premierepro'));}}
catch(e){f.writeln('ERROR '+e.toString());}f.close();
}());
