"""Create three original test inputs and declarative requests, without emulating AE output."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
asset_dir=ROOT/'samples/fixtures';asset_dir.mkdir(parents=True,exist_ok=True)
im=Image.new('RGBA',(512,512),(0,0,0,0));d=ImageDraw.Draw(im)
d.rounded_rectangle((80,80,432,432),radius=60,outline='#37dbff',width=14)
d.ellipse((180,180,332,332),outline='white',width=10);im.save(asset_dir/'geometry.png')
im=Image.new('RGBA',(640,360),(0,0,0,0));d=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',66)
d.text((40,90),'MOTION 02',font=font,fill='#ffd33d');d.line((40,185,580,185),fill='white',width=8)
im.save(asset_dir/'typography.png')
im=Image.new('RGBA',(512,512),(0,0,0,0));d=ImageDraw.Draw(im)
for row in range(16):
    for col in range(16):
        if (row+col)%3!=0:
            d.rectangle((col*32+4,row*32+4,col*32+27,row*32+27),fill=(60+col*9,80+row*9,220,180))
im.save(asset_dir/'texture.png')
base=json.loads((ROOT/'skills/after-effects/ae-procedural-motion/examples/square.json').read_text())
manifest=[]
for name in ['geometry','typography','texture']:
    asset=asset_dir/f'{name}.png';cfg={**base,'name':'asset-'+name,'count':12,'asset':asset.as_posix()}
    (asset_dir/f'{name}.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    manifest.append({'name':name,'file':asset.name,'sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'provenance':'original synthetic test input; not a tutorial asset'})
(asset_dir/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Created 3 original fixture images and 3 requests; AE generalization tests remain unrun.')
