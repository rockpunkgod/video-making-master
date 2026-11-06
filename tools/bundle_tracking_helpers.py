from pathlib import Path
import shutil
root=Path('.').resolve();dst=root/'skills/after-effects/ae-camera-tracking/scripts'
for name in ['run_ae.py','render_ae.py','validate_video.py','measure_tracking_drift.py','capture_native_window.ps1','create_tracked_solid_gui.ps1']:
 shutil.copy2(root/'tools'/name,dst/name)
text=(root/'tools/prepare_tracking_composite.py').read_text(encoding='utf-8')
text=text.replace("ROOT=Path(__file__).resolve().parents[1]","ROOT=Path(__file__).resolve().parent")
text=text.replace("default=ROOT/'samples/tracking-fixture-001'","required=True").replace("default=ROOT/'samples/fixtures/geometry.png'","required=True")
old="template=(ROOT/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_text(encoding='utf-8')\nencoder=template[template.index('    function encode'):template.index('    function write')]"
assert old in text
text=text.replace(old,"encoder=(ROOT/'json-encode.jsx').read_text(encoding='utf-8')")
(dst/'prepare_composite.py').write_text(text,encoding='utf-8')
t=(root/'skills/after-effects/ae-procedural-motion/scripts/template.jsx').read_text(encoding='utf-8');(dst/'json-encode.jsx').write_text(t[t.index('    function encode'):t.index('    function write')],encoding='utf-8')
p=dst/'create_tracked_solid_gui.ps1';text=p.read_text(encoding='utf-8');text=text.replace("param([int]$ProcessId,","param([Parameter(Mandatory=$true)][string]$ProjectPath,[int]$ProcessId,");needle="if($title.ToString() -notlike '*tracking-attempt.aep*')";text=text.replace(needle,"$expectedPath=[System.IO.Path]::GetFullPath($ProjectPath)\nif(!$title.ToString().Contains($expectedPath) -or $title.ToString() -notlike '*tracking-attempt.aep*')");p.write_text(text,encoding='utf-8')
print('Copied reviewed lab helpers; local serializer and required explicit assets remove repo-relative runtime dependencies.')
