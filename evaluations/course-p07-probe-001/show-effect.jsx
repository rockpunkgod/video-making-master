(function(){
 if(app.project && app.project.numItems>0)throw Error('Preserve current work; this inspection expects the observed empty project');
 app.open(new File('E:/自媒体/video-skills-lab/evaluations/course-p07-probe-001/probe-project.aep'));
 var c=app.project.item(1);c.openInViewer();var l=c.layer(1);l.selected=true;l.property('ADBE Effect Parade').property('ADBE Fractal Noise').selected=true;
 var menu=app.findMenuCommandId('效果控件');if(menu>0)app.executeCommand(menu);
}());
