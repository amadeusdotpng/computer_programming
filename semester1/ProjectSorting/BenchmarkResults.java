public class BenchmarkResults {
    int[] array;
    long swaps;
    long compares;
    long time;
    public BenchmarkResults(int[] array_, long swaps_, long compares_) {
        array = array_;
        swaps = swaps_;
        compares = compares_;
    }

    public void setTime(long time_) {
        time = time_;
    }
}
