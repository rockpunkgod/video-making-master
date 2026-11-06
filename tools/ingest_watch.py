"""Invoke the existing Watch CLI and retain provenance; ingestion is not learning or verification."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='+');a=ap.parse_args()
source=ROOT/'sources/videos.json';registry=json.loads(source.read_text(encoding='utf-8'))
env=dict(os.environ);env['PATH']=str(ROOT/'.venv/Scripts')+os.pathsep+env['PATH'];env['PYTHONUTF8']='1'
evidence=ROOT/'cache/ingestion';evidence.mkdir(exist_ok=True)
for id in a.ids:
    entry=next((e for e in registry['videos'] if e['id']==id),None)
    if not entry:raise ValueError('ID not in user-provided source list: '+id)
    output=evidence/(id+'.txt')
    if output.exists():raise FileExistsError('Review existing evidence before rerunning '+id)
    print('WATCH '+id,flush=True)
    cmd=[str(ROOT/'.venv/Scripts/python.exe'),'D:/Codex/skills/watch/scripts/watch.py',entry['url'],'--engine','local','--no-whisper','--fps','0.03','--max-frames','18','--no-dedup','--resolution','1280','--out-dir',str(ROOT/'cache/watch')]
    try:
        completed=subprocess.run(cmd,capture_output=True,env=env,timeout=1200)
        text=completed.stdout.decode('utf-8',errors='replace');errors=completed.stderr.decode('utf-8',errors='replace');output.write_text(text+'\n## Process diagnostics\n'+errors,encoding='utf-8')
        media=re.search(r'\*\*Local media:\*\* `([^`]+)`',text);work=re.search(r'_Work dir: `([^`]+)`',text)
        record={'stage':'ingested_not_reviewed','exit_code':completed.returncode,'report':output.relative_to(ROOT).as_posix(),'local_media':media.group(1) if media else None,'work_dir':work.group(1) if work else None,'frames_reviewed':False,'transcript_reviewed':False}
        if completed.returncode:record['stage']='ingestion_failed'
    except subprocess.TimeoutExpired:
        output.write_text('Watch timed out; check run-owned partial artifacts before retry.\n',encoding='utf-8');record={'stage':'ingestion_timeout','report':output.relative_to(ROOT).as_posix(),'frames_reviewed':False,'transcript_reviewed':False}
    entry.setdefault('ingestion',[]).append(record)
    source.write_text(json.dumps(registry,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'id':id,**record},ensure_ascii=True),flush=True)
