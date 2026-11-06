(function () {
    var root = new Folder('E:/自媒体/video-skills-lab/reports'); root.create();
    var file = new File(root.fsName + '/ae-runtime.txt');
    file.encoding = 'UTF-8'; file.open('w');
    try {
        file.writeln('app.version=' + app.version);
        file.writeln('app.buildName=' + app.buildName);
        app.newProject();
        var comp = app.project.items.addComp('LAB_PROBE',640,360,1,1,24);
        var text=comp.layers.addText('AE SCRIPT READY');
        text.property('ADBE Transform Group').property('ADBE Position').setValue([320,180]);
        app.project.save(new File('E:/自媒体/video-skills-lab/samples/environment-probe.aep'));
        file.writeln('project_saved=true');
        file.writeln('output_modules='+app.project.renderQueue.items.add(comp).outputModule(1).templates.join('|'));
    } catch(e) {file.writeln('ERROR='+e.toString());}
    file.close();
}());
