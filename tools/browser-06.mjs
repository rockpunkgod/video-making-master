const fs=await import('node:fs/promises');const task=await taskSpace(14);const page=task.page('p1');
const path='E:/自媒体/video-skills-lab/sources/videos.json';const list=JSON.parse(await fs.readFile(path,'utf8'));
for(const entry of list.videos.filter(e=>e.platform==='bilibili')) {
 await page.goto(entry.url,{timeout:25000});
 const data=await page.evaluate(()=>({pages:window.__INITIAL_STATE__?.videoData?.pages?.map(p=>({page:p.page,part:p.part,duration:p.duration})),description:window.__INITIAL_STATE__?.videoData?.desc}));
 entry.parts=data.pages||[];entry.description=data.description||entry.page?.description;
 await page.evaluate(()=>document.querySelector('video')?.pause());
 await fs.writeFile(path,JSON.stringify(list,null,2),'utf8');console.log({id:entry.id,parts:entry.parts.length});
}
