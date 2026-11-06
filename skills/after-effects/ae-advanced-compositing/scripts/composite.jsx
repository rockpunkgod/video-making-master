(function () {
__ENCODER__
var cfg=__CONFIG__,out=__OUTPUT__,errors=[],stage='ownership';
function write(value){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(value));f.close();}
function find(name){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===name&&app.project.item(i) instanceof CompItem)return app.project.item(i);throw Error('Missing comp '+name);}
function control(comp,name){return comp.layer('controls').effect(name)(1);}
function importRole(role){
    var spec=cfg.inputs[role];
    var folder=app.project.importFile(new ImportOptions(new File(spec.project))),comp=null;
    if(!(folder instanceof FolderItem))throw Error('Native project import differs');
    folder.name='SOURCE_'+role;
    function visit(group){for(var i=1;i<=group.numItems;i++){
        var item=group.item(i);if(item instanceof FolderItem){visit(item);continue;}
        if(item instanceof CompItem&&item.name===spec.composition)comp=item;
        if(item instanceof FootageItem&&item.file){
            var matched=false;
            for(var j=0;j<spec.asset_relinks.length;j++)if(item.file.name===spec.asset_relinks[j].original_name){item.replace(new File(spec.asset_relinks[j].path));matched=true;break;}
            if(!matched)throw Error('Unpackaged external footage in '+role+': '+item.file.name);
        }
    }}visit(folder);
    if(!comp)throw Error('Input composition not found for '+role);comp.name='P13_'+role.toUpperCase();
    comp.bgColor=[0,0,0];return comp;
}
function noCamera(comp){for(var i=1;i<=comp.numLayers;i++)if(comp.layer(i) instanceof CameraLayer)comp.layer(i).enabled=false;}
function slider(layer,name,v){var fx=layer.effect.addProperty('ADBE Slider Control');fx.name=name;fx.property(1).setValue(v);}
function point(layer,name,v){var fx=layer.effect.addProperty('ADBE Point3D Control');fx.name=name;fx.property(1).setValue(v);}
function layerRole(comp,role){return comp.layer('ROLE_'+role.toUpperCase());}
try {
    if(app.project&&app.project.numItems){
        var owned=true,hasComp=false;
        for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')owned=false;}
        if(!owned||!hasComp||app.project.dirty)throw Error('Preserve existing work');
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    }
    if(!app.project)app.newProject();app.project.bitsPerChannel=16;
    stage='import editable projects';var components={};
    var roles=['core','lines','noise','contours','dots'];
    for(var i=0;i<roles.length;i++)components[roles[i]]=importRole(roles[i]);
    stage='noise changes';var noise=components.noise;noCamera(noise);
    for(var i=noise.numLayers;i>=1;i--){var l=noise.layer(i);if(l.effect&&l.effect('ADBE Fractal Noise')&&!/^FN(?: [2-7])?$/.test(l.name))l.remove();}
    control(noise,'Position Z spacing').setValue(cfg.noise.z_spacing);
    var noiseCount=0;
    for(var i=1;i<=noise.numLayers;i++){
        var l=noise.layer(i);if(!l.effect)continue;var fx=l.effect('ADBE Fractal Noise');if(!fx)continue;
        noiseCount++;fx.property('ADBE Fractal Noise-0009').setValue(0);
        fx.property('ADBE Fractal Noise-0011').setValue(cfg.noise.width);fx.property('ADBE Fractal Noise-0012').setValue(cfg.noise.height);
        if(fx.property('ADBE Fractal Noise-0004').value!==2000)errors.push('Inherited noise contrast differs');
    }
    if(noiseCount!==cfg.noise.count)throw Error('Noise layer count differs');
    stage='contour changes';noCamera(components.contours);control(components.contours,'Position Z spacing').setValue(cfg.contour_z_spacing);
    stage='nested dots';var inner=components.dots;inner.duration=151/30;var innerCtrl=inner.layer('controls');
    for(var i=1;i<=inner.numLayers;i++){var l=inner.layer(i);l.outPoint=151/30;if(l!==innerCtrl)l.parent=innerCtrl;}
    innerCtrl.transform.scale.setValue([cfg.dots.inner_scale,cfg.dots.inner_scale]);
    var scatter=app.project.items.addComp('P13_DOT_SCATTER',1280,720,1,151/30,30);scatter.comment='video-skills-lab:course-reproduction';scatter.bgColor=[0,0,0];
    var ctrl=scatter.layers.addNull();ctrl.name='controls';slider(ctrl,'seed',cfg.dots.seed);slider(ctrl,'driftSpeed',cfg.dots.drift_speed);point(ctrl,'Position Min',cfg.dots.pos_min);point(ctrl,'Position Max',cfg.dots.pos_max);
    var posExpression='seed=thisComp.layer("controls").effect("seed")(1);\nseedRandom(seed,1);\nposMin=thisComp.layer("controls").effect("Position Min")(1);\nposMax=thisComp.layer("controls").effect("Position Max")(1);\npos=random(posMin,posMax);\ndrift=time*random(thisComp.layer("controls").effect("driftSpeed")(1));\npos+drift+value;';
    for(var i=1;i<=cfg.dots.count;i++){
        var l=scatter.layers.add(inner);l.name='DOT_CLUSTER_'+i;l.moveToEnd();l.threeDLayer=true;
        l.transform.position.setValue([0,0,0]);l.transform.position.expression=posExpression;
        l.timeRemapEnabled=true;l.property('ADBE Time Remapping').expression='seedRandom(5,true);\ntime-random()';
    }
    components.dots=scatter;
    stage='main scene';var main=app.project.items.addComp(cfg.name,1920,1080,1,20,24);main.comment='video-skills-lab:course-reproduction';main.bgColor=[0,0,0];
    for(var i=0;i<roles.length;i++){
        var role=roles[i],spec=cfg.layers[role],source=components[role],l=main.layers.add(source);
        l.name='ROLE_'+role.toUpperCase();l.threeDLayer=true;l.collapseTransformation=spec.collapse;
        l.transform.position.setValue([960,540,spec.z]);
        if(spec.orientation)l.transform.orientation.setValue(spec.orientation);
        l.startTime=spec.start_frame/24*cfg.camera_time_scale;l.inPoint=l.startTime;l.outPoint=Math.min(20,l.startTime+source.duration);
        if(role==='noise'){
            var key=l.effect.addProperty('ADBE Linear Color Key2');key.property('ADBE Linear Color Key2-0003').setValue([1,1,1,1]);
            key.property('ADBE Linear Color Key2-0005').setValue(0);key.property('ADBE Linear Color Key2-0006').setValue(10);
        }
    }
    var camera=main.layers.addCamera('Camera 1',[960,540]);camera.autoOrient=AutoOrientType.NO_AUTO_ORIENT;
    camera.property('ADBE Camera Options Group').property('ADBE Camera Zoom').setValue(cfg.camera_zoom);
    camera.property('ADBE Camera Options Group').property('ADBE Camera Depth of Field').setValue(0);
    var cp=camera.transform.position;
    for(var i=0;i<cfg.camera_frames.length;i++)cp.setValueAtTime(cfg.camera_frames[i]/24*cfg.camera_time_scale,[960,540,cfg.camera_z[i]]);
    for(var k=1;k<=cp.numKeys;k++){cp.setTemporalAutoBezierAtKey(k,false);cp.setInterpolationTypeAtKey(k,KeyframeInterpolationType.LINEAR,KeyframeInterpolationType.LINEAR);cp.setSpatialAutoBezierAtKey(k,false);cp.setSpatialTangentsAtKey(k,[0,0,0],[0,0,0]);}
    while(app.project.renderQueue.numItems)app.project.renderQueue.item(1).remove();
    var rq=app.project.renderQueue.items.add(main),om=rq.outputModule(1),templates=om.templates,selected='';
    for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}
    if(!selected)throw Error('Tested H264 output template missing');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
    stage='save reopen';app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
    stage='native validation';var samples=[],previous=0,maxXYError=0,maxPositiveStep=0,cameraKeys=[];
    var savedCameraPosition=main.layer('Camera 1').transform.position;
    for(var k=1;k<=savedCameraPosition.numKeys;k++)cameraKeys.push({time:savedCameraPosition.keyTime(k),value:savedCameraPosition.keyValue(k),in_type:String(savedCameraPosition.keyInInterpolationType(k)),out_type:String(savedCameraPosition.keyOutInterpolationType(k))});
    for(var f=0;f<480;f++){
        var v=main.layer('Camera 1').transform.position.valueAtTime(f/24,false);maxXYError=Math.max(maxXYError,Math.abs(v[0]-960),Math.abs(v[1]-540));
        if(f)maxPositiveStep=Math.max(maxPositiveStep,v[2]-previous);previous=v[2];samples.push({frame:f,z:v[2]});
    }
    if(maxXYError>1e-6||maxPositiveStep>1e-6)errors.push('Camera direction/centering failure');
    var roleRecords=[];
    for(var i=0;i<roles.length;i++){
        var role=roles[i],l=layerRole(main,role),spec=cfg.layers[role];
        if(!l.threeDLayer||l.collapseTransformation!==spec.collapse||Math.abs(l.transform.position.value[2]-spec.z)>1e-6)errors.push('Role structure failure '+role);
        roleRecords.push({role:role,source:l.source.name,collapse:l.collapseTransformation,threeD:l.threeDLayer,position:l.transform.position.value,inPoint:l.inPoint,outPoint:l.outPoint,orientation:l.transform.orientation.value});
    }
    var scatter=find('P13_DOT_SCATTER'),offsets=[],maxTimeDrift=0,startReadbacks=[];
    var boundaryProp=scatter.layer(2).property('ADBE Time Remapping'),savedExpression=boundaryProp.expression;
    boundaryProp.expression='-0.5';var negativeProbe=boundaryProp.valueAtTime(0,false);
    boundaryProp.expression='0.5';var positiveProbe=boundaryProp.valueAtTime(0,false);boundaryProp.expression=savedExpression;
    if(negativeProbe!==0||Math.abs(positiveProbe-.5)>1e-6)errors.push('Native remap boundary behavior differs');
    for(var i=2;i<=scatter.numLayers;i++){
        var l=scatter.layer(i),tr=l.property('ADBE Time Remapping'),offset=tr.valueAtTime(1,false)-1;offsets.push(offset);startReadbacks.push(tr.valueAtTime(0,false));
        for(var f=0;f<151;f++)maxTimeDrift=Math.max(maxTimeDrift,Math.abs(tr.valueAtTime(f/30,false)-Math.max(0,f/30+offset)));
        if(tr.expressionError||l.transform.position.expressionError||offset>0||offset<-1)errors.push('Dot timing expression failure');
    }
    var distinct={};for(var i=0;i<offsets.length;i++)distinct[String(offsets[i])]=true;var count=0;for(var n in distinct)if(distinct.hasOwnProperty(n))count++;
    if(count!==cfg.dots.count||maxTimeDrift>1e-6)errors.push('Dot offsets not independent/stable');
    var expressionCount=0,missing=[];
    function inspect(p){if(p.propertyType===PropertyType.PROPERTY){if(p.canSetExpression&&p.expressionEnabled){expressionCount++;p.valueAtTime(1,false);if(p.expressionError)errors.push(p.expressionError);}}else for(var j=1;j<=p.numProperties;j++)inspect(p.property(j));}
    for(var i=1;i<=app.project.numItems;i++){
        var item=app.project.item(i);if(item instanceof CompItem)for(var j=1;j<=item.numLayers;j++)inspect(item.layer(j));
        else if(item instanceof FootageItem&&item.footageMissing)missing.push(item.name);
    }
    if(missing.length)errors.push('Missing footage');
    stage='editable camera test';var original=main.layer('Camera 1').transform.position.keyValue(6);
    main.layer('Camera 1').transform.position.setValueAtKey(6,[960,540,original[2]-100]);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
    var changed=main.layer('Camera 1').transform.position.keyValue(6)[2];if(changed!==original[2]-100)errors.push('Camera key edit/reopen failure');
    main.layer('Camera 1').transform.position.setValueAtKey(6,original);app.project.save();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));main=find(cfg.name);
    var restored=main.layer('Camera 1').transform.position.keyValue(6)[2];if(restored!==original[2])errors.push('Camera key restore failure');
    var exports=[],frames=[0,24,36,48,72,96,144,162,192,240,300,479];
    for(var i=0;i<frames.length;i++){var name='native-still-'+frames[i]+'.png';main.saveFrameToPng(frames[i]/24,new File(out+'/'+name));exports.push(name);}
    write({status:errors.length?'failed':'built',project_reopened:true,expression_errors:errors,selected_template:selected,output_format:'mp4',
        native_png_exports:exports,main_layers:main.numLayers,role_records:roleRecords,camera_validated_frames:480,max_camera_xy_error:maxXYError,max_forward_z_step:maxPositiveStep,
        camera_samples:samples,native_camera_keys:cameraKeys,native_camera_edit:{original:original[2],changed:changed,restored:restored},
        dot_offsets:offsets,distinct_dot_offsets:count,max_time_remap_error:maxTimeDrift,time_remap_boundary_probe:{negative_constant:negativeProbe,positive_constant:positiveProbe,start_readbacks:startReadbacks,production_expression_unchanged:true},expressions_checked:expressionCount,
        missing_media:missing,noise_count:noiseCount,course_fidelity_status:'candidate; camera frame indices/layer starts estimated; exact random identities and final count unverified',rendered:false});
}catch(error){
    var retained=null;
    if(stage!=='ownership'&&app.project&&app.project.dirty){try{app.project.save(new File(out+'/failed-project.aep'));retained='failed-project.aep';}catch(saveError){}}
    write({status:'failed',error:error.toString(),line:error.line,stage:stage,retained_failed_project:retained});
}
}());
