public class Main {
	public static void main(String[] args) throws Exception {
		Turtle.bgcolor("Cyan");
		Turtle.setCanvasSize(1280,720);
		
		Ground job1 = new Ground();
		Horizon job2 = new Horizon();
		Sun job3 = new Sun();
		Ground job4 = new Ground();
		Dwelling job5 = new Dwelling();
		Dweller job6 = new Dweller();
		Cloud job7 = new Cloud(400, 200);
		Cloud job8 = new Cloud(100, 300);
		Cloud job9 = new Cloud(-250, 250);

		job1.start();
		job2.start();
		
		job1.join();
		job2.join();

		job3.start();

		job3.join();

		job4.start();
		job4.join();

		job5.start();
		job5.join();
		
		job6.start();
		job7.start();
		job8.start();
		job9.start();
	}
}

