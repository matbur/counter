/**
 * Created by matbur on 08.12.16.
 */
var tab, slider, n, slider_v;


function setup() {
    createCanvas(400, 400);
    n = 4;
    slider = createSlider(2, 10, n, 1);
    slider_v = n - 1;
    // slider.position(0, 0);
    tab = [];
}

function draw() {
    n = slider.value();
    if (n != slider_v) {
        console.log("v");
        slider_v = n;
        clear();
        tab = [];
        for (let i = 0; i < n; i++) {
            tab.push(new Circle(i, ...n_circle(i, n)));
        }
    }
    for (let i of tab) {
        i.update();
        i.draw();
    }
}

class Circle {
    constructor(i, x, y, r = 20) {
        this.num = i;
        this.x = x;
        this.y = y;
        this.radius = r;
        this.diameter = 2 * r;
        this.left = x - r;
        this.right = x + r;
        this.top = y - r;
        this.bottom = y + r;
        this.over = false;
        this.pressed = false;

    }

    draw() {
        ellipse(this.x, this.y, this.diameter);
        fill(0);
        text(this.num, this.x - 3, this.y + 4);
    }

    isMouseOver() {
        this.over = mouseX > this.left &&
            mouseX < this.right &&
            mouseY > this.top &&
            mouseY < this.bottom;
    }

    isPressed() {
        if (this.over && mouseIsPressed) {
            this.pressed = true;
        } else if (!mouseIsPressed) {
            this.pressed = false;
        }
    }

    update() {
        this.isMouseOver();
        this.isPressed();
        if (this.over || this.pressed) {
            fill(128);
        } else {
            fill(255);
        }
    }
}

function n_circle(i, n) {
    const p = 200;
    const r = 150;
    let alpha = 2 * PI * i / n;
    return [p - r * cos(alpha), p + r * sin(alpha)];
}