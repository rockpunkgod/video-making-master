"""Remove published lab intermediates inside explicitly selected managed scopes.

Default is a reviewable plan. --apply requires that the exact delivery manifest
is committed and pushed, validates all retained hashes, and never follows links.
Uses file deletion and empty-directory removal, not recursive shell deletion.
"""
import argparse,hashlib,json,os,stat,subprocess,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--scope',action='append',required=True)
ap.add_argument('--keep-active',action='append',default=[],help='Exact still-needed learning input, relative to lab root')
ap.add_argument('--report',type=Path,required=True);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
root=ROOT.resolve();managed=[root/'cache',root/'samples']
def safe(p):
    p=p.resolve();p.relative_to(root)
    if not any(p==m or m in p.parents for m in managed):raise ValueError('Cleanup scope outside cache/samples: '+str(p))
    return p
def link(p):return p.is_symlink() or bool(getattr(p,'is_junction',lambda:False)())
manifest_file=root/'reports/git-delivery-manifest.json';manifest_bytes=manifest_file.read_bytes();manifest=json.loads(manifest_bytes)
keep={safe(root/r['path']) for r in manifest['files'] if (root/r['path']).resolve().is_relative_to(root/'samples') or (root/r['path']).resolve().is_relative_to(root/'cache')}
active={safe(root/p) for p in a.keep_active}
if any(not p.is_file() for p in active):raise FileNotFoundError('Explicit active learning input missing')
keep|=active
for record in manifest['files']:
    p=root/record['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('Retained delivery hash mismatch: '+record['path'])
scopes=[safe(root/s) for s in a.scope]
if any(link(p) or not p.is_dir() for p in scopes):raise ValueError('Scope must be an existing real directory')
targets={};links=[]
for scope in scopes:
    for base,dirs,files in os.walk(scope,followlinks=False):
        for name in list(dirs):
            p=Path(base)/name
            if link(p):links.append(str(p.relative_to(root)));dirs.remove(name)
        for name in files:
            p=Path(base)/name
            if link(p):links.append(str(p.relative_to(root)));continue
            p=safe(p)
            if p not in keep:targets[p]=dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
report=dict(status='planned',scopes=[p.relative_to(root).as_posix() for p in scopes],published_commit=head,
    manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),files=len(targets),bytes=sum(r['bytes'] for r in targets.values()),
    keep_active=[p.relative_to(root).as_posix() for p in sorted(active)],protected_delivery_files=len(keep),skipped_links=links,
    targets=[targets[p] for p in sorted(targets)],authorization='User requested keeping only deliverables after library publication; scope restricted to this independent lab')
output=a.report.resolve();output.relative_to(root/'reports');output.parent.mkdir(parents=True,exist_ok=True)
if output.exists():raise FileExistsError('Fresh cleanup report required')
if a.apply:
    committed=subprocess.check_output(['git','show','HEAD:reports/git-delivery-manifest.json'],cwd=root)
    if committed!=manifest_bytes:raise ValueError('Commit the exact delivery manifest before cleanup')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+branch],cwd=root,text=True).split()
    if not remote or remote[0]!=head:raise ValueError('Delivery commit not verified on origin; publish before deleting intermediates')
    report['status']='running';output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    deleted=freed=0;errors=[]
    for p in sorted(targets):
        safe(p)
        if link(p) or p in keep:raise ValueError('Deletion target changed to protected/link path')
        try:
            p.unlink();deleted+=1;freed+=targets[p]['bytes']
        except OSError as error:errors.append(dict(path=targets[p]['path'],error=str(error)))
    for scope in scopes:
        for base,dirs,files in os.walk(scope,topdown=False,followlinks=False):
            p=Path(base)
            if p==scope or link(p):continue
            safe(p)
            try:p.rmdir()
            except OSError:pass
    changed=[]
    for record in manifest['files']:
        p=root/record['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=record['sha256']:changed.append(record['path'])
    report.update(status='completed' if not errors and not changed else 'incomplete',deleted_files=deleted,deleted_bytes=freed,
                  errors=errors,retained_hash_changes=changed,completed_at=time.strftime('%Y-%m-%d %H:%M:%S'))
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in {'targets','authorization'}},ensure_ascii=True,indent=2))
raise SystemExit(0 if report['status'] in {'planned','completed'} else 1)
