"""Export five actual AE PNGs to distinguish text jitter from video codec residue."""
import argparse,json,subprocess,time,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--ae',required=True,type=Path);ap.add_argument('--collect-existing',action='store_true',help='Collect a completed owned audit without re-executing Adobe');a=ap.parse_args();root=a.directory.resolve()
cfg=json.loads((root/'request.json').read_text(encoding='utf-8'))
if not cfg.get('timeless'):raise ValueError('Audit is for the explicit stable-text correction')
out=root/'native-stability'
if out.exists() and not a.collect_existing:raise FileExistsError('Fresh native-stability evidence directory required')
if not a.collect_existing:out.mkdir()
result=out/'receipt.json'
body=r'''(function(){__ENCODER__
var out=__OUT__,target=__TARGET__,receipt={status:'failed'};
try{
 if(app.project&&app.project.numItems){var own=true,hasComp=false;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem){hasComp=true;if(app.project.item(i).comment!=='video-skills-lab:course-reproduction')own=false;}if(!own||!hasComp||app.project.dirty)throw Error('Preserve existing work');app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}
 app.open(new File(target));var comp=null;for(var i=1;i<=app.project.numItems;i++)if(app.project.item(i) instanceof CompItem&&app.project.item(i).name===__NAME__)comp=app.project.item(i);if(!comp)throw Error('Missing target composition');
 for(var f=0;f<5;f++)comp.saveFrameToPng(f,new File(out+'/frame-'+f+'.png'));
 receipt={status:'exported',times_seconds:[0,1,2,3,4],source_project:target};
}catch(e){receipt={status:'failed',error:e.toString()};}
var file=new File(out+'/receipt.json');file.encoding='UTF-8';file.open('w');file.write(encode(receipt));file.close();}());'''
body=body.replace('__ENCODER__',(Path(__file__).parent/'json_encode_adobe.jsx').read_text(encoding='utf-8')).replace('__OUT__',json.dumps(out.as_posix(),ensure_ascii=False)).replace('__TARGET__',json.dumps((root/'project.aep').as_posix(),ensure_ascii=False)).replace('__NAME__',json.dumps(cfg['name']))
jsx=out/'audit.jsx'
if not a.collect_existing:
 jsx.write_text(body,encoding='utf-8');subprocess.Popen([str(a.ae.resolve()),'-r',str(jsx)])
elif not jsx.is_file() or not result.is_file():raise FileNotFoundError('No owned completed audit to collect')
deadline=time.monotonic()+90
while time.monotonic()<deadline:
 if result.exists():break
 time.sleep(.5)
else:raise TimeoutError('Native still audit has no receipt; inspect Adobe before retry')
receipt=json.loads(result.read_text(encoding='utf-8-sig'))
if receipt.get('status')!='exported':raise RuntimeError(receipt)
# AE may return from saveFrameToPng before the output files finish flushing.
paths=[out/f'frame-{i}.png' for i in range(5)];previous=None;deadline=time.monotonic()+30
while time.monotonic()<deadline:
 sizes=[p.stat().st_size if p.exists() else 0 for p in paths]
 if all(sizes) and sizes==previous:break
 previous=sizes;time.sleep(.5)
else:raise TimeoutError('Native PNG exports not complete; do not resubmit the audit')
hashes=[hashlib.sha256((out/f'frame-{i}.png').read_bytes()).hexdigest() for i in range(5)]
report=dict(status='passed' if len(set(hashes))==1 else 'failed',times_seconds=receipt['times_seconds'],png_sha256=hashes,identical_native_png_files=len(set(hashes))==1,scope='Five native frame exports are byte-identical; full150-frame text equality is checked in the build receipt')
(root/'native-stability-quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
