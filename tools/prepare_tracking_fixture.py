"""Create an original textured 3D test scene, so a tracking skill need not depend on tutorial footage."""
import json
import random
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1];out=ROOT/'samples/tracking-fixture-001';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',22)
for index,name in enumerate(['floor','back','side']):
    rng=random.Random(110+index);im=Image.new('RGB',(1024,1024),(50+index*25,62,80));draw=ImageDraw.Draw(im)
    for row in range(12):
        for col in range(12):
            x=col*84+8;y=row*84+8;color=tuple(rng.randint(70,230) for _ in range(3));draw.rectangle((x,y,x+65,y+65),fill=color)
            for detail in range(5):
                dx=rng.randrange(8,55);dy=rng.randrange(8,55);draw.rectangle((x+dx,y+dy,x+dx+5,y+dy+5),fill=(15,20,30))
            draw.text((x+5,y+20),f'{index}{row:X}{col:X}',font=font,fill=(240,240,240))
    im.save(out/f'{name}.png')
script=r'''
(function(){
var out=__OUTPUT__;
try{
 if(app.project&&app.project.numItems>0)throw Error('Open empty project before fixture creation');
 if(!app.project)app.newProject();
 var c=app.project.items.addComp('TRACKING_SOURCE',960,540,1,4,24);c.comment='video-skills-lab:tracking-fixture';
 function plane(name,position,rotation,size){var src=app.project.importFile(new ImportOptions(new File(out+'/'+name+'.png')));var l=c.layers.add(src);l.name=name;l.threeDLayer=true;var t=l.property('ADBE Transform Group');t.property('ADBE Position').setValue(position);t.property('ADBE Scale').setValue([size,size,size]);t.property('ADBE Orientation').setValue(rotation);return l;}
 plane('back',[480,270,2000],[0,0,0],300);
 plane('floor',[480,1050,800],[90,0,0],300);
 plane('side',[-850,270,800],[0,90,0],300);
 var camera=c.layers.addCamera('GROUND_TRUTH_CAMERA',[480,270]);var tr=camera.property('ADBE Transform Group');
 tr.property('ADBE Position').setValueAtTime(0,[200,180,-1300]);tr.property('ADBE Position').setValueAtTime(4,[760,340,-900]);
 tr.property('ADBE Anchor Point').setValue([480,400,1200]);camera.property('ADBE Camera Options Group').property('ADBE Camera Zoom').setValue(900);
 var rq=app.project.renderQueue.items.add(c);var om=rq.outputModule(1);var names=om.templates,selected='';for(var i=0;i<names.length;i++)if(/H\.264/.test(names[i])&&/15 Mbps/.test(names[i])){selected=names[i];break;}
 if(!selected)throw Error('No known native H264 template');om.applyTemplate(selected);om.file=new File(out+'/source.mp4');
 app.project.save(new File(out+'/source-scene.aep'));
 var f=new File(out+'/fixture-status.json');f.encoding='UTF-8';f.open('w');f.write('{"status":"built","width":960,"height":540,"fps":24,"duration":4,"purpose":"original tracking input; not a solved camera"}');f.close();
}catch(e){var err=new File(out+'/fixture-error.txt');err.encoding='UTF-8';err.open('w');err.write(e.toString());err.close();}
}());
'''
(out/'build-source.jsx').write_text(script.replace('__OUTPUT__',json.dumps(out.as_posix(),ensure_ascii=True)),encoding='utf-8')
print(out/'build-source.jsx')
