(function(){
 function enc(v){if(v instanceof Array){var a=[];for(var i=0;i<v.length;i++)a.push(enc(v[i]));return '['+a.join(',')+']';}if(typeof v==='number')return String(v);if(typeof v==='string')return '"'+v.replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'"';return String(v);}
 function write(text){var f=new File('E:/自媒体/video-skills-lab/evaluations/course-p09-probe-001/receipt.json');f.encoding='UTF-8';f.open('w');f.write(text);f.close();}
 try{
 if(app.project&&app.project.numItems>0)throw Error('Probe requires observed empty project; preserve existing work');
 if(!app.project)app.newProject();var c=app.project.items.addComp('COURSE_P09_PROBE',1920,1080,1,5,30);c.comment='video-skills-lab:course-reproduction';var l=c.layers.addShape();l.threeDLayer=true;
 var p=l.transform.position;p.expression='[10,20,30]+5';var scalar=p.value;
 p.expression='seedRandom(1,1);p=random([-1084,-630,1930],[3130,1950,8890]);d=time*random(-124);p+d+value';p.setValue([0,0,0]);var a=p.valueAtTime(0,false),b=p.valueAtTime(1,false),delta=[];for(var i=0;i<3;i++)delta.push(b[i]-a[i]);
 var fx=l.effect.addProperty('ADBE Point3D Control');var pointMatch=fx.property(1).matchName;fx.property(1).setValue([1,2,3]);
 var group=l.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group'),fill=group.property('ADBE Vectors Group').addProperty('ADBE Vector Graphic - Fill');fill.property('ADBE Vector Fill Color').expression='seedRandom(5,1);random([1,1,1,1])';var rgba=fill.property('ADBE Vector Fill Color').value;
 app.project.save(new File('E:/自媒体/video-skills-lab/evaluations/course-p09-probe-001/probe-project.aep'));
 write('{"status":"probed","scalar_plus_array":'+enc(scalar)+',"position_at_0":'+enc(a)+',"position_at_1":'+enc(b)+',"one_second_delta":'+enc(delta)+',"point3d_parameter_match":'+enc(pointMatch)+',"color_random_array":'+enc(rgba)+'}');
 }catch(e){write('{"status":"failed","line":'+e.line+',"error":'+enc(e.toString())+'}');}
}());
