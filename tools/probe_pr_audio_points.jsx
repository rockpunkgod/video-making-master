(function(){var c=app.project.activeSequence.audioTracks[0].clips[0];
function t(s){var v=new Time();v.seconds=s;return v;}
c.start=t(.7);c.inPoint=t(0);c.outPoint=t(4.0995);c.end=t(4.7995);
return {status:'precise_audio_points_probe',start:c.start.seconds,end:c.end.seconds,in_point:c.inPoint.seconds,out_point:c.outPoint.seconds,duration:c.duration.seconds};
}());
