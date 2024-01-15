import java.util.Arrays;

public class ArrayList implements CapstoneList {
	/* Instance Variables */
	private int[] vList;
	private int count;

	/**
	 * Constructs an empty ArrayList with an initial capacity of eight.
	 */
	public ArrayList() {
		vList = new int[8];
		count = 0;
	}

	/**
	 * Returns the string representation of the list with the elements in order enclosed by square brackets ("[]") and each separated by a comma and a space (", ").
	 * @return <code>the string representation of the listi</code>
	 */
	public String toString() {
		return Arrays.toString(Arrays.copyOf(vList, count));
	}
	

	private void ensureCapacity() {
		if(count>=vList.length) {
			vList=Arrays.copyOf(vList, count*2);
		}
	}

	
	/**
	 * Inserts the specified value at the specified position to the list. Shifts the elements at the specified position and any subsequent elements to the right.
	 * @param index <code>index in which the specified value is to be inserted</code>
	 * @param value <code>value that is to be inserted</code>
	 * @throws IndexOutOfBoundsException <code>if the index is out of range (index &lt; 0 || index &gt; size())</code>
	 */
	public void add(int index, int value) {
		ensureCapacity();
		for(int i = this.size()-1; i>=index; i--) {
			vList[i+1] = vList[i];
		}
		vList[index] = value;
		count++;
	}
	
	/**
	 * Appends the specified value to the list.
	 * @param value <code>value that is to be appended</code>
	 */
	public void add(int value) {
		ensureCapacity();
		vList[count] = value;
		count++;
	}
	
	/**
	 * Removes all of the elements from the list. The list will be empty after this call returns
	 */
	public void clear() {
		count = 0;
	}

	/**
	 * Returns a copy of this ArrayList instance.
	 * @return <code>a clone of this ArrayList instance</code>
	 */
	public CapstoneList clone() {
		ArrayList rList = new ArrayList();
		for(int v : vList) rList.add(v);
		return rList;
	}
	
	/**
	 * Returns <code>true</code> if the list contains the specified value, otherwise returns <code>false</code>.
	 * @param value <code>value whose presence in this list is to be tested</code>
	 * @return <code>true if the list contains the specified value</code>
	 */
	public boolean contains(int value) {
		for(int v : vList) {
			if(value == v) return true;
		}
		return false;
	}
	
	/**
	 * Returns <code>true</code> if this list and the specified list contain the same values in the same order, otherwise returns <code>false</code>.
	 * @param list <code>list whose equality with this list is to be tested</code>
	 * @return <code>true if this list and the specified list contain the same values in the same order</code>
	 */
	public boolean equals(CapstoneList list) {
		if(count != list.size()) return false;
		for(int i = 0; i < count; i++) {
			if(vList[i] != list.get(i)) return false;
		}
		return true;
	}
	
	/**
	 * Returns the value in the specified position in this list.
	 * @param index <code>index of the value to return</code>
	 * @return <code>the element at the specified position in this list.</code>
	 * @throws IndexOutOfBoundsException <code>if the index is out of range (index &lt; 0 || index &gt; size())</code>
	 */
	public int get(int index) {
		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
		return vList[index];
	}

	/**
	 * Returns the index of the first occurrence of the specified value in this list, or -1 if the specified value is not in this list.
	 * @param value <code>value to search for</code>
	 * @return <code>the index of the first occurrence of the specified value in this list, or -1 if the specified value is not in this list.</code>
	 */
	public int indexOf(int value) {
		for(int i = 0; i < count; i++) {
			if(value == vList[i]) return i;
		}
		return -1;
	}

	/**
	 * Returns <code>true</code> if this list contains no values.
	 * @return <code>true if this list contains no values.</code>
	 */
	public boolean isEmpty() {
		return count == 0;
	}

	/**
	 * Returns the index of the last occurrence of the specified value in this list, or -1 if this list does not contain the value.
	 * @param value <code>value to search for</code>
	 * @return <code>the index of the last occurrence of the specified value in this list, or -1 if this list does not contain the value</code>
	 */
	public int lastIndexOf(int value) {
		for(int i = count-1; i >= 0; i--) {
			if(value == vList[i]) return i;
		}
		return -1;
	}

	/**
	 * Removes the value at the specified position from this list. Shifts and subsequent values to the left.
	 * @param index <code>the index of the value to be removed</code>
	 * @return <code>the value to be removed</code>
	 * @throws IndexOutOfBoundsException <code>if the index is out of range (index &lt; 0 || index &gt; size())</code>
	 */
	public int pop(int index) {
		/* Original Implementation */
		/*		
		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
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

	/**
	 * Removes the first occurrence of the specified value from this list if it is present. Shifts any subsequent values to the left. If the list does not contain the value, the list remains unchanged.
	 * @param value <code>value that is to be removed</code>
	 * @return <code>true if this list contained the specified value</code>
	 */
	public boolean remove(int value) {
		int i = this.indexOf(value);
		if(i == -1) return false;
		this.pop(i);
		return true;
	}

	/**
	 * Replaces the value at the specified position in this list with the specified value.
	 * @param index <code>index of the value to be replaced</code>
	 * @param value <code>value to be stored at the specified posiition</code>
	 * @return <code>the value previously at the specified position</code>
	 * @throws IndexOutOfBoundsException <code>if the index is out of range (index &lt; 0 || index &gt; size())</code>
	 */
	public int set(int index, int value) {
		if(index < 0 || index >= count) throw new IndexOutOfBoundsException();
		int r = vList[index];
		vList[index] = value;
		return r;
	}

	/**
	 * Returns the number of values in this list.
	 * @return <code>the number of values in this list.</code>
	 */
	public int size() {
		return count;
	}

	/**
	 * Returns an ArrayList containing the values between the specified <code>fromIndex</code>, inclusive, and <code>toIndex</code>, exclusive.
	 * @param fromIndex <code>low endpoint (inclusive) of the subList</code>
	 * @param toIndex <code>high endpoint (exclusive) of the subList</code>
	 * @return <code>a new ArrayList containing the values between the specified fromIndex, inclusive, and toIndex, exclusive.</code>
	 * @throws IndexOutOfBoundsException <code>if (fromIndex &lt; 0 || toIndex &gt; size())</code>
	 * @throws IllegalArgumentException <code>if the endpoint indices are out of order (fromIndex &gt; toIndex)</code>
	 */
	public CapstoneList subList(int fromIndex, int toIndex) {
		if(fromIndex < 0 || toIndex > size()) throw new IndexOutOfBoundsException();
		if(fromIndex > toIndex) throw new IllegalArgumentException("'fromIndex' must be less than or equal to 'toIndex'");
		ArrayList rList = new ArrayList();
		for(int i = fromIndex; i < toIndex; i++) rList.add(this.get(i));
		return rList;
	}
	
	/**
	 * Returns an int array containing all of the value in this list in proper sequence.
	 * @Return <code>an int array containing the vlues of the list in proper sequence.</code>
	 */
	public int[] toArray() {
		return Arrays.copyOf(vList, count);
	}

}
