public class Dweller extends Thread{
    @Override
    public void run() {
        Turtle t = new Turtle(0,-160);
        t.up();
        t.hide();
        t.shape("./sadlain.png");
        t.shapeSize(91,100);
        t.speed(1500);
        t.show();
        t.setPosition(-300, -160);

    }
}
