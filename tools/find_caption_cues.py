"""Query existing Watch caption evidence; delegates VTT parsing to Watch."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,'D:/Codex/skills/watch/scripts')
from transcribe import parse_vtt

ap=argparse.ArgumentParser();ap.add_argument('vtt',type=Path);ap.add_argument('--terms',default='poster,loop,wiggle,random,seed,value');ap.add_argument('--start',type=float,default=0);ap.add_argument('--end',type=float,default=100000);ap.add_argument('--limit',type=int,default=60)
a=ap.parse_args();terms=a.terms.lower().split(',');last=-100;count=0
for cue in parse_vtt(str(a.vtt)):
    t=cue['start'];text=cue['text']
    if a.start<=t<=a.end and t-last>=4 and any(term in text.lower() for term in terms):
        print(f'{int(t)//60:02}:{int(t)%60:02} {text}');last=t;count+=1
        if count>=a.limit:break
