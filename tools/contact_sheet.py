from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import sys
folder=Path(sys.argv[1]); files=sorted(folder.glob('frame_*.jpg'))
for start in range(0,len(files),12):
    batch=files[start:start+12]; sheet=Image.new('RGB',(1280, len(range(0,len(batch),3))*264),'#222222'); draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(batch):
        im=Image.open(p); im.thumbnail((420,236)); x=(i%3)*426; y=(i//3)*264
        sheet.paste(im,(x,y));draw.text((x,y+238),p.name,fill='white')
    out=folder/f'contact-{start//12+1}.jpg';sheet.save(out); print(out)
