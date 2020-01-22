let canvas = new Canvas("world");
let world = new World(canvas.width, canvas.height);
let drawWeb = true;


initWorld();
setInterval(() => {
    canvas.clear();
    canvas.drawWorld(world);
    canvas.drawWorldSpaces(world, drawWeb);
    world.moveObjects(0.01);
    world.buildQuadTrees();
}, 1 / 60 * 1000);

function initWorld(){
    let numPoints = document.getElementById("numPoints").value;
    world.populate(numPoints);
}
function toggleWeb() {
    drawWeb = !drawWeb;
}