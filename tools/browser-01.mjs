const fs = await import('node:fs/promises');
const task = await taskSpace('video-skills-lab-20261106');
console.log({spaceId:task.spaceId});
const page = task.page('p1');
await page.goto('https://www.bilibili.com/video/BV1Yh4y1A7XT/');
const snapshot = await page.snapshot({scope:'full_page'});
await fs.writeFile('E:/自媒体/video-skills-lab/sources/first-page.txt',snapshot,'utf8');
console.log(snapshot);
