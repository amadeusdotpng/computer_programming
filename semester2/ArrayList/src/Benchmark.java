public class Benchmark {
	public static void main(String[] args) {
		final double MILLI2NANO = 1E6;
		final double SEC2MILLI = 1E3; 


		/* .add() and .pop() Benchmark */
		double implementAddMilli = 0; 
		double javaAddMilli = 0; 
		double implementPopMilli = 0; 
		double javaPopMilli = 0; 
		int n = 1;

		System.out.printf("%-10s | %14s | %14s | %14s | %14s\n", "", ".add()", "", ".pop()", "");
		System.out.printf("%-10s | %14s | %14s | %14s | %14s\n", "N", "Implementation", "Java", "Implementation", "Java");
		for(int i = 0; i < 20; i++) {
			java.util.ArrayList javaList = new java.util.ArrayList<Integer>();
			ArrayList implementList = new ArrayList();

			javaAddMilli = javaAdd(javaList, n)/MILLI2NANO;
			javaPopMilli = javaPop(javaList, n)/MILLI2NANO;
			implementAddMilli = implementAdd(implementList, n)/MILLI2NANO;
			implementPopMilli = implementPop(implementList, n)/MILLI2NANO;

			System.out.printf("%-10d | %14f | %14f | %14f | %14f\n", n, implementAddMilli, javaAddMilli, implementPopMilli, javaPopMilli);
			n *= 2;
		}

	}

	public static long implementAdd(ArrayList list, int n) {
		long start = System.nanoTime();
		for(int i = 0; i < n; i++) list.add(i);
		long rTime = System.nanoTime()-start;
		list = new ArrayList();
		return rTime;
	}

	public static long javaAdd(java.util.ArrayList list, int n) {
		long start = System.nanoTime();
		for(int i = 0; i < n; i++) 
			list.add(i);
		long rTime = System.nanoTime()-start;
		list = new java.util.ArrayList<Integer>();
		return rTime;
	}


	public static long implementPop(ArrayList list, int n) {
		for(int i = 0; i < n; i++) list.add(i);

		long start = System.nanoTime();
		for(int i = 0; i < n; i++) 
			list.pop(0);
		long rTime = System.nanoTime()-start;
		list = new ArrayList();
		return rTime;
	}

	public static long javaPop(java.util.ArrayList list, int n) {
		for(int i = 0; i<n; i++) list.add(i);
		long start = System.nanoTime();
		for(int i = 0; i < n; i++) list.remove(0);
		long rTime = System.nanoTime()-start;
		list = new java.util.ArrayList<Integer>();
		return rTime;
	}
}
