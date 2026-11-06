"""Stage an explicit standalone delivery without tutorial caches or duplicated runs.

Does not commit or push. Existing artifacts are preserved on disk.
"""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[
 'samples/course-reproduction-009/p14-baseline-002',
 'samples/course-reproduction-009/p14-algorithm-001',
 'samples/course-reproduction-009/p14-motion2026-001',
 'samples/course-reproduction-009/p14-ai-001',
 'samples/course-reproduction-002/p06-final-003',
 'samples/course-reproduction-002/p06-delay5-002',
 'samples/course-generalization-001/geometry',
 'samples/course-generalization-001/typography',
 'samples/course-generalization-001/texture',
 'samples/course-reproduction-003/p07-blocks-002',
 'samples/course-reproduction-003/p07-tint-001',
 'samples/course-reproduction-003/p07-seed7-isolated-001',
 'samples/course-reproduction-004/p08-disappear-001',
 'samples/course-reproduction-004/p08-appear-001',
 'samples/course-reproduction-004/p08-geometry-001',
 'samples/course-reproduction-004/p08-typography-001',
 'samples/course-reproduction-004/p08-texture-001',
 'samples/course-reproduction-005/p09-final-002',
 'samples/course-reproduction-005/p09-seed165-speed310-001',
 'samples/course-reproduction-005/p09-geometry-001',
 'samples/course-reproduction-005/p09-typography-001',
 'samples/course-reproduction-005/p09-texture-001',
 'samples/course-reproduction-006/p10-decimal-binary-002',
 'samples/course-reproduction-006/p10-variation-001',
 'samples/course-reproduction-006/p10-single-digit-001',
 'samples/course-reproduction-006/p10-decimal-binary-003',
 'samples/course-reproduction-006/p10-variation-002',
 'samples/course-reproduction-006/p10-single-digit-002',
 'samples/course-reproduction-006/p10-controls-animation-005',
 'samples/course-reproduction-006/p10-reference-replay-006',
 'samples/course-reproduction-006/p10-reference-variation-001',
 'samples/course-reproduction-006/p10-reference-standalone-001',
 'samples/course-reproduction-007/p11-baseline-001',
 'samples/course-reproduction-007/p11-variation-002',
 'samples/course-reproduction-007/p11-geometry-002',
 'samples/course-reproduction-007/p11-typography-002',
 'samples/course-reproduction-007/p11-texture-002',
 'samples/course-reproduction-008/p12-baseline-001',
 'samples/course-reproduction-008/p12-seed0-001',
 'samples/course-reproduction-008/p12-sparse-002',
 'samples/tracking-fixture-001/solve-calibrated-001/composite-001',
 'samples/tracking-fixture-001/solve-calibrated-001/composite-typography',
 'samples/tracking-gallery-001/solve-001/composite-pixel-sized',
 'samples/tracking-corridor-001/solve-calibrated-001/composite-pixel-sized',
 'samples/pr-sound-suite-002/baseline',
 'samples/pr-sound-suite-002/variation',
 'samples/pr-sound-suite-002/reveal',
]
chosen=[]
for name in CASES:
 folder=ROOT/name
 if not folder.is_dir():raise FileNotFoundError(folder)
 for path in folder.rglob('*'):
  if not path.is_file():continue
  rel=path.relative_to(folder)
  if rel.parts[0] in {'inputs','assets'}:
   if path.suffix.lower() in {'.png','.jpg','.jpeg','.wav','.mp3','.mp4','.json','.md'}:chosen.append(path)
  elif len(rel.parts)==1 and (path.name in {'project.aep','project.prproj','final.mp4','native-mix.wav','credits.md','build.jsx'} or path.suffix.lower()=='.json'):
   chosen.append(path)
  elif len(rel.parts)==1 and path.name.startswith('native-still-') and path.suffix.lower()=='.png':
   chosen.append(path)
 # Every published demonstration must include both its actual native project and video.
 if not (folder/'final.mp4').is_file() or not any((folder/p).is_file() for p in ['project.aep','project.prproj']):raise ValueError('Incomplete native delivery '+name)
for path in (ROOT/'evaluations').rglob('*'):
 if path.is_file() and path.suffix.lower() in {'.json','.md','.jsx','.py','.txt','.log'} and '__pycache__' not in path.parts:chosen.append(path)
chosen=sorted(set(chosen))
records=[]
for path in chosen:
 size=path.stat().st_size
 if size>=100_000_000:raise ValueError('GitHub single-file limit requires another delivery method: '+str(path))
 records.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
manifest=dict(scope='Standalone video-skills-lab progress snapshot; overall curriculum incomplete',cases=CASES,files=records,
 excluded=['tutorial media and frames in cache','local environments and models','duplicate/failed intermediate native binaries','Adobe preset files derived from installed vendor files','Adobe autosave and transport data','repeated native audio/video exports'],
 portability='Native projects retain original Windows media paths. Rebuild from the bundled scripts or relink the bundled inputs/assets; historical report references may point to local-only artifacts.',
 total_selected_bytes=sum(r['bytes'] for r in records))
(ROOT/'reports/git-delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
subprocess.run(['git','add','--','.gitignore','.gitattributes','AGENTS.md','README.md','registry.json','skills','sources','tools','reports'],cwd=ROOT,check=True)
for start in range(0,len(chosen),60):subprocess.run(['git','add','-f','--',*[p.relative_to(ROOT).as_posix() for p in chosen[start:start+60]]],cwd=ROOT,check=True)
print(json.dumps(dict(selected_files=len(chosen),selected_MB=round(manifest['total_selected_bytes']/1048576,2),native_demonstrations=len(CASES)),indent=2))
