import json,subprocess
from pathlib import Path
import numpy as np
p=Path('samples/pr-pilot-001');b=subprocess.run(['ffmpeg','-v','error','-i',str(p/'keyframe-calibration.mp4'),'-vn','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True,check=True).stdout;a=np.frombuffer(b,dtype='<f4').reshape(-1,2).astype(float);base=json.loads((p/'gain-calibration.json').read_text())['native_default_rms'];windows=[]
for start,end,expected in [(0.1,.8,None),(1.1,1.4,0),(1.8,2.2,-6.020599913),(2.7,3.5,-12.041199826)]:
 rms=float(np.sqrt(np.mean(a[int(start*48000):int(end*48000)]**2)));db=float(20*np.log10(max(rms,1e-12)/base));windows.append({'start':start,'end':end,'measured_db':db,'expected_db':expected,'passed':rms<1e-4 if expected is None else abs(db-expected)<.15})
report={'status':'passed' if all(w['passed'] for w in windows) else 'failed','finding':'Native volume keys are referenced to source time for this clip with source in=0; sequence start is 1 second','windows':windows};(p/'keyframe-calibration.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
