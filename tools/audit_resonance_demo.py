"""Read saved original-demo media and probe native recursive time precision."""
import argparse,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/after-effects/ae-advanced-expressions/scripts'))
from launch_adobe import launch
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--ae',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();d=a.directory.resolve();report=a.report.resolve()
if report.exists():raise FileExistsError('Fresh native audit report required')
c=json.loads((d/'request.json').read_text(encoding='utf-8'))
body='(function(){__ENC__\nvar path=__PROJECT__,out=__OUT__,rows=[];function write(v){var f=new File(out);f.encoding=\'UTF-8\';f.open(\'w\');f.write(encode(v));f.close();}try{if(app.project&&app.project.numItems){if(app.project.dirty)throw Error(\'Dirty project preserved\');for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).comment.indexOf(\'video-skills-lab:\')!==0)throw Error(\'Unowned project\');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}app.open(new File(path));var media=[],title=null;for(var i=1;i<=app.project.numItems;i++){var it=app.project.item(i);if(it instanceof FootageItem&&it.file)media.push({name:it.name,path:it.file.fsName,exists:it.file.exists,missing:it.footageMissing});if(it instanceof CompItem&&it.name===\'RESONANCE_MASTER\')title=it.layer(\'FINAL_TITLE\').text.sourceText.value.text;}var probe=app.project.items.addComp(\'TEMP_TIME_GRID\',32,32,1,2,30);probe.comment=\'video-skills-lab:resonance temporary audit\';var clock=probe.layers.addNull(2);clock.name=\'CLOCK\';var ef=clock.property(\'ADBE Effect Parade\').addProperty(\'ADBE Slider Control\');ef.name=\'tick\';ef.property(1).expression=\'time\';var sampler=probe.layers.addNull(2),value=sampler.property(\'ADBE Effect Parade\').addProperty(\'ADBE Slider Control\').property(1);value.expression=\'thisComp.layer("CLOCK").effect("tick")(1).valueAtTime(time-__DELAY__)\';var actual=value.valueAtTime(0,false),err=value.expressionError;probe.remove();app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File(path));write({status:\'completed\',completed:1,total:1,projects:[{project:path,media:media}],projects_modified:false,reopened_title:title,time_quantization_probe:{comp_fps:30,requested_previous_time:-__DELAY__,actual_sampled_time:actual,expression_error:err},scope:\'Saved project media readback; temporary probe removed without saving; final owned project reopened\'});}catch(e){write({status:\'failed\',error:e.toString(),line:e.line});}}());'

body=body.replace('__ENC__',(ROOT/'skills/after-effects/ae-advanced-expressions/scripts/json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__PROJECT__',json.dumps((d/'project.aep').as_posix())).replace('__OUT__',json.dumps(report.as_posix())).replace('__DELAY__',str(c['wave']['delay']))
jsx=d/'native-audit.jsx';jsx.write_text(body,encoding='utf-8');launch(a.ae,['-r',str(jsx)]);deadline=time.monotonic()+120
while time.monotonic()<deadline:
 if report.exists():
  try:r=json.loads(report.read_text(encoding='utf-8-sig'))
  except (ValueError,OSError):time.sleep(.2);continue
  print(json.dumps(r));raise SystemExit(0 if r['status']=='completed' else 1)
 time.sleep(.3)
raise RuntimeError('No native audit result; inspect existing Adobe handle before retry')
