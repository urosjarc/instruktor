class Point {

    static radius = 5;

    constructor(x0, y0, vy, vx) {
        this.x = x0;
        this.y = y0;
        this.vy = vy;
        this.vx = vx;
    }

    move(dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
    }
}

class Space {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.impact = false;
        this.width = width;
        this.height = height;
        this.subSpaces = [];
        this.objects = [];
    }

    contains(point) {
        return point.x >= this.x &&
            point.x <= this.x + this.width &&
            point.y >= this.y &&
            point.y <= this.y + this.height;
    }

    buildQuadTrees(level) {
        let w = this.width / 2;
        let h = this.height / 2;

        if (w < Point.radius*2|| h < Point.radius*2){
            if(this.objects.length > 1) this.impact = true;
            return;
        } else if (this.objects.length <= 1) return;

        this.subSpaces.push(new Space(this.x, this.y, w, h));
        this.subSpaces.push(new Space(this.x + w, this.y, w, h));
        this.subSpaces.push(new Space(this.x + w, this.y + h, w, h));
        this.subSpaces.push(new Space(this.x, this.y + h, w, h));

        for (let i in this.objects) {
            for (let j in this.subSpaces) {
                if (this.subSpaces[j].contains(this.objects[i])) {
                    this.subSpaces[j].objects.push(this.objects[i]);
                    break;
                }
            }
        }

        for (let j in this.subSpaces){
            this.subSpaces[j].buildQuadTrees(level + 1);
        }

    }
}

class World extends Space {
    constructor(width, height) {
        super(0, 0, width, height, []);
    }

    populate(objNum) {
        this.objects = [];
        for (let i = 0; i < objNum; i++) {
            let point = new Point(
                randomNum(this.x, this.x + this.width),
                randomNum(this.y, this.y + this.height),
                randomNum(-100, 100),
                randomNum(-100, 100)
            );
            this.objects.push(point);
        }
    }

    moveObjects(dt) {
        for (let i in this.objects) {
            let point = this.objects[i];
            point.move(dt);
            this.checkCollision(point);
        }
    }

    buildQuadTrees() {
        this.subSpaces = [];
        return super.buildQuadTrees(0);
    }

    checkCollision(point) {
        if (this.x > point.x) {
            point.vx *= -1;
            point.x = this.x;
        } else if (this.x + this.width < point.x) {
            point.vx *= -1;
            point.x = this.x + this.width;
        }

        if (this.y > point.y) {
            point.vy *= -1;
            point.y = this.y;
        } else if (this.y + this.height < point.y) {
            point.vy *= -1;
            point.y = this.y + this.height;
        }
    }
}