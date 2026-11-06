"""Original, structurally different camera-tracking inputs; source scenes are never solver inputs."""
import argparse
import json
import random
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ap=argparse.ArgumentParser();ap.add_argument('variant',choices=['gallery','corridor']);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25)
for k in range(4):
    rng=random.Random(930+k if a.variant=='gallery' else 1260+k)
    im=Image.new('RGB',(1024,1024),(225,215,190) if a.variant=='gallery' else (38,49,58));d=ImageDraw.Draw(im)
    if a.variant=='gallery':
        # Non-repeating exhibition posters, circular forms and line drawings.
        for i in range(20):
            x=rng.randrange(20,850);y=rng.randrange(20,870);w=rng.randrange(65,160);h=rng.randrange(55,135)
            d.rectangle((x-5,y-5,x+w+5,y+h+5),fill=(32,31,35));d.rectangle((x,y,x+w,y+h),fill=tuple(rng.randrange(70,225) for _ in range(3)))
            d.ellipse((x+8,y+8,x+w-8,y+h-8),outline=(245,245,240),width=5)
            d.text((x+8,y+12),f'{k}-{i:02}',font=font,fill=(20,20,20))
        for i in range(120):
            x=rng.randrange(1020);y=rng.randrange(1020);d.line((x,y,x+15,y+9),fill=(65,55,45),width=3)
    else:
        # Industrial panels and distinct non-periodic hazard marks.
        for row in range(5):
            for col in range(4):
                x=col*250+12;y=row*200+10;d.rounded_rectangle((x,y,x+220,y+175),radius=8,fill=(70+rng.randrange(30),80,87),outline=(160,170,175),width=3)
                d.text((x+12,y+10),f'BAY {k}{row}{col}',font=font,fill=(240,185,45))
                for i in range(12):
                    xx=x+rng.randrange(12,195);yy=y+rng.randrange(50,155);d.rectangle((xx,yy,xx+7,yy+7),fill=(220,225,220))
                d.line((x+12,y+155,x+100,y+80),fill=(220,165,25),width=8)
    im.save(out/f'texture-{k}.png')

if a.variant=='gallery':
    duration=5;zoom=950
    planes=[('back',0,[480,270,1900],[0,0,0],280),('floor',1,[480,1150,550],[90,0,0],320),('left',2,[-800,270,650],[0,90,0],260),('display',3,[1100,320,1100],[0,-30,0],75)]
    start=[100,260,-1250];end=[690,180,-900];target=[480,340,1300]
else:
    duration=3.5;zoom=800
    planes=[('back',0,[480,270,2500],[0,0,0],250),('floor',1,[480,1100,1150],[90,0,0],400),('left',2,[-650,270,1200],[0,90,0],340),('right',3,[1610,270,1200],[0,-90,0],340)]
    start=[320,200,-1800];end=[510,340,-850];target=[500,400,2200]
cfg={'variant':a.variant,'width':960,'height':540,'fps':24,'duration':duration,'zoom':zoom,'planes':planes,'start':start,'end':end,'target':target}
(out/'fixture.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
encoder=(Path(__file__).resolve().parents[1]/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_text(encoding='utf-8');encoder=encoder[encoder.index('    function encode'):encoder.index('    function write')]
script=r'''
(function(){var out=__OUT__,cfg=__CFG__;
__ENCODER__
function write(n,v){var f=new File(out+'/'+n);f.encoding='UTF-8';f.open('w');f.write(encode(v));f.close();}
try{
if(app.project&&app.project.numItems>0)throw Error('Expected empty project');if(!app.project)app.newProject();
var c=app.project.items.addComp('TRACKING_SOURCE',cfg.width,cfg.height,1,cfg.duration,cfg.fps);c.comment='video-skills-lab:original-tracking-fixture';
for(var i=0;i<cfg.planes.length;i++){var p=cfg.planes[i];var src=app.project.importFile(new ImportOptions(new File(out+'/texture-'+p[1]+'.png')));var l=c.layers.add(src);l.name=p[0];l.threeDLayer=true;var t=l.property('ADBE Transform Group');t.property('ADBE Position').setValue(p[2]);t.property('ADBE Orientation').setValue(p[3]);t.property('ADBE Scale').setValue([p[4],p[4],p[4]]);}
var camera=c.layers.addCamera('GROUND_TRUTH_CAMERA',[480,270]);var t=camera.property('ADBE Transform Group');t.property('ADBE Position').setValueAtTime(0,cfg.start);t.property('ADBE Position').setValueAtTime(cfg.duration,cfg.end);t.property('ADBE Anchor Point').setValue(cfg.target);camera.property('ADBE Camera Options Group').property('ADBE Camera Zoom').setValue(cfg.zoom);
var queue=app.project.renderQueue.items.add(c);var om=queue.outputModule(1),templates=om.templates,selected='';for(var i=0;i<templates.length;i++)if(/H\.264/.test(templates[i])&&/15 Mbps/.test(templates[i])){selected=templates[i];break;}
if(!selected)throw Error('No native H264 template');om.applyTemplate(selected);om.file=new File(out+'/native.mp4');app.project.save(new File(out+'/project.aep'));
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(out+'/project.aep'));
write('receipt.json',{status:'built',project_reopened:true,expression_errors:[],selected_template:selected,output_format:'mp4',purpose:'original input only, not solver output'});
}catch(e){write('receipt.json',{status:'failed',error:e.toString()});}
}());
'''
script=script.replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=True)).replace('__CFG__',json.dumps(cfg)).replace('__ENCODER__',encoder)
(out/'build.jsx').write_text(script,encoding='utf-8');(out/'request.json').write_text(json.dumps({k:cfg[k] for k in ['width','height','fps','duration']}),encoding='utf-8')
print(out/'build.jsx')
