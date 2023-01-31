import java.util.Arrays;

public class List implements CapstoneList {

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
        if(index >= count) throw new IndexOutOfBoundsException();
        for(int i = count-1; i >= index; i--) {
            values[i+1] = values[i];
        }
        values[index] = value;
        count++;
    }

    public int get(int index) {
        if(index<-count || index>=count) throw new IndexOutOfBoundsException();
        return values[(index+count)%count]; // You can use negative numbers like in python
    }

    public int size() {
        return count;
    }

    public void clear() {
        count=0;
    }

    public boolean isEmpty() {
        return count==0;
    }
}
