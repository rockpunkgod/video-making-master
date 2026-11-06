(function(){
if(app.project&&app.project.numItems>0)throw Error('Expected empty project');
app.open(new File('E:/自媒体/video-skills-lab/samples/runs/square-005/project.aep'));
var f=new File('E:/自媒体/video-skills-lab/reports/square-audit.txt');f.encoding='UTF-8';f.open('w');
for(var i=1;i<=app.project.numItems;i++){var c=app.project.item(i);if(c instanceof CompItem){f.writeln(c.name);for(var n=1;n<=c.numLayers;n++){var l=c.layer(n);f.writeln(l.name);if(l.matchName==='ADBE Vector Layer'){var path=l.property('ADBE Root Vectors Group').property(1).property('ADBE Vector Shape').value;f.writeln('closed='+path.closed+' vertices='+path.vertices.toString());f.writeln('trim='+l.property('ADBE Root Vectors Group').property('ADBE Vector Filter - Trim').property('ADBE Vector Trim End').valueAtTime(3,false));}}}}
f.close();
}());
