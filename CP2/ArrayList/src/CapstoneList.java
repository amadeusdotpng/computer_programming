//DON'T MODIFY THIS FILE!!!

public interface CapstoneList
{
    public void add(int index, int value); 
    public void add(int value);
    public void clear();
    public CapstoneList clone(); //bonus
    public boolean contains(int value);
    public boolean equals(CapstoneList list);
    public int get(int index);
    public int indexOf(int value);
    public boolean isEmpty();
    public int lastIndexOf(int value); //bonus
    public int pop(int index); //remove specified index
    public boolean remove(int value); //remove first occurence
    public int set(int index, int value);
    public int size();
    public CapstoneList subList(int fromIndex, int toIndex); // bonus
    public int[] toArray(); //bonus
    
}
