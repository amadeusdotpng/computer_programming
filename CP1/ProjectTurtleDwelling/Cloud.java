public class Cloud extends Thread {
    double x, y;
    public Cloud(double x_, double y_) {
        x = x_;
        y = y_;
    }

    public void run() {
        Turtle t = new Turtle();
        t.up();
        t.hide();
        t.speed(500);
        t.shape("./cloud.png");
        t.shapeSize(150,65);
        t.show();
        t.setPosition(x,y);

    }
}
