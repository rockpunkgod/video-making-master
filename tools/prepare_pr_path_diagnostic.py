import json
from pathlib import Path
root=Path('.').resolve()
body=r'''(function(){var p=String(app.project.path),expected=__EXPECTED__;if(p.indexOf('video-skills-lab')<0)return 'not_lab';var arr=[];for(var i=0;i<Math.max(p.length,expected.length);i++)if(p.charCodeAt(i)!==expected.charCodeAt(i))arr.push(i+':'+p.charCodeAt(i)+'/'+expected.charCodeAt(i));return 'path='+p+';expected='+expected+';differences='+arr.join('|')+';pfile='+new File(p).fsName+';efile='+new File(expected).fsName+';lab_folder_exists='+new Folder(__ROOT__).exists+';temp_exists='+Folder.temp.exists;}());'''.replace('__EXPECTED__',json.dumps(str(root/'samples/pr-sound-001/project.prproj'),ensure_ascii=True)).replace('__ROOT__',json.dumps(root.as_posix(),ensure_ascii=True))
jsx='(function(){var bt=new BridgeTalk();bt.target="premierepro-26.0";bt.body='+json.dumps(body,ensure_ascii=True)+';bt.onResult=function(m){var f=new File('+json.dumps((root/'reports/pr-path-diagnostic.txt').as_posix(),ensure_ascii=True)+');f.encoding="UTF-8";f.open("w");f.write(m.body);f.close();};if(BridgeTalk.isRunning(bt.target))bt.send(15);}());'
(root/'tools/pr_path_diagnostic.jsx').write_text(jsx,encoding='utf-8')
