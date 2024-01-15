import java.util.*;
import java.io.*;

public class Hangman {
	public static void main(String[] args) {
		while(true) {
			int lives = 6;
			ArrayList<Character> guesses = new ArrayList<Character>();
			final String listPath = "words.txt";
			String report = "";
			String target = getRandomWord(listPath);

			while(true) {
				clearN(100, 20);
				System.out.println("");
				displayReport(report, target, guesses, lives);
				if(report.equals(target.toUpperCase())) {System.out.println("Congratulations! You win!"); break;}
				if(lives <= 0) {System.out.printf("Game over! The word was: %s\n", target); break;}
				char guess = getGuess(guesses);
				guesses.add(guess);

				String newReport = getReport(guesses, target);
				if(newReport.length() == report.length()) lives--;
				report = newReport;
			}

			if(!tryAgain()) {clearN(100,1); System.out.println("Thank you for playing!"); break;}
		}
	}

		public static String getReport(ArrayList<Character> gs, String t) {
			String report = "";
			for(char c : t.toCharArray()) {
			if(gs.contains(Character.toUpperCase(c))) report += c;
		}
		return report.toUpperCase();
		
	}

	public static void displayReport(String r, String t, ArrayList<Character> gs, int l) {
		String[] states = {"  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
						   "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
						   "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
						   "  +---+\n  |   |\n \\O   |\n  |   |\n      |\n      |\n=========",
						   "  +---+\n  |   |\n \\O/  |\n  |   |\n      |\n      |\n=========",
						   "  +---+\n  |   |\n \\O/  |\n  |   |\n /    |\n      |\n=========",
						   "  +---+\n  |   |\n \\O/  |\n  |   |\n / \\  |\n      |\n========="};
		int stateIndex = 6-l;
		System.out.println(states[stateIndex]+"\n\n");

		for(char c : t.toCharArray()) {
			if(r.contains(Character.toString(c).toUpperCase())) System.out.printf("%c ", Character.toUpperCase(c));
			else System.out.print("_ ");
		}
		String topRow    = "";
		String middleRow = "";
		String bottomRow = "";

		for(char c : "QWERTYUIOP".toCharArray()) {
			if(gs.contains(c)) topRow += "-";
			else topRow += c;
		}

		for(char c : "ASDFGHJKL".toCharArray()) {
			if(gs.contains(c)) middleRow += "-";
			else middleRow += c;
		}

		for(char c : "ZXCVBNM".toCharArray()) {
			if(gs.contains(c)) bottomRow += "-";
			else bottomRow += c;
		}
		System.out.println("\n");
		System.out.printf("%s\n %s\n   %s\n\n\n", String.join(" ", topRow.split("")), String.join(" ", middleRow.split("")), String.join(" ", bottomRow.split("")));
	}

	public static char getGuess(ArrayList<Character> gs) {
		Scanner s = new Scanner(System.in);
		while(true) {
			System.out.print("Guess: ");
			String guess = s.nextLine().strip().toUpperCase();
			if(guess.length() == 1 && guess.matches("[A-Z]") && !gs.contains(guess.charAt(0))) return guess.charAt(0);
			else {clearN(100, 2); System.out.println("Please enter a valid one-letter guess!");}
		}
	}

	public static boolean tryAgain() {
		Scanner s = new Scanner(System.in);
		while(true) {
			System.out.print("Would you like to try again? (Y/N): ");
			String g = s.nextLine().strip().toUpperCase();
			if(g.equals("Y")) return true;
			if(g.equals("N")) return false;
			clearN(100, 2);
			System.out.println("Please enter Y or N.");
		}
	}

	public static String getRandomWord(String path) {
		try {
			ArrayList<String> lines = new ArrayList<String>();
			File f = new File(path);
			Scanner s = new Scanner(f);
			while(s.hasNextLine()) lines.add(s.nextLine());
			return lines.get((int)(Math.random()*lines.size()));
		} catch(Exception e) {
			return "error";
		}
	}

	public static void clearN(int n, int u) {
    for(int i = 0; i < u; i++) {
		  System.out.print("\033[1A\r");
		  for(int j = 0; j < n; j++) {
			  System.out.print(" ");
		  }
		  System.out.print("\r");
	  }
  }
}	
