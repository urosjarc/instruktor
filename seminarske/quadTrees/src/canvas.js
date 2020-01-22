
class Canvas {
    constructor(canvasID){
        this.dom = document.getElementById(canvasID);
        this.ctx = this.dom.getContext("2d");
        this.width = null;
        this.height = null;

        this.init();
    }

    init(){
        let size = htmlContentSize(this.dom);
        this.width = size.width;
        this.height = size.height;
    }

    drawWorld(world){
        let self = this;
        world.objects.forEach(obj => {
            self.ctx.beginPath();
            self.ctx.arc(obj.x, obj.y, Point.radius, 0, 2*Math.PI);
            self.ctx.stroke();
        });
    }

    drawWorldSpaces(space, drawWeb){
        let self = this;

        for(let i in space.subSpaces){
            let obj = space.subSpaces[i];

            if(drawWeb)
                self.ctx.strokeRect(obj.x, obj.y, obj.width, obj.height);

            if(obj.impact === true){
                for(let j in obj.objects){
                    let point = obj.objects[j];
                    self.ctx.fillStyle = "red";
                    self.ctx.beginPath();
                    self.ctx.arc(point.x, point.y, Point.radius, 0, 2 * Math.PI);
                    self.ctx.fill();
                }
                return;
            }
            self.drawWorldSpaces(obj, drawWeb);
        }

    }

    clear(){
        this.ctx.clearRect(0, 0, this.width, this.height);
    }
}


