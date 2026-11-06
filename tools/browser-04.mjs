const fs=await import('node:fs/promises');
const task=await taskSpace(14); const page=task.page('p1');
await page.goto('https://www.bilibili.com/video/BV1Yh4y1A7XT/');
console.log(await page.evaluate(()=>({pages:window.__INITIAL_STATE__?.videoData?.pages,desc:window.__INITIAL_STATE__?.videoData?.desc})));
await fs.writeFile('E:/自媒体/video-skills-lab/sources/BV1Yh4y1A7XT-parts.json',JSON.stringify(await page.evaluate(()=>window.__INITIAL_STATE__?.videoData?.pages),null,2),'utf8');
await page.evaluate(()=>document.querySelector('video')?.pause());
