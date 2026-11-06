const fs = await import('node:fs/promises');
const task = await taskSpace(14);
const page = task.page('p1');
await fs.mkdir('E:/自媒体/video-skills-lab/sources',{recursive:true});
const snapshot = await page.snapshot({scope:'full_page'});
await fs.writeFile('E:/自媒体/video-skills-lab/sources/first-page.txt',snapshot,'utf8');
console.log(snapshot);
