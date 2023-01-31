import java.util.Arrays;

public class List {

    public int[] values;
    public int count;
    

    public List() {
        values= new int[8];
        count = 0;
    }


    @Override
    public String toString() {
        return Arrays.toString(values);
    }
    private void upsize() {
        if(count>=values.length) {
            values=Arrays.copyOf(values, count*2);
        }
    }

    public void add(int value) {
        upsize();
        values[count] = value;
        count++;
    }

    public void insert(int value, int index) {
        upsize();
        for(int i = count-1; i >= index; i--) {
            values[i+1] = values[i];
        }
        values[index] = value;
        count++;
    }

    public int get(int i) {
        if(i<-count || i>=count) throw new IndexOutOfBoundsException();
        return values[(i+count)%count]; // You can use negative numbers like in python
    }

    public int size() {
        return count;
    }
}
