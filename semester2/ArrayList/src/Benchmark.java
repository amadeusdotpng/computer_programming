public class Benchmark {
	public static void main(String[] args) {
		ArrayList list = new ArrayList();
		int n = 20;
		for(int i = 0; i < n; i++) list.add((int)(Math.random()*n));
		System.out.println(list);
		System.out.println(list.contains(10));
		System.out.println(list.get(9));
		System.out.println(list.isEmpty());
		System.out.println(list.indexOf(10));
		System.out.println(list.lastIndexOf(10));
		System.out.println(list.pop(9));
		System.out.println(list.remove(10));
		System.out.println(list.subList(3, 7));
		System.out.println(list.toArray().getClass().getSimpleName());
		System.out.println(list);
	}
}
