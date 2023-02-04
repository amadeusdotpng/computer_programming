import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Drawing {
	public static void main(String[] args) {
		JFrame frame = new JFrame("Drawing");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		MyPanel panel = new MyPanel();
		panel.setPreferredSize(new Dimension(600, 600));
		panel.addMouseMotionListener(panel);
		frame.add(panel);

		frame.pack();
		frame.setVisible(true);
	}
}

class MyPanel extends JPanel implements MouseMotionListener {
	int x = 0;
	int y = 0;
	protected void paintComponent(Graphics g) {
		g.setColor(new Color(15,15,15));
		g.fillRect(0,0,getWidth(), getHeight());
		g.setColor(new Color(0,0,255));
		g.fillOval(x-50, y-50, 100, 100);
		g.fillOval(-x-50+getWidth(), -y-50+getHeight(), 100, 100);
		g.fillOval(x-50, -y-50+getHeight(), 100, 100);
		g.fillOval(-x-50+getWidth(), y-50, 100, 100);
	}
	
	public void mouseMoved(MouseEvent e) {
		x = e.getX();
		y = e.getY();
		System.out.printf("%d, %d\n", x, y);
		repaint();
	}

	public void mouseDragged(MouseEvent e) {

	}
}
