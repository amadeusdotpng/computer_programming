import java.util.Arrays;
public class SortingBenchmark {
    public static void main(String[] args) {
        System.out.println("Array Length,"+
                            "Bubble Time, Bubble Swaps, Bubble Compares,"+
                            "Selection Time, Selection Swaps, Selection Compares,"+
                            "Insertion Time, Insertion Swaps, Insertion Compares,"+
                            "QuickSort Time, QuickSort Swaps, QuickSort Compares,"+
                            "Standard Java Array Sort");
        int[] a = {6,2,4,3,1};
        BenchmarkResults insertion = insertionSort(a);
        System.out.print(insertion.swaps);
    }

    public static void benchmark(int length) {
        int[] testArray = createRandomArray(length);
        long start;
        long end;

        // Bubble Sort
        start = System.nanoTime();
        BenchmarkResults bubble = bubbleSort(testArray.clone());
        end = System.nanoTime();
        bubble.setTime(end-start);

        // Selection Sort
        start = System.nanoTime();
        BenchmarkResults selection = selectionSort(testArray.clone());
        end = System.nanoTime();
        selection.setTime(end-start);

        // Insertion Sort
        start = System.nanoTime();
        BenchmarkResults insertion = insertionSort(testArray.clone());
        end = System.nanoTime();
        insertion.setTime(end-start);

        // Quick Sort
        start = System.nanoTime();
        BenchmarkResults quickSort = quickSort(testArray.clone(), 0, length-1);
        end = System.nanoTime();
        quickSort.setTime(end-start);
        
        // Java Sort
        start = System.nanoTime();
        Arrays.sort(testArray.clone());
        end = System.nanoTime();

        long javaSortTime = end-start;
        // length, bubble time, swaps, compares, selection time, swaps, compares, insertion time, swaps, compares, qsort time, swaps, compares, java sort time
        System.out.printf("%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%f\n", length,
                        (double)bubble.time/1000000.0, bubble.swaps, bubble.compares,
                        (double)selection.time/1000000.0, selection.swaps, selection.compares,
                        (double)insertion.time/1000000.0, insertion.swaps, insertion.compares,
                        (double)quickSort.time/1000000.0, quickSort.swaps, quickSort.compares,
                        (double)javaSortTime/1000000.0);
    }

    public static int[] createRandomArray(int length) {
        int[] a = new int[length];
        for(int i = 0; i < length; i++) {
            a[i] = (int)(Math.random()*length+1);
        }
        return a;
    }

    public static void swap(int[] a, int index1, int index2) {
        int temp = a[index1];
        a[index1] = a[index2];
        a[index2] = temp;
    }

    // https://en.wikipedia.org/wiki/Bubble_sort#Pseudocode_implementation
    public static BenchmarkResults bubbleSort(int[] a) {
        long swaps = 0;
        long compares = 0;
        boolean swapped;

        while(true) {
            swapped = false;
            for(int j = 0; j < a.length-1; j++) {
                compares++;
                if(a[j+1] < a[j]) {
                    swaps++;
                    swap(a, j, j+1);
                    swapped = true;
                }
            }

            if(!swapped) {
                break;
            }
        }
        return new BenchmarkResults(a, swaps, compares);
    }

    // https://en.wikipedia.org/wiki/Selection_sort#Implementations
    public static BenchmarkResults selectionSort(int[] a) {
        long swaps = 0;
        long compares = 0;

        for(int i = 0; i < a.length-1; i++) {
            int minIndex = i;
            for(int j = i+1; j < a.length; j++) {
                compares++;
                if(a[j] < a[minIndex]) {
                    minIndex = j;
                }
            }

            if(minIndex != i) {
                swaps++;
                swap(a, minIndex, i);
            }
        }
        return new BenchmarkResults(a, swaps, compares);
    }

    // https://en.wikipedia.org/wiki/Insertion_sort#Algorithm
    public static BenchmarkResults insertionSort(int[] a) {
        long swaps = 0;
        long compares = 0;

        for(int i = 1; i < a.length; i++) {
            for(int j = i; j > 0 && a[j-1] > a[j]; j--) {
                compares++;
                if(a[j-1] > a[j])  {
                    swaps++;
                    swap(a, j, j-1);
                }
            }
        }
        return new BenchmarkResults(a, swaps, compares);
    }

    // https://en.wikipedia.org/wiki/Quicksort#Multi-pivot_quicksort
    public static BenchmarkResults quickSort(int[] a, int low, int high) {
        long swaps = 0;
        long compares = 0;

        if(low >= high) return new BenchmarkResults(a, swaps, compares);

        long[] stats = partition(a, low, high, swaps, compares);
        BenchmarkResults fHalf = quickSort(a, low, (int)stats[0]);
        BenchmarkResults lHalf = quickSort(a, (int)stats[0]+1, high);

        swaps = stats[1]+fHalf.swaps+lHalf.swaps;
        compares = stats[2]+fHalf.compares+lHalf.compares;
        return new BenchmarkResults(a, swaps, compares);
    }

    public static long[] partition(int[] a, int low, int high, long swaps, long compares) {
        int pivot = a[(high+low)/2];
        int i = low-1;
        int j = high+1;
        
        while(true) {
            compares++;
            do {
                i++;
            } while(a[i] < pivot);

            compares++;
            do {
                j--;
            } while(a[j] > pivot);
            if(i >= j) return new long[] {j, swaps, compares};
            swaps++;
            swap(a, i, j);
        }
    }
}
