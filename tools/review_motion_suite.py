"""Extract viewable native-render evidence and record objective temporal statistics."""
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
suite=ROOT/'samples/runs/suite-20261106-091450';results=json.loads((suite/'results.json').read_text(encoding='utf-8'))
review_root=ROOT/'evaluations/motion-suite-001';review_root.mkdir(exist_ok=True)
for record in results:
    run=ROOT/record['run'];cfg=json.loads((run/'request.json').read_text(encoding='utf-8'));folder=review_root/cfg['name'];folder.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1200,850),'#202020');draw=ImageDraw.Draw(sheet)
    for i,fraction in enumerate([0.08,0.2,0.4,0.6,0.8,0.96]):
        timestamp=cfg['duration']*fraction;target=folder/f'frame_{i:02d}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(timestamp),'-i',str(run/'final.mp4'),'-frames:v','1',str(target)],check=True)
        im=Image.open(target);im.thumbnail((390,390));x=(i%3)*400;y=(i//3)*425;sheet.paste(im,(x+(390-im.width)//2,y))
        draw.text((x+8,y+395),f"{cfg['name']} t={timestamp:.2f}s",fill='white')
    sheet.save(folder/'review.jpg')
    raw=subprocess.run(['ffmpeg','-v','error','-i',str(run/'final.mp4'),'-vf','scale=64:64,format=gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
    frames=[raw[i:i+4096] for i in range(0,len(raw),4096)];diffs=[sum(abs(a-b) for a,b in zip(frames[i-1],frames[i]))/4096 for i in range(1,len(frames))]
    stats={'decoded_frames':len(frames),'consecutive_frame_mad_max':max(diffs),'consecutive_frame_mad_mean':sum(diffs)/len(diffs),'interpretation':'objective difference statistics only; not an aesthetic score or hard-cut proof'}
    (folder/'temporal-statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print((folder/'review.jpg').as_posix())
