public class Main {
    public static void main(String[] args) {
        List L = new List();
        int n = 3;
        for(int i = 0; i < n; i++) L.add((int)(Math.random()*100));
        L.insert(100, 1);
        System.out.println(L.get(-1));
        System.out.println(L);
        System.out.println(L.values.length);
        System.out.println(L.size());
    }
}