(function(){
var root='E:/自媒体/video-skills-lab/samples/tracking-fixture-001';
if(app.project&&app.project.numItems>0)throw Error('Expected empty project after render');
app.open(new File(root+'/source-scene.aep'));
var c=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name==='TRACKING_SOURCE')c=app.project.item(i);
var l=c.layer('back'),corners=[[0,0],[1024,0],[1024,1024],[0,1024]];
for(var i=0;i<4;i++){var e=l.property('ADBE Effect Parade').addProperty('ADBE Point Control');e.name='GROUND_TRUTH_CORNER_'+i;e.property(1).expression='var p=thisLayer.toComp(['+corners[i][0]+','+corners[i][1]+',0]);[p[0],p[1]];';}
var rows=[];for(var f=0;f<96;f++){var quad=[];for(var i=0;i<4;i++){var v=l.property('ADBE Effect Parade').property('GROUND_TRUTH_CORNER_'+i).property(1).valueAtTime(f/24,false);quad.push('['+v[0]+','+v[1]+']');}rows.push('['+quad.join(',')+']');}
var file=new File(root+'/ground-truth-back-plane.json');file.encoding='UTF-8';file.open('w');file.write('{"scope":"evaluation only, generated original scene; never imported in solve","corners":['+rows.join(',')+']}');file.close();
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.newProject();
}());
