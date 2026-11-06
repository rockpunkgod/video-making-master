import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'sources/videos.json';data=json.loads(source.read_text(encoding='utf-8'))
categories={
'BV1Yh4y1A7XT':['ae-procedural-motion','ae-advanced-expressions'],
'BV1c7GTzMEh5':['ae-advanced-expressions'],
'PbVB52WCUDE':['ae-3d-projection','ae-cinematic-camera'],
'BV1VE411r7Z5':['ae-mocha-tracking'],
'BV1xP411C7u3':['ae-mocha-tracking'],
'BV1nn4y1d7GJ':['ae-procedural-motion','ae-advanced-expressions'],
'wiISCTB4s1Y':['ae-cinematic-camera','ae-advanced-compositing'],
'U19f1A1ooFE':['ae-advanced-expressions'],
'BV1aK4y1U7Xv':['ae-3d-projection'],
'BV1qb4y1x7h1':['ae-mocha-tracking','ae-advanced-compositing'],
'BV1Pu411Q7DB':['ae-advanced-compositing'],
'OagnZAD_9wY':['pr-cinematic-sound'],
'KECzwyUursc':['pr-cinematic-sound'],
'vA5yAFOo_K8':['pr-cinematic-color'],
'BV1H44y1n7Be':['pr-cinematic-sound','pr-narrative-editing'],
'BV1jfxL6uEqo':['pr-narrative-editing'],
'BV1fy5T6xEbx':['pr-narrative-editing'],
'BV1Sf4y1D7T7':['pr-cinematic-color']}
lines=['# 课程来源清单','', '分类依据为已访问页面的标题、简介与分P目录；页面访问不等于完成学习。', '', '|序号|来源|章节数|候选技术|学习状态|','|---|---|---:|---|---|']
for e in data['videos']:
    e['categories']=categories[e['id']];e['classification_basis']='page title/description/part list; content unverified except noted passes'
    if e['id']=='BV1Yh4y1A7XT' and e['status'] in ['queued','page_inspected']:
        e['status']='partially_analyzed';e['passes']={'global':'partial: p1 overview; p5,p6 frames','detail':'partial: p5,p6 cue frames; p6 06:50-06:52 at 24fps','abstraction':'candidate: delayed procedural arrays'}
    n=len(e.get('parts',[])) or 1
    lines.append(f"|{e['order']}|[{e['title']}]({e['url']})|{n}|{', '.join(e['categories'])}|{'局部取证，尚未完整学习' if e['status']=='partially_analyzed' else '仅页面与目录'}|")
data['source_links']=len(data['videos']);data['chapter_count']=sum(len(e.get('parts',[])) or 1 for e in data['videos'])
data['retrieved_date']='2026-11-06';data['all_courses_learned']=False
source.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
(ROOT/'reports/source-catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for filename,box,target in [('desktop.png',(970,520,1585,850),'ae-cep-error.png'),('desktop-03.png',(715,309,1266,644),'ae-language-error.png')]:
    p=ROOT/'reports'/filename
    if p.is_file():
        Image.open(p).crop(box).save(ROOT/'reports'/target)
# Full desktop captures contain unrelated UI; only task-specific error crops are retained.
for filename in ['desktop.png','desktop-02.png','desktop-03.png']:
    (ROOT/'reports'/filename).unlink(missing_ok=True)
p=ROOT/'sources/first-page.txt'
if p.is_file():p.replace(ROOT/'cache/first-page-session-snapshot.txt')
print(f"{data['source_links']} links; {data['chapter_count']} chapters; see registry.json for verified skills")
