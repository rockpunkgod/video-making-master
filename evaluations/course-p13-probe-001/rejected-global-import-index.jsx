(function () {
// Character-wise escaping avoids this Premiere host's replacement-string backslash behavior.
function encode(value) {
    if(value===null)return 'null';
    if(typeof value==='string'){
        var out=String.fromCharCode(34);
        for(var i=0;i<value.length;i++){
            var c=value.charCodeAt(i);
            if(c===34||c===92)out+=String.fromCharCode(92,c);
            else if(c<32){var hex=c.toString(16);while(hex.length<4)hex='0'+hex;out+=String.fromCharCode(92)+'u'+hex;}
            else out+=value.charAt(i);
        }
        return out+String.fromCharCode(34);
    }
    if(typeof value==='number'){if(!isFinite(value))throw Error('Non-finite JSON number');return String(value);}
    if(typeof value==='boolean')return String(value);
    var entries=[],key;
    if(value instanceof Array){for(var i=0;i<value.length;i++)entries.push(encode(value[i]));return '['+entries.join(',')+']';}
    for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
    return '{'+entries.join(',')+'}';
}

var cfg={"schema_version": 1, "source": "https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=13", "inputs": {"contours": {"project": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001/inputs/contours/project.aep", "composition": "COURSE_P06_TRIM_FINAL", "sha256": "1096b70a15213deeb87f9b4e2bfda15b7afd1b8312e3c1582c0173910d4710ca", "origin": "samples/course-reproduction-002/p06-final-003/project.aep", "assets": [], "asset_relinks": []}, "noise": {"project": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001/inputs/noise/project.aep", "composition": "COURSE_P07_DIGITAL_BLOCKS", "sha256": "19f2374c9e1127e5a51d30f6dca65865a2fbe799f9a025eb0cb56b9ef49326bb", "origin": "samples/course-reproduction-003/p07-tint-001/project.aep", "assets": [], "asset_relinks": []}, "core": {"project": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001/inputs/core/project.aep", "composition": "COURSE_P11_ALGORITHMIC_LAYOUT", "sha256": "5dbe0b2eca9a2662003d1741b8cd4b2586224f672e39a9effa062c6b7a2ecd1f", "origin": "samples/course-reproduction-007/p11-baseline-001/project.aep", "assets": [], "asset_relinks": []}, "lines": {"project": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001/inputs/lines/project.aep", "composition": "COURSE_P12_CYBER_LINES", "sha256": "e3839ffa90c7e31626ef5f338192606d486e2a6d9ec7d85cfcf53d3761c9dda9", "origin": "samples/course-reproduction-008/p12-baseline-001/project.aep", "assets": [], "asset_relinks": []}, "dots": {"project": "E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001/inputs/dots/project.aep", "composition": "COURSE_P08_THRESHOLD", "sha256": "557f40ed0ac336ff3a17dbd2cdb5f7aefc88c5742adf0efa7294dc9ce26368af", "origin": "samples/course-reproduction-004/p08-appear-001/project.aep", "assets": [], "asset_relinks": []}}, "camera_frames": [23, 47, 81, 91, 144, 161], "camera_z": [-1866.6666666667, -7500, -8500, -12500, -12500, -21000], "camera_zoom": 1866.6666666667, "layers": {"core": {"start_frame": 0, "z": 0, "collapse": false}, "noise": {"start_frame": 32, "z": -5000, "collapse": true, "orientation": [0, 0, 90]}, "contours": {"start_frame": 80, "z": -10000, "collapse": true}, "lines": {"start_frame": 128, "z": -20000, "collapse": false}, "dots": {"start_frame": 0, "z": -3870, "collapse": true}}, "noise": {"count": 7, "width": 500, "height": 20, "z_spacing": 350}, "contour_z_spacing": 300, "dots": {"count": 12, "seed": 653, "drift_speed": -124, "pos_min": [-1084, -630, 1930], "pos_max": [3130, 1950, 8890], "inner_scale": 34}, "provenance": {"observed": ["1920x1080/24fps/20s", "One Node35mm,DOFoff", "noise scale500/20,contrast2000", "noise orientationZ90", "contour zSpacing300", "dot PositionMin/Max and seed653/drift-124", "dot mainZ-3870 final17:35", "timeRemap seedRandom(5,true);time-random()"], "inferred": ["Camera frame indices estimated from04:59 ruler; \u00b11frame uncertainty", "Noise/contour/line starts32/80/128 at24fps from final17:35 timeline", "12 dot copies inferred from six copies duplicated; final count not directly read", "noise mainZ-5000 last fully read; no exact final transform claim", "Core176 count and original random identities inherit earlier candidate limits"]}, "name": "COURSE_P13_COMPOSITE", "width": 1920, "height": 1080, "fps": 24, "duration": 20, "motion_expectation": "required", "camera_time_scale": 1, "status": "candidate", "scope": "Course13 rough spatial assembly, not the fully stylized title sequence", "variant": false},out="E:/\u81ea\u5a92\u4f53/video-skills-lab/samples/course-reproduction-010/p13-baseline-001",errors=[],stage='ownership';
function write(value){var f=new File(out+'/receipt.json');f.encoding='UTF-8';f.open('w');f.write(encode(value));f.close();}
function find(name){for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i).name===name&&app.project.item(i) instanceof CompItem)return app.project.item(i);throw Error('Missing comp '+name);}
function control(comp,name){return comp.layer('controls').effect(name)(1);}
function importRole(role){
    var spec=cfg.inputs[role],previous=app.project.numItems;
    var folder=app.project.importFile(new ImportOptions(new File(spec.project))),comp=null;
    if(!(folder instanceof FolderItem))throw Error('Native project import differs');
    folder.name='SOURCE_'+role;
    for(var i=previous+1;i<=app.project.numItems;i++){
        var item=app.project.item(i);
        if(item instanceof CompItem&&item.name===spec.composition)comp=item;
        if(item instanceof FootageItem&&item.file){
            var matched=false;
            for(var j=0;j<spec.asset_relinks.length;j++)if(item.file.name===spec.asset_relinks[j].original_name){item.replace(new File(spec.asset_relinks[j].path));matched=true;break;}
            if(!matched)throw Error('Unpackaged external footage in '+role+': '+item.file.name);
        }
    }
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
    stage='native validation';var samples=[],previous=0,maxXYError=0,maxPositiveStep=0;
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
    var scatter=find('P13_DOT_SCATTER'),offsets=[],maxTimeDrift=0;
    for(var i=2;i<=scatter.numLayers;i++){
        var l=scatter.layer(i),tr=l.property('ADBE Time Remapping'),offset=tr.valueAtTime(0,false);offsets.push(offset);
        for(var f=0;f<151;f++)maxTimeDrift=Math.max(maxTimeDrift,Math.abs(tr.valueAtTime(f/30,false)-(f/30+offset)));
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
        camera_samples:samples,native_camera_edit:{original:original[2],changed:changed,restored:restored},
        dot_offsets:offsets,distinct_dot_offsets:count,max_time_remap_error:maxTimeDrift,expressions_checked:expressionCount,
        missing_media:missing,noise_count:noiseCount,course_fidelity_status:'candidate; camera frame indices/layer starts estimated; exact random identities and final count unverified',rendered:false});
}catch(error){write({status:'failed',error:error.toString(),line:error.line,stage:stage});}
}());
