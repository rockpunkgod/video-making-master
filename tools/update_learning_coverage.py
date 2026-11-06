import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'sources/videos.json';data=json.loads(path.read_text(encoding='utf-8'))
records={
'U19f1A1ooFE':{'global':'reviewed 24 global frames and original English automatic captions queried','detail':'13 technical cue frames reviewed; four expression mechanisms identified','abstraction':'merge index distribution with procedural arrays; other variants pending native testing'},
'wiISCTB4s1Y':{'global':'8 global frames reviewed and original English automatic captions queried','detail':'8 technical cue frames reviewed; source-only native error 0.27px distinguished from local results','abstraction':'native solve, observed three-point plane creation and independent drift checks implemented; three original synthetic input scenes verified, real footage pending'},
'PbVB52WCUDE':{'global':'18 frames across full range reviewed; chapter structure extracted','detail':'pending; exact parameters and operations not fully extracted','abstraction':'separate projection geometry, model conversion and reflective surfaces; dependency not available'},
'BV1xP411C7u3':{'global':'18 frames reviewed; Mocha Pro and mesh replacement identified','detail':'pending; several source UI sections appear blank','abstraction':'PowerMesh is distinct from Mocha AE; plugin missing'},
'BV1aK4y1U7Xv':{'global':'18 frames reviewed; vanishing point, separation and camera move identified','detail':'pending','abstraction':'photo reconstruction variant shares projection principles with V5; version differences retained'},
'BV1qb4y1x7h1':{'global':'18 frames reviewed; screen plane and hand occlusion layers identified','detail':'pending','abstraction':'combine with downstream keying/removal lesson'},
'BV1Pu411Q7DB':{'global':'18 frames reviewed; keying, replacement and marker removal identified','detail':'pending','abstraction':'combine with upstream planar tracking lesson'},
'OagnZAD_9wY':{'global':'18 full-range frames reviewed; native English automatic captions queried','detail':'6 cue frames reviewed around volume automation, reverb, pitch shifter, lowpass and breathing; no independent audio audition','abstraction':'combine event, ambience and narrative layers in one sound skill; PR execution pending'},
'KECzwyUursc':{'global':'18 full-range frames reviewed; audio metadata en-US but default captions ar; additional English Watch transcript requested explicitly','detail':'multitrack grouping visible at 03:15 and 05:41; no exact processing parameters verified','abstraction':'merge ambience and transitions with cinematic sound skill, not a separate tool'},
'vA5yAFOo_K8':{'global':'18 full-range frames reviewed; native Hindi captions available but not fully checked','detail':'curves and reference color blocks identified; exact curve points and color-management settings pending','abstraction':'reference-based curve styling candidate; PR host execution pending'}
}
for entry in data['videos']:
    if entry['id'] in records:
        entry['status']='partially_analyzed';entry['passes']=records[entry['id']]
        for ingest in entry.get('ingestion',[]):ingest['stage']='global_frames_reviewed_detail_pending';ingest['frames_reviewed']=True
path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
print('Coverage updated from reviewed evidence; no entire-course completion claimed.')
