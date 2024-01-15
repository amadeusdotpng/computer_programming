import javax.sound.sampled.*;

public class ArrayAnimation
{
	public static void sleep(int fps)
	{
			try
			{
				Thread.sleep(1000/fps);
			}
			catch(Exception e){}
			
	}
	
	public static void playFrequency(double frequency, int durationMillis) {
        try {
            int sampleRate = 44100;
            int bufferSize = sampleRate * durationMillis / 1000;
            byte[] buffer = new byte[bufferSize];
            AudioFormat format = new AudioFormat(sampleRate, 8, 1, true, false);
            SourceDataLine dataLine = AudioSystem.getSourceDataLine(format);
            dataLine.open(format, bufferSize);
            dataLine.start();

            for (int i = 0; i < bufferSize; i++) {
                double angle = 2.0 * Math.PI * i * frequency / format.getSampleRate();
                buffer[i] = (byte) (Math.sin(angle) * 127.0);
            }

            dataLine.write(buffer, 0, bufferSize);
            dataLine.drain();
            dataLine.close();
        } catch (LineUnavailableException ex) {
            System.err.println("Error playing frequency: " + ex.getMessage());
        }
    }
	
	public static void shuffle(int[] nums)
	{
		for(int i=0;i<nums.length;i++)
		{
			int j=(int)(Math.random()*(nums.length-i)+i);
			int temp=nums[i];
			nums[i]=nums[j];
			nums[j]=temp;
		}
	}
	
	public static int[] getArray(int n)
	{
		int[] nums=new int[n];
		for(int i=0;i<n;i++) nums[i]=i+1;
		return nums;
	}
	
	public static boolean isSorted(int[] nums)
	{
		for(int i=0;i<nums.length-1;i++) 
			if (nums[i]>nums[i+1])
				return false;
		return true;
	}
	
	public static void bubbleSort(int[] arr) {
        int n = arr.length;
        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap arr[j] and arr[j + 1]
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                    ArrayDisplay.show(arr,j,j+1);
                    //~ playFrequency(440*Math.pow(2,arr[j]/12.0),1000);
                    sleep(20);
                }
            }
            // If no two elements were swapped in the inner loop, the array is already sorted
            if (!swapped) {
                break;
            }
        }
    }
    public static void quickSort(int[] nums)
    {
		quickSort(nums, 0, nums.length - 1);
	}
    public static void quickSort(int[] array, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(array, low, high);
            quickSort(array, low, pivotIndex - 1);
            quickSort(array, pivotIndex + 1, high);
        }
    }

    private static int partition(int[] nums, int low, int high) {
        int pivot = nums[high];
        int i=low;
        int j=high;
        while(i<j)
        {
			if(nums[i]<pivot)i++;
			else if(nums[j]>pivot)j--;
			else swap(nums,i,j);
		
			ArrayDisplay.show(nums,i,j);
			sleep(10);
		}
		//~ ArrayDisplay.shadeIndex(i,gray);
		return i;
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    
    
    
	
	public static void main(String[] args)
	{
		int[] nums=getArray(32);
		shuffle(nums);
		ArrayDisplay.show(nums);
		sleep(10);
		quickSort(nums);
		ArrayDisplay.show(nums);
		ArrayDisplay.reset();
		//~ while(!isSorted(nums))
		//~ {
			//~ ArrayDisplay.show(nums);
			//~ shuffle(nums);
			//~ sleep();
		//~ }
	}	
}

