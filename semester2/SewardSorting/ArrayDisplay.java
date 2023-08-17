import java.awt.*;
import javax.swing.*;

public class ArrayDisplay extends JPanel {
    private static int[] data;
    private static JFrame frame; 
    private static int highlightIndex1=-1;
    private static int highlightIndex2=-1;

	
    
    public static void setup()
    {

        ArrayDisplay barVisualization = new ArrayDisplay();
        frame = new JFrame("Bar Visualization");
        //~ frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(barVisualization);
        frame.setSize(800, 600);
        frame.setLocationRelativeTo(null);
        
	}

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        double width = 1.0*getWidth() / data.length;
        int maxHeight = 0;
        for(int num:data)maxHeight=Math.max(maxHeight,num);

        for (int i = 0; i < data.length; i++) {
            int barHeight = (int) ((double) data[i] / (double) maxHeight * getHeight());
            if(i!=highlightIndex1 && i!=highlightIndex2) g.setColor(Color.BLUE);
            else g.setColor(Color.ORANGE);
            g.fillRect((int)(i * width+width/10), getHeight() - barHeight, (int)(width*8/10 - 1), barHeight);
        }
    }
    
    public static void show(int[] array)
    {
		if(frame==null)setup();
		highlightIndex1=-1;
		highlightIndex2=-1;
		data=array;
		frame.setVisible(true);
		frame.repaint();
	}
    
    public static void show(int[] array, int highlightIndex1, int highlightIndex2 )
    {
		ArrayDisplay.highlightIndex1=highlightIndex1;
		ArrayDisplay.highlightIndex2=highlightIndex2;
		if(frame==null)setup();
		data=array;
		frame.setVisible(true);
		frame.repaint();
	}
    
 

    public static void main(String[] args) {
        
    }
}



