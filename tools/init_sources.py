import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = ['BV1Yh4y1A7XT','BV1c7GTzMEh5','PbVB52WCUDE','BV1VE411r7Z5','BV1xP411C7u3','BV1nn4y1d7GJ','wiISCTB4s1Y','U19f1A1ooFE','BV1aK4y1U7Xv','BV1qb4y1x7h1','BV1Pu411Q7DB','OagnZAD_9wY','KECzwyUursc','vA5yAFOo_K8','BV1H44y1n7Be','BV1jfxL6uEqo','BV1fy5T6xEbx','BV1Sf4y1D7T7']
for name in ['sources/learning-notes','skills/after-effects','skills/premiere-pro','samples','evaluations','reports','cache/watch']:
    (ROOT/name).mkdir(parents=True, exist_ok=True)
videos = [dict(order=i+1,id=id,platform='bilibili' if id.startswith('BV') else 'youtube',url=f'https://www.bilibili.com/video/{id}/' if id.startswith('BV') else f'https://www.youtube.com/watch?v={id}',status='queued',title=None,categories=[],passes={'global':'pending','detail':'pending','abstraction':'pending'}) for i,id in enumerate(IDS)]
target=ROOT/'sources/videos.json'
if not target.exists():
    target.write_text(json.dumps({'schema_version':1,'videos':videos},ensure_ascii=False,indent=2),encoding='utf-8')
