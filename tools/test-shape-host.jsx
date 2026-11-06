(function(){var f=new File('E:/自媒体/video-skills-lab/reports/shape-host-test.txt');f.encoding='UTF-8';f.open('w');
var cfg={shape:'square',size:840};var s=new Shape(),points=[],sides=cfg.shape==='square'?4:cfg.shape==='triangle'?3:6;
f.writeln('shape='+cfg.shape+' sides='+sides);
if(sides===4)points=[[-cfg.size/2,-cfg.size/2],[cfg.size/2,-cfg.size/2],[cfg.size/2,cfg.size/2],[-cfg.size/2,cfg.size/2]];
else for(var v=0;v<sides;v++){var a=-Math.PI/2+v*2*Math.PI/sides;points.push([Math.cos(a)*cfg.size/2,Math.sin(a)*cfg.size/2]);}
s.vertices=points;s.closed=true;var tangents=[];for(var v2=0;v2<sides;v2++)tangents.push([0,0]);s.inTangents=tangents;s.outTangents=tangents;
f.writeln('points='+points.toString());f.writeln('vertices='+s.vertices.toString());f.close();}());
