"""Check staged publication content, exact demo hashes, JSON and Python syntax."""
import hashlib,json,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw=subprocess.check_output(['git','ls-files','-z'],cwd=root);names=[n.decode('utf-8') for n in raw.split(b'\0') if n]
bad=[];json_count=0;py_count=0
pattern=re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for name in names:
 p=root/name;parts=p.relative_to(root).parts
 if any(s in {'.venv','cache','__pycache__','.env','.git-credentials'} for s in parts) or p.suffix=='.pyc':bad.append('forbidden path '+name)
 data=p.read_bytes()
 if p.stat().st_size>=100_000_000:bad.append('oversize '+name)
 if p.suffix.lower() in {'.py','.jsx','.ps1','.mjs','.json','.md','.txt','.log'}:
  if pattern.search(data):bad.append('possible credential '+name)
 if p.suffix=='.json':
  try:json.loads(data.decode('utf-8-sig'));json_count+=1
  except Exception as e:bad.append('JSON invalid '+name+': '+str(e))
 if p.suffix=='.py':
  try:compile(data,str(p),'exec');py_count+=1
  except Exception as e:bad.append('Python syntax invalid '+name+': '+str(e))
manifest=json.loads((root/'reports/git-delivery-manifest.json').read_text(encoding='utf-8'))
for r in manifest['files']:
 if r['path'] not in names:bad.append('unstaged delivery '+r['path']);continue
 if hashlib.sha256((root/r['path']).read_bytes()).hexdigest()!=r['sha256']:bad.append('delivery SHA changed '+r['path'])
for name in manifest['cases']:
 folder=root/name;q=json.loads((folder/'quality.json').read_text(encoding='utf-8-sig'))
 if q.get('sha256') and hashlib.sha256((folder/'final.mp4').read_bytes()).hexdigest()!=q['sha256']:bad.append('video/quality SHA mismatch '+name)
print(json.dumps(dict(status='failed' if bad else 'passed',tracked_files=len(names),json_parsed=json_count,python_compiled=py_count,native_demonstrations=len(manifest['cases']),problems=bad),ensure_ascii=False,indent=2))
raise SystemExit(bool(bad))
