(function(){
var f=new File('E:/自媒体/video-skills-lab/reports/current-properties.txt'); f.encoding='UTF-8';f.open('w');
function dump(p,depth){f.writeln(new Array(depth+1).join(' ')+p.name+' | '+p.matchName);if(depth<3)for(var i=1;i<=p.numProperties;i++)dump(p.property(i),depth+1);}
f.writeln('version='+app.version);f.writeln('items='+app.project.numItems);
for(var i=1;i<=app.project.numItems;i++){var item=app.project.item(i);f.writeln('ITEM '+item.name);if(item instanceof CompItem)for(var j=1;j<=item.numLayers;j++){var l=item.layer(j);if(l.name==='LAB_CAMERA')dump(l,0);}}
f.close();
}());
