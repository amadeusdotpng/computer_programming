import java.awt.Color;

public class Sun extends Thread {
    
    @Override
    public void run() {
        Color sunColor = Color.decode("#FC984C");
        
        Turtle t = new Turtle();
        t.hide();
        t.up();
        t.penColor(sunColor);

        t.speed(0);
        t.up();
        t.setPosition(0, -160);
        t.speed(1000);
        t.dot(sunColor, 300);

        t.speed(100);
        t.face(1,-160);
        for(int i = 0; i < 7; i++) {
            t.up();
            t.setPosition(0, -160);
            t.left(22.5);
            t.forward(200);
            t.down();
            t.forward(100);
        }
        
        
        
    }
}
