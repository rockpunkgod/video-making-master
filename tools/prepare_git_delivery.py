"""Stage an explicit standalone delivery without tutorial caches or duplicated runs.

Does not commit or push. Existing artifacts are preserved on disk.
"""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[
 'samples/course2-rotation-001/baseline-004',
 'samples/course2-rotation-001/variation-001',
 'samples/course2-rotation-001/hexagons-001',
 'samples/course2-rotation-001/tags-001',
 'samples/course2-rotation-001/stars-001',
 'samples/course2-rotation-001/isolated-001',
 'samples/course2-rotation-001/boundary-original-001',
 'samples/course2-rotation-001/boundary-repaired-001',
 'samples/course2-scroll-001/horizontal-001',
 'samples/course2-scroll-001/horizontal-grid-001',
 'samples/course2-scroll-001/horizontal-map-001',
 'samples/course2-scroll-001/horizontal-overshoot-001',
 'samples/course2-scroll-001/horizontal-type-001',
 'samples/course2-scroll-001/horizontal-variation-isolated-001',
 'samples/course2-scroll-001/vertical-006',
 'samples/course2-scroll-001/vertical-grid-001',
 'samples/course2-scroll-001/vertical-map-001',
 'samples/course2-scroll-001/vertical-overshoot-001',
 'samples/course2-scroll-001/vertical-type-001',
 'samples/course2-magnifier-001/baseline-002',
 'samples/course2-magnifier-001/variation-001',
 'samples/course2-magnifier-001/grid-001',
 'samples/course2-magnifier-001/type-001',
 'samples/course2-magnifier-001/map-001',
 'samples/course2-butterfly-001/flap-baseline-003',
 'samples/course2-butterfly-001/flap-fast-002',
 'samples/course2-butterfly-001/moth-002',
 'samples/course2-butterfly-001/petal-002',
 'samples/course2-butterfly-001/mechanical-002',
 'samples/course2-butterfly-001/flight-002',
 'samples/course2-spring-001/baseline-004',
 'samples/course2-spring-001/constant-stage-001',
 'samples/course2-spring-001/variation-001',
 'samples/course2-spring-001/zigzag-002',
 'samples/course2-spring-001/ribbon-002',
 'samples/course2-spring-001/chain-002',
 'samples/course2-spring-001/external-png-002',
 'samples/course-reproduction-022/final-reconstruction-005',
 'samples/course-reproduction-021/p18-proxy-lines-003',
 'samples/course-reproduction-021/p18-proxy-core-001',
 'samples/course-reproduction-021/p18-proxy-type-001',
 'samples/course-reproduction-021/p18-proxy-lines-originals-001',
 'samples/course-reproduction-020/p17-line-style-003',
 'samples/course-reproduction-020/p17-line-style-variation-002',
 'samples/course-reproduction-019/p17-streak-style-003',
 'samples/course-reproduction-019/p17-streak-style-variation-001',
 'samples/course-reproduction-018/p17-tunnel-001',
 'samples/course-reproduction-018/p17-tunnel-variation-001',
 'samples/course-reproduction-017/p16-style-003',
 'samples/course-reproduction-017/p16-style-variation-001',
 'samples/course-reproduction-016/p16-noise-002',
 'samples/course-reproduction-016/p16-noise-variation-001',
 'samples/course-reproduction-015/p16-core-001',
 'samples/course-reproduction-015/p16-core-variation-001',
 'samples/course-reproduction-014/p15-assembly-003',
 'samples/course-reproduction-014/p15-assembly-variation-001',
 'samples/course-reproduction-013/p15-streaks-001',
 'samples/course-reproduction-013/p15-streaks-variation-001',
 'samples/course-reproduction-012/p15-polar-002',
 'samples/course-reproduction-012/p15-polar-variation-001',
 'samples/course-reproduction-011/p15-radial-002',
 'samples/course-reproduction-011/p15-radial-slow-002',
 'samples/course-reproduction-010/p13-baseline-004',
 'samples/course-reproduction-010/p13-geometry-001',
 'samples/course-reproduction-010/p13-typography-001',
 'samples/course-reproduction-010/p13-texture-001',
 'samples/course-reproduction-009/p14-baseline-002',
 'samples/course-reproduction-009/p14-algorithm-001',
 'samples/course-reproduction-009/p14-motion2026-001',
 'samples/course-reproduction-009/p14-ai-001',
 'samples/course-reproduction-002/p06-final-003',
 'samples/course-reproduction-002/p06-delay5-002',
 'samples/course-generalization-001/geometry',
 'samples/course-generalization-001/typography',
 'samples/course-generalization-001/texture',
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
 'samples/pr-sound-suite-001/baseline-soft-transitions-001',
]
chosen=[]
for name in CASES:
 folder=ROOT/name
 if not folder.is_dir():raise FileNotFoundError(folder)
 for path in folder.rglob('*'):
  if not path.is_file():continue
  rel=path.relative_to(folder)
  if rel.parts[0] in {'inputs','assets'}:
   if path.suffix.lower() in {'.aep','.png','.jpg','.jpeg','.wav','.mp3','.mp4','.mov','.json','.md'}:chosen.append(path)
  elif len(rel.parts)==1 and (path.name in {'project.aep','project.prproj','final.mp4','native-mix.wav','credits.md'} or path.suffix.lower()=='.json'):
   chosen.append(path)
  elif len(rel.parts)==1 and path.name.startswith(('native-still-','native-control-')) and path.suffix.lower()=='.png':
   if folder.name=='p15-radial-002' and path.name not in {'native-still-0.png','native-still-24.png','native-still-120.png','native-still-239.png','native-still-gui-red.png','native-still-gui-green.png','native-still-gui-blue.png'}:continue
   chosen.append(path)
 # Every published demonstration must include both its actual native project and video.
 if not (folder/'final.mp4').is_file() or not any((folder/p).is_file() for p in ['project.aep','project.prproj']):raise ValueError('Incomplete native delivery '+name)
