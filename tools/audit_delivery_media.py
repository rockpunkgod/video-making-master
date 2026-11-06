"""Read dependencies from owned saved AEPs before any intermediate cleanup.

Generates a reviewed read-only Adobe audit; does not launch or modify projects.
"""
import ast,json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
tree=ast.parse((root/'tools/prepare_git_delivery.py').read_text(encoding='utf-8'))
cases=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASES' for t in n.targets))
projects=[(root/name/'project.aep').as_posix() for name in cases if (root/name/'project.aep').is_file()]
out=root/'reports/native-media-dependencies.json'
if out.exists():raise FileExistsError('Preserve the previous audit or select a fresh evidence output')
body=r'''(function(){__ENC__
var paths=__PATHS__,out=__OUT__,rows=[],restore=null;
function write(result){var f=new File(out);f.encoding='UTF-8';f.open('w');f.write(encode(result));f.close();}
function closeOwned(){
 if(!app.project||!app.project.numItems)return;
 if(app.project.dirty)throw Error('Dirty Adobe project preserved');
 for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment.indexOf('video-skills-lab:')!==0)throw Error('Unowned Adobe project preserved');
 app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}
try{
 if(app.project&&app.project.file)restore=app.project.file.fsName;
 for(var pi=0;pi<paths.length;pi++){
  closeOwned();app.open(new File(paths[pi]));var media=[];
  for(var j=1;j<=app.project.numItems;j++){var item=app.project.item(j);if(item instanceof FootageItem&&item.file)media.push({name:item.name,path:item.file.fsName,exists:item.file.exists,missing:item.footageMissing});if((item instanceof CompItem||item instanceof FootageItem)&&item.proxySource&&item.proxySource.file){var pf=item.proxySource.file;media.push({name:item.name,kind:'proxy',path:pf.fsName,exists:pf.exists,missing:!pf.exists,use_proxy:item.useProxy});}}
  rows.push({project:paths[pi],media:media});write({status:'running',completed:rows.length,total:paths.length,projects:rows});
 }
 closeOwned();if(restore)app.open(new File(restore));write({status:'completed',completed:rows.length,total:paths.length,projects:rows,projects_modified:false,previous_project_restored:restore});
}catch(e){write({status:'failed',error:e.toString(),line:e.line,completed:rows.length,total:paths.length,projects:rows});}
}());'''
body=body.replace('__ENC__',(root/'skills/after-effects/ae-procedural-motion/scripts/json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__PATHS__',json.dumps(projects)).replace('__OUT__',json.dumps(out.as_posix()))
(root/'tools/audit_delivery_media.jsx').write_text(body,encoding='utf-8')
print(json.dumps(dict(projects=len(projects),output=str(out)),indent=2))
