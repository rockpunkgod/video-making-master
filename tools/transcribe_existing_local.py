"""Timestamp export adapter for an already installed faster-whisper and local model.

No installer, model downloader, network ASR, or alternative speech recognition engine.
Run with the caller's existing Python environment containing faster-whisper.
"""
import argparse,json,os,subprocess,time
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('media',type=Path);ap.add_argument('--model',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--language',default='zh');ap.add_argument('--start',type=float,default=0);ap.add_argument('--duration',type=float,required=True);a=ap.parse_args()
if not a.media.is_file() or not all((a.model/f).is_file() for f in ['model.bin','config.json','tokenizer.json']):raise FileNotFoundError('Existing media and complete local model required; no downloads permitted')
if a.start<0 or a.duration<=0:raise ValueError('Invalid audio interval')
if a.out.exists():raise FileExistsError('Fresh evidence directory required')
a.out.mkdir(parents=True)
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
wav=a.out/'input.wav'
subprocess.run(['ffmpeg','-v','error','-n','-ss',str(a.start),'-i',str(a.media.resolve()),'-t',str(a.duration),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)],check=True)
from faster_whisper import WhisperModel
began=time.monotonic();print('Loading existing local model; network access disabled for model loading.',flush=True)
model=WhisperModel(str(a.model.resolve()),device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
segments,info=model.transcribe(str(wav),language=a.language,beam_size=5,vad_filter=False,condition_on_previous_text=False)
rows=[]
for s in segments:
    row={'start':s.start+a.start,'end':s.end+a.start,'text':s.text.strip(),'average_log_probability':s.avg_logprob,'no_speech_probability':s.no_speech_prob};rows.append(row)
    print(json.dumps(row,ensure_ascii=True),flush=True)
def stamp(seconds):
    ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(a.out/'transcript.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}" for i,r in enumerate(rows))+'\n',encoding='utf-8')
result={'status':'transcribed_accuracy_unverified','backend':'existing faster-whisper','model_path':str(a.model.resolve()),'model_loading_local_only':True,'audio_uploaded':False,'source':str(a.media.resolve()),'interval_start':a.start,'interval_duration':a.duration,'language_hint':a.language,'reported_language':info.language,'elapsed_seconds':time.monotonic()-began,'segments':rows,'evidence_note':'Automatic speech transcription is not visual evidence or a human accuracy review.'}
(a.out/'transcript.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('Saved timestamped local transcript.',flush=True)