for path in (ROOT/'evaluations').rglob('*'):
 if path.is_file() and path.suffix.lower() in {'.json','.md','.jsx','.py','.txt','.log'} and '__pycache__' not in path.parts:chosen.append(path)
# Some native tracking projects still reference their original generated clips.
# These are necessary inputs, not disposable renders. Read the actual saved
# Adobe dependencies before cleanup instead of guessing from folder names.
supplemental=[]
for name in ['native-media-dependencies.json','pr-media-dependencies.json','native-media-dependencies-p15.json','native-media-dependencies-p15-polar.json','native-media-dependencies-p15-streaks.json','native-media-dependencies-p15-assembly.json','native-media-dependencies-p16-core.json','native-media-dependencies-p16-noise.json','native-media-dependencies-p16-style.json','native-media-dependencies-p17-tunnel.json','native-media-dependencies-p17-streak.json','native-media-dependencies-p17-lines.json','native-media-dependencies-p18-proxies.json','native-media-dependencies-final-reconstruction.json','native-media-dependencies-final-reconstruction-005.json','native-media-dependencies-course2-spring.json','native-media-dependencies-course2-butterfly.json','native-media-dependencies-course2-magnifier.json','native-media-dependencies-course2-scroll.json','native-media-dependencies-course2-rotation-final.json']:
 audit=ROOT/'reports'/name
 if not audit.is_file():continue
 data=json.loads(audit.read_text(encoding='utf-8-sig'))
 if data['status']!='completed':raise ValueError('Native dependency audit incomplete: '+name)
 for project in data['projects']:
  for record in project['media']:
   path=Path(record['path']).resolve()
   if path.suffix.lower() not in {'.mp4','.mov','.wav','.mp3','.aif','.aiff','.png','.jpg','.jpeg'}:continue
   path.relative_to(ROOT.resolve())
   if not path.is_file():raise FileNotFoundError('Required native media missing: '+str(path))
   supplemental.append(path);chosen.append(path)
chosen=sorted(set(chosen))
records=[]
for path in chosen:
 size=path.stat().st_size
 rel=path.relative_to(ROOT).as_posix();is_lfs=False
 if size>=100_000_000 or path.suffix.lower()=='.mov':
  is_lfs=subprocess.check_output(['git','check-attr','filter','--',rel],cwd=ROOT,text=True).strip().endswith(': filter: lfs')
 if size>=100_000_000 and not is_lfs:raise ValueError('GitHub single-file limit requires explicit Git LFS delivery: '+str(path))
 record=dict(path=rel,bytes=size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 if is_lfs:record['storage']='git-lfs'
 records.append(record)
manifest=dict(scope='Standalone video-skills-lab progress snapshot; overall curriculum incomplete',cases=CASES,files=records,
 supplemental_native_media=sorted({p.relative_to(ROOT).as_posix() for p in supplemental}),
 excluded=['tutorial media and frames in cache','local environments and models','duplicate/failed intermediate native binaries','Adobe preset files derived from installed vendor files','Adobe autosave and transport data','repeated native audio/video exports'],
 portability='Native projects retain original Windows media paths. Rebuild from the bundled scripts or relink the bundled inputs/assets; historical report references may point to local-only artifacts.',
 total_selected_bytes=sum(r['bytes'] for r in records))
(ROOT/'reports/git-delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
subprocess.run(['git','add','--','.gitignore','.gitattributes','AGENTS.md','README.md','registry.json','skills','sources','tools','reports'],cwd=ROOT,check=True)
for start in range(0,len(chosen),60):subprocess.run(['git','add','-f','--',*[p.relative_to(ROOT).as_posix() for p in chosen[start:start+60]]],cwd=ROOT,check=True)
print(json.dumps(dict(selected_files=len(chosen),selected_MB=round(manifest['total_selected_bytes']/1048576,2),native_demonstrations=len(CASES)),indent=2))
