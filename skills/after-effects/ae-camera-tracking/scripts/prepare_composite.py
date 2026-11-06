"""Build a composite from an actual native tracked solid; never import the source scene camera."""
import json
import argparse
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--tracking-dir',type=Path,required=True);ap.add_argument('--name',default='composite-001');ap.add_argument('--asset',type=Path,required=True);ap.add_argument('--scale',type=float,default=100);ap.add_argument('--screen-width',type=float)
a=ap.parse_args();tracking=a.tracking_dir.resolve()
if not a.name.replace('-','').replace('_','').isalnum():raise ValueError('Invalid run name')
if not a.asset.is_file() or not 1<=a.scale<=500:raise ValueError('Invalid overlay asset or scale')
if a.screen_width is not None and not 16<=a.screen_width<=800:raise ValueError('screen-width must be in [16,800] pixels')
out=tracking/a.name
if out.exists():raise FileExistsError('Use a fresh composite output')
(out/'inputs').mkdir(parents=True);shutil.copy2(a.asset,out/'inputs/overlay.png')
encoder=(ROOT/'json-encode.jsx').read_text(encoding='utf-8')
body=r'''
function write(name,value){var f=new File(out+'/'+name);f.encoding='UTF-8';f.open('w');f.write(encode(value));f.close();}
try{
 if(!app.project.file||app.project.file.fsName!==new File(__TRACKING_PROJECT__).fsName)throw Error('Different active tracking project');
 var c=app.project.activeItem;if(!(c instanceof CompItem)||c.name!=='TRACKING_SOLVE')throw Error('Expected native solve comp');
 var solid=null,camera=null;
 for(var i=1;i<=c.numLayers;i++){var l=c.layer(i);if(l instanceof CameraLayer){if(camera)throw Error('Multiple cameras');camera=l;}else if(l.threeDLayer){if(solid)throw Error('Multiple reference planes');solid=l;}}
 if(!solid||!camera)throw Error('Native tracked camera and plane required');
 var image=app.project.importFile(new ImportOptions(new File(out+'/inputs/overlay.png')));
 solid.replaceSource(image,false);solid.name='LAB_TRACKED_OVERLAY';
 solid.property('ADBE Transform Group').property('ADBE Anchor Point').setValue([image.width/2,image.height/2,0]);
 solid.property('ADBE Transform Group').property('ADBE Scale').setValue([__SCALE__,__SCALE__,__SCALE__]);
 var probe=solid.property('ADBE Effect Parade').addProperty('ADBE Point Control');probe.name='LAB_PROJECTED_ANCHOR';
 probe.property(1).expression='var p=thisLayer.toComp(thisLayer.anchorPoint);[p[0],p[1]];';
 var cornerLocal=[[0,0,0],[image.width,0,0],[image.width,image.height,0],[0,image.height,0]];
 for(var corner=0;corner<4;corner++){var cp=solid.property('ADBE Effect Parade').addProperty('ADBE Point Control');cp.name='LAB_CORNER_'+corner;cp.property(1).expression='var p=thisLayer.toComp(['+cornerLocal[corner][0]+','+cornerLocal[corner][1]+',0]);[p[0],p[1]];';}
 var targetWidth=__SCREEN_WIDTH__,sizing=[];
 if(targetWidth!==null){
  for(var pass=0;pass<4;pass++){
   var left=Infinity,right=-Infinity;for(var j=0;j<4;j++){var p=solid.property('ADBE Effect Parade').property('LAB_CORNER_'+j).property(1).valueAtTime(0,false);left=Math.min(left,p[0]);right=Math.max(right,p[0]);}
   var measured=right-left;sizing.push(measured);if(!isFinite(measured)||measured<=0)throw Error('Invalid native projected footprint');
   if(Math.abs(measured-targetWidth)<0.1)break;
   var scale=solid.property('ADBE Transform Group').property('ADBE Scale').value;var factor=targetWidth/measured;
   solid.property('ADBE Transform Group').property('ADBE Scale').setValue([scale[0]*factor,scale[1]*factor,scale[2]*factor]);
  }
  if(Math.abs(sizing[sizing.length-1]-targetWidth)>=0.1)throw Error('Screen-space sizing did not converge');
 }
 var positions=[],corners=[];for(var frame=0;frame<Math.round(c.duration*c.frameRate);frame++){
  var xy=solid.property('ADBE Effect Parade').property('LAB_PROJECTED_ANCHOR').property(1).valueAtTime(frame/c.frameRate,false);positions.push([xy[0],xy[1]]);
  var quad=[];for(var corner=0;corner<4;corner++){var qxy=solid.property('ADBE Effect Parade').property('LAB_CORNER_'+corner).property(1).valueAtTime(frame/c.frameRate,false);quad.push([qxy[0],qxy[1]]);}corners.push(quad);
 }
 if(solid.property('ADBE Effect Parade').property('LAB_PROJECTED_ANCHOR').property(1).expressionError)throw Error('Projection expression failed');
 var fx=c.layer('ANALYSIS_SOURCE').property('ADBE Effect Parade').property('ADBE 3D Tracker');
 var errorLabel=fx.property('ADBE 3D Tracker-0311').name;
 write('projection-trace.json',{width:c.width,height:c.height,fps:c.frameRate,source_frames:positions.length,points:positions,corners:corners,native_error_label:errorLabel,position_key_count:camera.property('ADBE Transform Group').property('ADBE Position').numKeys});
 write('placement.json',{target_width_pixels:targetWidth,sizing_iterations:sizing,initial_scale:__SCALE__,final_scale:solid.property('ADBE Transform Group').property('ADBE Scale').value});
 if(app.project.renderQueue.numItems!==0)throw Error('Unexpected render queue');
 var queue=app.project.renderQueue.items.add(c);var om=queue.outputModule(1),templates=om.templates,selected='';
 for(var t=0;t<templates.length;t++)if(/H\.264/.test(templates[t])&&/15 Mbps/.test(templates[t])){selected=templates[t];break;}
 if(!selected)throw Error('Native H264 template unavailable');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');
 var id=c.id;app.project.save(new File(out+'/project.aep'));app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
 var reopened=app.project.itemByID(id);if(!reopened||!reopened.layer('LAB_TRACKED_OVERLAY'))throw Error('Native composite did not reopen');
 write('receipt.json',{status:'built',project_reopened:true,expression_errors:[],output_format:'mp4',selected_template:selected,native_camera:true,source:'flattened MP4 only',plane_source:'native tracker context menu',rendered:false});
}catch(e){write('receipt.json',{status:'failed',error:e.toString(),line:e.line});}
'''
body=body.replace('__TRACKING_PROJECT__',json.dumps((tracking/'tracking-attempt.aep').as_posix(),ensure_ascii=True)).replace('__SCALE__',str(a.scale)).replace('__SCREEN_WIDTH__',json.dumps(a.screen_width))
(out/'build.jsx').write_text('(function(){\n'+encoder+'var out='+json.dumps(out.as_posix(),ensure_ascii=True)+';\n'+body+'\n}());',encoding='utf-8')
input_path=tracking/'input.json'
cfg=json.loads(input_path.read_text(encoding='utf-8')) if input_path.is_file() else {'width':960,'height':540,'fps':24,'duration':4}
(out/'request.json').write_text(json.dumps({key:cfg[key] for key in ['width','height','fps','duration']}),encoding='utf-8')
print(out/'build.jsx')
