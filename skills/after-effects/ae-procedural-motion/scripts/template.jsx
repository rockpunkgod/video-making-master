(function () {
    var cfg=__CONFIG__, out=__OUTPUT__;
    // ExtendScript installations do not consistently provide the global JSON object.
    function encode(value) {
        if(value===null)return 'null';
        if(typeof value==='string')return '"'+value.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';
        if(typeof value==='number'||typeof value==='boolean')return String(value);
        var entries=[],key;
        if(value instanceof Array){for(var z=0;z<value.length;z++)entries.push(encode(value[z]));return '['+entries.join(',')+']';}
        for(key in value)if(value.hasOwnProperty(key)&&typeof value[key]!=='undefined')entries.push(encode(key)+':'+encode(value[key]));
        return '{'+entries.join(',')+'}';
    }
    function write(name,text) {var f=new File(out+'/'+name);f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write '+name);f.write(text);f.close();}
    function slider(layer,name,value) {var e=layer.property('ADBE Effect Parade').addProperty('ADBE Slider Control');e.name=name;e.property(1).setValue(value);}
    function animate(p,times,values) {
        for(var i=0;i<times.length;i++) p.setValueAtTime(times[i],values[i]);
        for(var k=1;k<=p.numKeys;k++) {
            p.setInterpolationTypeAtKey(k,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
            p.setTemporalEaseAtKey(k,[new KeyframeEase(0,66)],[new KeyframeEase(0,66)]);
        }
    }
    function inspect(group,errors) {
        for(var j=1;j<=group.numProperties;j++) {
            var p=group.property(j);
            if(p.propertyType===PropertyType.PROPERTY) {
                if(p.canSetExpression && p.expressionEnabled) {
                    for(var f=0;f<Math.round(cfg.duration*cfg.fps);f++) p.valueAtTime(f/cfg.fps,false);
                    if(p.expressionError) errors.push(group.name+'/'+p.name+': '+p.expressionError);
                }
            } else inspect(p,errors);
        }
    }
    try {
        // Never close or replace a user's unsaved project.
        if(app.project && app.project.numItems>0) {
            var labOwned=true,hasComp=false;
            for(var own=1;own<=app.project.numItems;own++)if(app.project.item(own) instanceof CompItem){hasComp=true;if(app.project.item(own).comment!=='video-skills-lab:ae-procedural-motion')labOwned=false;}
            if(hasComp&&labOwned&&!app.project.dirty)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
            else throw Error('Open a fresh empty AE project before executing');
        }
        if(!app.project) app.newProject();
        app.project.rootFolder.comment='video-skills-lab:ae-procedural-motion';
        var comp=app.project.items.addComp(cfg.name,cfg.width,cfg.height,1,cfg.duration,cfg.fps);
        comp.comment='video-skills-lab:ae-procedural-motion';
        comp.bgColor=[0,0,0];
        var ctrl=comp.layers.addNull();ctrl.name='LAB_CONTROLS';ctrl.threeDLayer=true;
        ctrl.property('ADBE Transform Group').property('ADBE Position').setValue([cfg.width/2,cfg.height/2,0]);
        slider(ctrl,'Delay Frames',cfg.delay_frames);slider(ctrl,'Z Spacing',cfg.z_spacing);
        slider(ctrl,'Master Rotation',0);slider(ctrl,'Reveal',0);
        var times=[0,cfg.duration*0.25,cfg.duration*0.55,cfg.duration];
        animate(ctrl.property('ADBE Effect Parade').property('Master Rotation').property(1),times,[0,cfg.rotation_degrees*0.25,-cfg.rotation_degrees*0.15,cfg.rotation_degrees]);
        animate(ctrl.property('ADBE Effect Parade').property('Reveal').property(1),[0,Math.min(0.8,cfg.duration/3)],[0,100]);
        var assetItem=null,assetComp=null;
        if(cfg.asset) {
            assetItem=app.project.importFile(new ImportOptions(new File(cfg.asset)));
            assetComp=app.project.items.addComp('LAB_ASSET',cfg.width,cfg.height,1,cfg.duration,cfg.fps);
            assetComp.comment='video-skills-lab:ae-procedural-motion';
            var source=assetComp.layers.add(assetItem);
            source.property('ADBE Transform Group').property('ADBE Position').setValue([cfg.width/2,cfg.height/2]);
            var fit=Math.min(cfg.size/assetItem.width,cfg.size/assetItem.height)*100;
            source.property('ADBE Transform Group').property('ADBE Scale').setValue([fit,fit]);
        }
        for(var n=cfg.count-1;n>=0;n--) {
            var layer;
            if(assetComp) layer=comp.layers.add(assetComp);
            else {
                layer=comp.layers.addShape();
                var contents=layer.property('ADBE Root Vectors Group');
                var path=contents.addProperty('ADBE Vector Shape - Group');
                // ExtendScript chains conditional operators differently from modern JS.
                var s=new Shape(),points=[],sides=6;
                if(cfg.shape==='square')sides=4;
                else if(cfg.shape==='triangle')sides=3;
                if(sides===4) points=[[-cfg.size/2,-cfg.size/2],[cfg.size/2,-cfg.size/2],[cfg.size/2,cfg.size/2],[-cfg.size/2,cfg.size/2]];
                else for(var v=0;v<sides;v++) {var a=-Math.PI/2+v*2*Math.PI/sides;points.push([Math.cos(a)*cfg.size/2,Math.sin(a)*cfg.size/2]);}
                s.vertices=points;s.closed=true;var tangents=[];for(var v2=0;v2<sides;v2++) tangents.push([0,0]);s.inTangents=tangents;s.outTangents=tangents;
                path.property('ADBE Vector Shape').setValue(s);
                var stroke=contents.addProperty('ADBE Vector Graphic - Stroke');
                stroke.property('ADBE Vector Stroke Color').setValue(cfg.color);
                stroke.property('ADBE Vector Stroke Width').setValue(cfg.stroke_width);
                var trim=contents.addProperty('ADBE Vector Filter - Trim');
                trim.property('ADBE Vector Trim End').expression='var c=thisComp.layer("LAB_CONTROLS");var n=effect("Order")(1);c.effect("Reveal")(1).valueAtTime(time-framesToTime(c.effect("Delay Frames")(1))*n);';
            }
            layer.name='LAB_ELEMENT_'+n;layer.threeDLayer=true;slider(layer,'Order',n);
            var tr=layer.property('ADBE Transform Group');
            tr.property('ADBE Position').expression='var c=thisComp.layer("LAB_CONTROLS");var n=effect("Order")(1);[thisComp.width/2,thisComp.height/2,n*c.effect("Z Spacing")(1)];';
            tr.property('ADBE Rotate Z').expression='var c=thisComp.layer("LAB_CONTROLS");var n=effect("Order")(1);c.effect("Master Rotation")(1).valueAtTime(time-framesToTime(c.effect("Delay Frames")(1))*n);';
            tr.property('ADBE Opacity').expression='var c=thisComp.layer("LAB_CONTROLS");var n=effect("Order")(1);c.effect("Reveal")(1).valueAtTime(time-framesToTime(c.effect("Delay Frames")(1))*n);';
        }
        var camera=comp.layers.addCamera('LAB_CAMERA',[cfg.width/2,cfg.height/2]);
        camera.property('ADBE Transform Group').property('ADBE Position').setValue([cfg.width/2,cfg.height/2,-cfg.camera_zoom]);
        camera.property('ADBE Transform Group').property('ADBE Anchor Point').setValue([cfg.width/2,cfg.height/2,0]);
        camera.property('ADBE Camera Options Group').property('ADBE Camera Zoom').setValue(cfg.camera_zoom);
        var errors=[];for(var l=1;l<=comp.numLayers;l++)inspect(comp.layer(l),errors);
        if(errors.length) throw Error(errors.join('\n'));
        var rq=app.project.renderQueue.items.add(comp);
        var om=rq.outputModule(1);var templates=om.templates,selected='',format='';
        for(var t=0;t<templates.length;t++) if(/PNG/.test(templates[t])&&!/alpha|Alpha/.test(templates[t])){selected=templates[t];break;}
        if(selected){format='png';new Folder(out+'/render').create();om.applyTemplate(selected);om.file=new File(out+'/render/frame_[#####].png');}
        else {
            for(var t2=0;t2<templates.length;t2++)if(/H\.264/.test(templates[t2])&&/15 Mbps/.test(templates[t2])){selected=templates[t2];break;}
            if(selected){format='mp4';om.applyTemplate(selected);om.file=new File(out+'/native.mp4');}
        }
        app.project.save(new File(out+'/project.aep'));
        var compID=comp.id;
        // Reopen the native project so save success alone cannot satisfy editability.
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
        var reopened=app.project.itemByID(compID); // IDs may change: fall back to name.
        if(!reopened)for(var q=1;q<=app.project.numItems;q++)if(app.project.item(q).name===cfg.name)reopened=app.project.item(q);
        if(!reopened)throw Error('Saved composition missing after reopen');
        var errors2=[];for(var l2=1;l2<=reopened.numLayers;l2++)inspect(reopened.layer(l2),errors2);
        var expectedSides=6;if(cfg.shape==='square')expectedSides=4;else if(cfg.shape==='triangle')expectedSides=3;
        var observedSides=[],maxRotationError=0,maxZError=0;
        var reopenedCtrl=reopened.layer('LAB_CONTROLS');
        for(var element=0;element<cfg.count;element++){
            var el=reopened.layer('LAB_ELEMENT_'+element);
            if(!cfg.asset){var vertices=el.property('ADBE Root Vectors Group').property(1).property('ADBE Vector Shape').value.vertices.length;observedSides.push(vertices);if(vertices!==expectedSides)errors2.push('Wrong polygon vertex count for '+el.name);}
            for(var sample=0;sample<Math.round(cfg.duration*cfg.fps);sample++){
                var sampleTime=sample/cfg.fps;
                var expectedRotation=reopenedCtrl.property('ADBE Effect Parade').property('Master Rotation').property(1).valueAtTime(sampleTime-element*cfg.delay_frames/cfg.fps,false);
                var actualRotation=el.property('ADBE Transform Group').property('ADBE Rotate Z').valueAtTime(sampleTime,false);
                maxRotationError=Math.max(maxRotationError,Math.abs(expectedRotation-actualRotation));
                var position=el.property('ADBE Transform Group').property('ADBE Position').valueAtTime(sampleTime,false);
                maxZError=Math.max(maxZError,Math.abs(position[2]-element*cfg.z_spacing));
            }
        }
        if(maxRotationError>0.001||maxZError>0.001)errors2.push('Parameter mapping failed');
        write('receipt.json',encode({status:errors2.length?'failed':'built',app_version:app.version,comp:cfg.name,layers:reopened.numLayers,expression_errors:errors2,output_templates:templates,selected_template:selected,output_format:format,project_reopened:true,shape_vertices:observedSides,max_rotation_error:maxRotationError,max_z_error:maxZError,rendered:false}));
    } catch(e) {write('receipt.json',encode({status:'failed',error:e.toString(),line:e.line,rendered:false}));}
}());
