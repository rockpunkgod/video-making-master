import json,subprocess,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,'tools');from validate_video import validate
root=Path('samples/pr-pilot-001');config={'width':960,'height':540,'fps':24,'duration':4}
rows=[]
for name in ['baseline','half-gain']:
 q=validate(root/(name+'.mp4'),config);(root/(name+'-quality.json')).write_text(json.dumps(q,indent=2),encoding='utf-8');rows.append(q['status'])
def rms(path):
 b=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ar','48000','-ac','2','-f','f32le','-'],capture_output=True,check=True).stdout
 a=np.frombuffer(b,dtype='<f4').reshape(-1,2);a=a[24000:168000];return float(np.sqrt(np.mean(a.astype(float)**2)))
a=rms(root/'inputs/calibration.wav');b=rms(root/'baseline.mp4');c=rms(root/'half-gain.mp4');difference=float(20*np.log10(c/b));report={'status':'passed' if abs(difference+6.020599913)<.1 and all(x=='passed' for x in rows) else 'failed','input_rms':a,'native_default_rms':b,'native_half_parameter_rms':c,'default_vs_input_db':float(20*np.log10(b/a)),'half_vs_default_db':difference,'expected_db':-6.020599913,'tolerance_db':.1,'method':'decode actual native H264/AAC exports to stereo float PCM; measure stationary interior tone, not parameter readback alone'}
(root/'gain-calibration.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
