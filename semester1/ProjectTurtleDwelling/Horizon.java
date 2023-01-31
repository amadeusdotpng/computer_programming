import java.awt.Color;

public class Horizon extends Thread {

    @Override
    public void run() {
        Color[] colors = {Color.decode("#32334D"), Color.decode("#5A3E49"), Color.decode("#834945"), Color.decode("#AB5F43"), Color.decode("#FC6A38")};

        Turtle t = new Turtle();
        t.hide();
        t.up();
		t.setPosition(-640,360);

        t.down();
		
        for(int i=0; i < 5; i++) {
            t.penColor(colors[i]);
            for(int j=0; j < 104; j++) {
                t.speed(5);
			    t.forward(1280);
			    t.up();
			    t.speed(0);
			    t.setPosition(-640, t.getY()-1);
			    t.down();
            }
        }
		
		
    }
    
}
