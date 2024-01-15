public class Ground extends Thread {

    @Override
    public void run() {
        Turtle t = new Turtle();
        t.hide();
        t.up();
		t.setPosition(-640,-160);
		t.penColor("Green");

		t.down();
		
		for(int i = 0; i < 200; i++) {
			t.speed(5);
			t.forward(1280);
			t.up();
			t.speed(0);
			t.setPosition(-640, -160-i);
			t.down();
		}
    }
}
