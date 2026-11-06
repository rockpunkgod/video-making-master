(function(){
var out='E:/自媒体/video-skills-lab/samples/tracking-fixture-001';
var f=new File(out+'/tracker-properties-initial.txt');f.encoding='UTF-8';f.open('w');
try{
 if(app.project&&app.project.numItems>0)throw Error('Expected empty project');
 if(!app.project)app.newProject();
 var source=app.project.importFile(new ImportOptions(new File(out+'/source.mp4')));
 var comp=app.project.items.addComp('TRACKING_SOLVE',source.width,source.height,1,source.duration,source.frameRate);comp.comment='video-skills-lab:tracking-attempt';
 var layer=comp.layers.add(source);layer.name='ANALYSIS_SOURCE';var fx=layer.property('ADBE Effect Parade').addProperty('ADBE 3D Tracker');
 layer.selected=true;fx.selected=true;comp.openInViewer();
 for(var i=1;i<=fx.numProperties;i++){var p=fx.property(i);f.writeln(i+' | '+p.name+' | '+p.matchName+' | '+p.propertyValueType);try{f.writeln('VALUE '+p.value);}catch(e){f.writeln('custom value not exposed');}}
 app.project.save(new File(out+'/tracking-attempt.aep'));f.writeln('EFFECT_APPLIED_NOT_YET_VERIFIED');
}catch(e){f.writeln('ERROR '+e.toString()+' line '+e.line);}
f.close();
}());
