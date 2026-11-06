const fs=await import('node:fs/promises'); const task=await taskSpace(14); const page=task.page('p1');
await page.goto('https://helpx.adobe.com/after-effects/kb/after-effects-could-not-load-cep-suite.html',{timeout:30000});
console.log(await page.snapshot());
