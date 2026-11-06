const task=await taskSpace(14);const page=task.page('p1');
await page.goto('https://aescripts.com/projection-3d/',{timeout:30000});
console.log(await page.snapshot({scope:'full_page'}));
