const fs = await import('node:fs/promises');
const task = await taskSpace(14);
const page = task.page('p1');
console.log(await page.evaluate(() => ({title:document.title,description:document.querySelector('meta[name="description"]')?.content,video:[...document.querySelectorAll('video')].map(v=>({time:v.currentTime,duration:v.duration,paused:v.paused}))})));
await page.evaluate(()=>document.querySelector('video')?.pause());
const list = JSON.parse(await fs.readFile('E:/自媒体/video-skills-lab/sources/videos.json','utf8'));
for (const entry of list.videos) {
  try {
    await page.goto(entry.url,{timeout:25000});
    const data = await page.evaluate(()=>({title:document.title,description:document.querySelector('meta[name="description"]')?.content||'',heading:document.querySelector('h1')?.textContent||'',duration:document.querySelector('video')?.duration||null}));
    entry.page=data; entry.title=data.heading||data.title; entry.status='page_inspected';
    await page.evaluate(()=>document.querySelector('video')?.pause());
    console.log({id:entry.id,...data});
  } catch(e) {entry.status='page_unavailable';entry.error=String(e).slice(0,500);console.log({id:entry.id,error:entry.error});}
  await fs.writeFile('E:/自媒体/video-skills-lab/sources/videos.json',JSON.stringify(list,null,2),'utf8');
}
