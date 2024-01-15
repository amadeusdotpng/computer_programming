import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.image.*;
import javax.imageio.*;
import java.io.*;

public class Scene {
	public static void main(String[] args) {
		JFrame frame = new JFrame("Drawing");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		MyPanel panel = new MyPanel();
		panel.setPreferredSize(new Dimension(1240, 920));
		panel.setOpaque(false);
		panel.addMouseMotionListener(panel);
		frame.add(panel);

		frame.pack();
		frame.setVisible(true); 
	}
}

class MyPanel extends JPanel implements MouseMotionListener {
	private int mouseX = 0;
	private int mouseY = 0;

	private String[][] skyColors = {{"#AA6992", "#EDAE98", "#F5D8BA", "#F4EDD4", "#96BFC3", "#488AB5"},
									{"#32334D", "#5A3E49", "#834945", "#AB5F43", "#FC984C", "#FC6A38"},
									{"#070B34", "#141852", "#2B2F77", "#483475", "#6B4984", "#855988"}};

	private BufferedImage ocean;
	private BufferedImage island;
	private BufferedImage sun;
	private BufferedImage ship;
	private BufferedImage cloud0;
	private BufferedImage cloud1;

	protected void paintComponent(Graphics g) {
		/* Setup */
		Graphics2D g2 = (Graphics2D)g;
		setImages();

		int horizon = getHeight()-ocean.getHeight();
		
		/* Background */
		for(int i = 0; i < skyColors[0].length-1; i++) {
			int skyHeight = (horizon+5)/5;
			int reflectionHeight = ocean.getHeight()/5;
			
			double interpolation; 
			Color skyC1, skyC2, reflectionC1, reflectionC2;
			
			if(mouseY < horizon) {	// Day Time
				interpolation = Math.min(Math.max((double)mouseY/horizon, 0), 1);
				skyC1 = lerpColor(skyColors[0][i], skyColors[1][i], interpolation);
				skyC2 = lerpColor(skyColors[0][i+1], skyColors[1][i+1], interpolation);
				reflectionC1 = lerpColor(skyColors[0][5-i], skyColors[1][5-i], interpolation);
				reflectionC2 = lerpColor(skyColors[0][5-(i+1)], skyColors[1][5-(i+1)], interpolation);
			} else {	// Night Time
				interpolation = Math.min(Math.max((double)(mouseY-horizon)/(getHeight()-horizon), 0), 1);
				skyC1 = lerpColor(skyColors[1][i], skyColors[2][i], interpolation);
				skyC2 = lerpColor(skyColors[1][i+1], skyColors[2][i+1], interpolation);
				reflectionC1 = lerpColor(skyColors[1][5-i], skyColors[2][5-i], interpolation);
				reflectionC2 = lerpColor(skyColors[1][5-(i+1)], skyColors[2][5-(i+1)], interpolation);
			}
			
			drawVertGradientRect(skyC1, skyC2, 0, i*skyHeight, getWidth(), skyHeight, g2);
			drawVertGradientRect(reflectionC1, reflectionC2, 0, horizon+i*reflectionHeight, getWidth(), reflectionHeight, g2);	
		}

		/* Sun */
		int sunX = mouseX - sun.getWidth()/2;
		int sunY = mouseY - sun.getHeight()/2;

		if(mouseY+(sun.getHeight()/2) > horizon) {
			sun = sun.getSubimage(0,0, sun.getWidth(), Math.max(horizon-sunY, 1));
		}

		if(mouseY <= horizon+50) {
			g2.drawImage(sun, sunX, sunY, this);
		}

		/* Ocean */
		g2.drawImage(ocean, 0, horizon, this);
		g2.drawImage(ocean, ocean.getWidth()*2, (getHeight()-ocean.getHeight()), -ocean.getWidth(), ocean.getHeight(), this);
		
		/* Stuff */
		g2.drawImage(island, 250, horizon-100, this);
		g2.drawImage(ship, 720, horizon-175, this);
		g2.drawImage(cloud0, 0, horizon-320, this);
		g2.drawImage(cloud1, getWidth()-(cloud1.getWidth()+240), horizon-420, this);
	}

	private void drawVertGradientRect(Color top, Color bot, int x, int y, int width, int height, Graphics2D g2) {
		g2.setPaint(new GradientPaint(0, y, top, 0, y+height, bot));
		g2.fill(new Rectangle(x, y, width, height));
	}

	private Color lerpColor(String h1, String h2, double interpolation) {
		Color c1 = Color.decode(h1);
		Color c2 = Color.decode(h2);
		double inverse_interp = 1-interpolation;

		float r = (float)(c1.getRed() * inverse_interp + c2.getRed() * interpolation);
		float g = (float)(c1.getGreen() * inverse_interp + c2.getGreen() * interpolation);
		float b = (float)(c1.getBlue() * inverse_interp + c2.getBlue() * interpolation);
		return new Color(r/255, g/255, b/255);
	}

	private void setImages() {
		try {
			ocean = ImageIO.read(new File("./pics/ocean.png"));
			island = ImageIO.read(new File("./pics/islandSmall.png"));
			sun = ImageIO.read(new File("./pics/sun.png"));
			ship = ImageIO.read(new File("./pics/ship.png"));
			cloud0 = ImageIO.read(new File("./pics/cloud0.png"));
			cloud1 = ImageIO.read(new File("./pics/cloud1.png"));
		} catch(IOException e) {
			System.out.println(e);
		}
	}

	public void mouseMoved(MouseEvent e) {
		/* Move Sun */
		mouseX = e.getX();
		mouseY = e.getY();
		repaint();
	}

	public void mouseDragged(MouseEvent e) {
		// Nothing
	}
}
