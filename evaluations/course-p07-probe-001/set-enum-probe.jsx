(function(){
 if(!app.project.file || app.project.file.fsName.replace(/\\/g,'/')!=='E:/自媒体/video-skills-lab/evaluations/course-p07-probe-001/probe-project.aep')throw Error('Unexpected project');
 var fx=app.project.item(1).layer(1).property('ADBE Effect Parade').property('ADBE Fractal Noise');
 fx.property('ADBE Fractal Noise-0001').setValue(16);fx.property('ADBE Fractal Noise-0002').setValue(1);
 fx.property('ADBE Fractal Noise-0003').setValue(1);fx.property('ADBE Fractal Noise-0004').setValue(2000);fx.property('ADBE Fractal Noise-0015').setValue(1);
 app.project.save(new File('E:/自媒体/video-skills-lab/evaluations/course-p07-probe-001/enum-probe.aep'));
}());
