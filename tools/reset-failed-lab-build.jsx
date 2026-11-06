(function(){
var p=app.project,comp=null,valid=true;
for(var i=1;i<=p.numItems;i++){var item=p.item(i);if(item instanceof CompItem){if(item.name!=='square-baseline')valid=false;else comp=item;}}
if(!valid||!comp||comp.numLayers!==26||!comp.layer('LAB_CONTROLS')||!comp.layer('LAB_CAMERA'))throw Error('Unexpected project; refusing reset');
p.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.newProject();
}());
