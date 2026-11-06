(function(){
return {version:app.version,project_items:app.project.rootItem.children.numItems,sequences:app.project.sequences.numSequences,
saveAs:typeof app.project.saveAs,importFiles:typeof app.project.importFiles,createNewSequenceFromClips:typeof app.project.createNewSequenceFromClips,openDocument:typeof app.openDocument};
}());
