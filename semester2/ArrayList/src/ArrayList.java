import java.util.Arrays;
import java.util.stream.IntStream;

public class ArrayList implements CapstoneList {
	/* Instance Variables */
	private int[] vList;
	private int count;

	public ArrayList() {
		vList = new int[8];
		count = 0;
	}

	public String toString() {
		return Arrays.toString(Arrays.copyOf(vList, count));
	}

	private void ensureCapacity() {
		if(count>=vList.length) {
			vList=Arrays.copyOf(vList, count*2);
		}
	}

	public void add(int index, int value) {
		ensureCapacity();
		for(int i = this.size()-1; i>=index; i--) {
			vList[i+1] = vList[i];
		}
		vList[index] = value;
		count++;
	}
	
	public void add(int value) {
		ensureCapacity();
		vList[count] = value;
		count++;
	}
	
	public void clear() {
		vList = new int[8];
		count = 0;
	}

	public CapstoneList clone() {
		ArrayList rList = new ArrayList();
		for(int v : vList) rList.add(v);
		return rList;
	}
	
	public boolean contains(int value) {
		for(int v : vList) {
			if(value == v) return true;
		}
		return false;
	}
	
	public boolean equals(CapstoneList list) {
		if(count != list.size()) return false;
		for(int i = 0; i < count; i++) {
			if(vList[i] != list.get(i)) return false;
		}
		return true;
	}
	
	public int get(int index) {
		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
		return vList[index];
	}

	public int indexOf(int value) {
		for(int i = 0; i < count; i++) {
			if(value == vList[i]) return i;
		}
		return -1;
	}

	public boolean isEmpty() {
		return count == 0;
	}

	public int lastIndexOf(int value) {
		for(int i = count-1; i >= 0; i--) {
			if(value == vList[i]) return i;
		}
		return -1;
	}

	public int pop(int index) {
/*		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
		int r = vList[index];
		for(int i = index; i < count-1; i++) {
			vList[i] = vList[i+1];
		}
*/
		/* Actual Java Implementation */
	
		int r = vList[index];
		int move = count - index - 1;
		if(move > 0)
			System.arraycopy(vList, index + 1, vList, index, move);

		count--;
		return r;
	}

	public boolean remove(int value) {
		int i = this.indexOf(value);
		if(i == -1) return false;
		this.pop(i);
		return true;
	}

	public int set(int index, int value) {
		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
		int r = vList[index];
		vList[index] = value;
		return r;
	}

	public int size() {
		return count;
	}

	public CapstoneList subList(int fromIndex, int toIndex) {
		ArrayList rList = new ArrayList();
		for(int i = fromIndex; i < toIndex; i++) rList.add(this.get(i));
		return rList;
	}

	public int[] toArray() {
		return Arrays.copyOf(vList, count);
	}

}
