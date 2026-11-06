(function(){
var s=app.project.activeSequence,rows=[];
for(var i=0;i<s.audioTracks.numTracks;i++)for(var j=0;j<s.audioTracks[i].clips.numItems;j++){
 var c=s.audioTracks[i].clips[j];var before=c.start.seconds;var t=new Time();t.seconds=.7;c.start=t;
 rows.push({track:i,clip:j,start_before:before,start_after:c.start.seconds,end:c.end.seconds,in_point:c.inPoint.seconds,out_point:c.outPoint.seconds});
}
return {status:'timing_probe_on_failed_lab_case',rows:rows};
}());
