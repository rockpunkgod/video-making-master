"""Read-only inventory. Presence and launch health are intentionally separate."""
import json
import platform
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
paths={'afterfx':'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe',
       'aerender':'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe',
       'premiere':'E:/自媒体/Adobe Premiere Pro 2026/Adobe Premiere Pro.exe',
       'mocha_ae':'E:/自媒体/Adobe After Effects 2026/Support Files/Plug-ins/Effects/mochaAE/Resources/mochaui/bin/mocha4ae_adobe.exe',
       'watch':'D:/Codex/skills/watch/scripts/watch.py'}
report={'system':platform.platform(),'paths':{k:{'path':v,'exists':Path(v).is_file(),'execution':'not_proven_by_inventory'} for k,v in paths.items()},'binaries':{}}
for name,args in [('ffmpeg',['-version']),('ffprobe',['-version']),('yt-dlp',['--version']),('ego-browser',['--version'])]:
    binary=shutil.which(name)
    if name=='yt-dlp' and not binary:
        candidate=ROOT/'.venv/Scripts/yt-dlp.exe';binary=str(candidate) if candidate.is_file() else None
    record={'path':binary,'available':bool(binary)}
    if binary:
        try:
            r=subprocess.run([binary,*args],capture_output=True,timeout=20)
            record.update(exit_code=r.returncode,version=(r.stdout+r.stderr).decode(errors='replace').splitlines()[:2])
        except subprocess.TimeoutExpired:record['error']='version query timed out'
    report['binaries'][name]=record
(ROOT/'reports/environment.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
