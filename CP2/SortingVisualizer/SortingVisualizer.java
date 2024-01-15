import java.awt.*;
import javax.swing.*;
import java.util.HashMap;

public class SortingVisualizer {
	public static void main(String[] args) {
		int w = Toolkit.getDefaultToolkit().getScreenSize().width;
		System.out.println(w);
		int[] list = generateArray(1728);
		Visualizer.updateArray(list);
		Helper.sleep(1);

		Visualizer.updateTitle("Shuffling");
		Helper.shuffle(list, 720, true);
		Helper.sleep(1);

		Visualizer.updateTitle("QuickSort");
		QuickSort.sort(list);
		Helper.sleep(1);

		Visualizer.updateTitle("Shuffling");
		Helper.shuffle(list, 720, true);
		Helper.sleep(1);

		Visualizer.updateTitle("HeapSort");
		HeapSort.sort(list);
		Helper.sleep(1);
	
		list = generateArray(w/4);
		Visualizer.updateArray(list);
		Helper.sleep(1);

		Visualizer.updateTitle("Shuffling");
		Helper.shuffle(list, 540, true);
		Helper.sleep(1);

		Visualizer.updateTitle("Sorting Visualizer");
		while(true) {
			Helper.shuffle(list, 1, false);
			Visualizer.updateArray(list);
			Helper.sleep(5);
		}
	}

	public static int[] generateArray(int n) {
		int[] list = new int[n];
		for(int i = 0; i < n; i++) {
			list[i] = i+1;
		}
		return list;
	}

	
}

class QuickSort {
	public static void sort(int[] arr) {
		quickSort(arr, 0, arr.length-1);
	}

	public static void quickSort(int[] array, int low, int high) {
		if(low < high) {
			int pivotIndex = partition(array, low, high);
			quickSort(array, low, pivotIndex - 1);
			quickSort(array, pivotIndex + 1, high);
		}
		Visualizer.resetIndices();
	}

	private static int partition(int[] array, int low, int high) {
		int pivot = array[high];
		int i = low;
		int j = high;
		Visualizer.updatePartition(pivot);
		while(i < j) {
			if(array[i]<pivot)
				i++;
			else if(array[j]>pivot)
				j--;
			else Helper.swap(array, i, j);
			Visualizer.updateComparison(i, j);
			Visualizer.updateArray(array);
			Helper.sleep(540);
		}
		return i;
	}

}
class HeapSort {
	public static void sort(int[] arr) {
		buildMaxHeap(arr, arr.length-1);
		int end = arr.length-1;
		while(end > 0) {
			Visualizer.updatePartition(0);
			Helper.swap(arr, 0, end);
			end--;
			siftDown(arr, 0, end);
		}
		Visualizer.resetIndices();
	}

	private static void buildMaxHeap(int[] array, int count) {
		int start = (count-1)/2;

		while(start >= 0) {
			siftDown(array, start, count-1);
			start--;
		}
		Visualizer.resetIndices();
	}

	private static void siftDown(int[] array, int start, int end) {
		int root = start;
		while(root*2+1 <= end) {
			int leftChildIndex  = root*2+1;
			int rightChildIndex = root*2+2;
			int swap = root;

			if(array[swap] < array[leftChildIndex])
				swap = leftChildIndex;

			if(rightChildIndex <= end && array[swap] < array[rightChildIndex])
				swap = rightChildIndex;

			Visualizer.updateComparison(swap, root);
			if(swap == root)
				return;
			else {
				Helper.swap(array, swap, root);
				root = swap;
			}
			Visualizer.updateArray(array);
			Helper.sleep(540);
		}
	}
}

class Visualizer extends JPanel {
	private static int[] data;
	private static JFrame frame;
	private static int comparisonIndex0 = -1;
	private static int comparisonIndex1 = -1;
	private static int partitionIndex = -1;
	
	public static void setup() {
		Visualizer sortVisualization = new Visualizer();

		frame = new JFrame("Sorting Visualizer");
		frame.add(sortVisualization);
		frame.setExtendedState(JFrame.MAXIMIZED_BOTH); 
	}

	public static void updateArray(int[] newArray) {
		if(frame==null)
			setup();
		data = newArray;
		frame.setVisible(true);
		frame.repaint();
	}

	public static void updateComparison(int index0, int index1) {
		if(frame==null)
			setup();
		comparisonIndex0 = index0;
		comparisonIndex1 = index1;
		frame.setVisible(true);
		frame.repaint();
	}

	public static void updatePartition(int index) {
		if(frame==null)
			setup();
		partitionIndex = index;
		frame.setVisible(true);
		frame.repaint();
	}

	public static void resetIndices() {
		if(frame==null)
			setup();
		comparisonIndex0 = -1;
		comparisonIndex1 = -1;
		partitionIndex = -1;
		frame.setVisible(true);
		frame.repaint();
	}

	public static void updateTitle(String title) {
		frame.setTitle(title);
	}

	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g);
		g.setColor(Color.BLACK);
		g.fillRect(0,0,getWidth(), getHeight());

		double width = getWidth() / data.length;
		int maxHeight = 0;

		for(int num : data)
			maxHeight = Math.max(maxHeight, num);

		for (int i = 0; i < data.length; i++) {
			int barHeight = (int)((double) data[i] / (double)(maxHeight) * (getHeight()-width*5.0/10.0));
			int X = (int)(i * width);
			int Y = (int)(getHeight() - barHeight);
			if(i == comparisonIndex0 || i == comparisonIndex1) {
				drawBar(g, X, Y, (int)(width*10.0/10.0), barHeight, Color.RED);
			}
			else if(i == partitionIndex) {
				drawBar(g, X, Y, (int)(width*10.0/10.0), barHeight, Color.BLUE);
			} else {
				drawBar(g, X, Y, (int)(width*10.0/10.0), barHeight, Color.WHITE);
			}
		}
	}

	private static void drawBar(Graphics g, int X, int Y, int width, int height, Color color) {
		g.setColor(color);
		g.fillRect(X, Y, width, height);
	}
}

class Helper {
	public static void sleep(double fps) {
		try {
			Thread.sleep((int)(1000.0/fps));
		} catch(Exception e) {}
	}
	public static void swap(int[] array, int i, int j) {
		int tmp = array[i];
		array[i] = array[j];
		array[j] = tmp;
	}

	public static void shuffle(int[] nums, double fps, boolean show) {
		for(int i = 0; i < nums.length; i++) {
			int j=(int)(Math.random() * (nums.length-i)+i);
			int temp=nums[i];
			nums[i]=nums[j];
			nums[j]=temp;
			if(show) {
				Visualizer.updateArray(nums);
				Helper.sleep(fps);
			}
		}
	}
}
