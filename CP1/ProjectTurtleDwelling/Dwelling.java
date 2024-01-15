public class Dwelling extends Thread {
    @Override
    public void run() {
        Turtle t = new Turtle();
        t.up();
        t.hide();
        t.speed(500);
        t.shape("./house.png");
        t.show();
        t.setPosition(-400,-70);

    }
}
