//Ask the user for a 5 letter word.  Loop until they actually give you 5 letters.
//After you do this print a whole bunch of blank lines so you can hide this word from a second user.

//This word will serve as the hidden word in wordle.
//Allow the second user to guess 5 letter words.
//Tell them if each letter is [not in the string], [in the string but not here], or [in the string here].
//Loop until they win.
//Allow for another game to be played.

import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;
public class Wordle {
	public static void main(String[] args) {
		int gameN = 1;

		System.out.println("Key: [] is correct guess");
		System.out.println("     () is in the word");
		System.out.println("     {} is incorrect guess\n");
    
		while(true) {
			String word = getWordN(5, "Please provide a five-letter word for the target word: ").toUpperCase();
			System.out.printf("Game %d:\nGuess the five letter word!~\n\n", gameN);
			guessWord(word);
			if(getQuit()) break;

			gameN++;
		}
		System.out.println("Thank you for playing!");
	}

	public static void guessWord(String target) {
    int guessN = 1;
    Map<Character, Integer> letters = new HashMap<Character, Integer>();
    letters = lettersHandler(letters);
    
		while(true) {
      System.out.println(printLetters(letters));
			String guess = getWordN(5, "Please provide a five-letter word: ").toUpperCase();
      clearN(27+26, 4);
      
			int[] scores = getScore(guess, target);
      letters = lettersHandler(letters, guess, scores);
			System.out.println(guessN+": "+printScore(scores, guess));
      
			if(scores[scores.length-1] == 1) {
        System.out.printf("\nYou Win! The word was \"%s\"!\n\n", target);
        break;
			}
      guessN++;
		}
	}

  public static Map<Character, Integer> lettersHandler(Map<Character, Integer> charsStatus) {
    if(charsStatus.isEmpty()) {
      for(int i = 65; i <= 90; i++) {
        charsStatus.put((char)i, 2);
      }
    }
    return charsStatus;
  }
  
  public static Map<Character, Integer> lettersHandler(Map<Character, Integer> charsStatus, String guess, int[] scores) {
    /*  0 = Correctly Guessed
     *  1 = In the Word
     *  2 = Unused
     *  All incorrectly guessed letters are removed from the map;
     */
    if(charsStatus.isEmpty()) return lettersHandler(charsStatus);
    
    for(int i = 0; i < guess.length(); i++) {
      char c = Character.toUpperCase(guess.charAt(i));
      if     (charsStatus.containsKey(c) && scores[i] == 2) charsStatus.remove(c);
      else if(charsStatus.containsKey(c) && scores[i] < charsStatus.get(c)) charsStatus.put(c, scores[i]);
    }
    
    return charsStatus;
  }

  public static String printLetters(Map<Character, Integer> chars) {
    String unused  = "Unused Letters:            ";
    String inWord  = "Letters in the Word:       ";
    String correct = "Correctly Guessed Letters: ";
    for(Map.Entry<Character, Integer> entry : chars.entrySet()) {
      if     (entry.getValue() == 2) unused  += entry.getKey()+"";
      else if(entry.getValue() == 1) inWord  += entry.getKey()+"";
      else if(entry.getValue() == 0) correct += entry.getKey()+"";
    }
    return String.format("\n%S\n%S\n%S", unused, inWord, correct);
  }
  
  public static Boolean getQuit() {
    while(true) {
			String quit = getWordN(1,"Do you want to play again? (y/n) ").toLowerCase();
			if	   (quit.equals("n")) return true;
			else if(quit.equals("y")) {
        System.out.println("==============================\n");
        return false;
      }
		}
  }
  
	public static int[] getScore(String guess, String target) {
		int[] scores = new int[guess.length()+1];
		scores[guess.length()] = 1;
    /*  0 = Correctly Guessed
     *  1 = In the Word
     *  2 = Incorrectly Guessed
     */
		for(int i = 0; i < guess.length(); i++) {
			if	(guess.charAt(i)==target.charAt(i)) {scores[i] = 0;}
			else if	(target.contains(guess.charAt(i)+""))  {scores[i] = 1; scores[guess.length()] = 0;}
			else					    {scores[i] = 2; scores[guess.length()] = 0;}
		}
		return scores;
	}

	public static String printScore(int[] scores, String guess) {
		String[] formats = {"[]", "()", "{}"};
		String scoreString = "";
		for(int i = 0; i < guess.length(); i++) {
			int formatIndex = scores[i];
			scoreString += formats[formatIndex].charAt(0)+""+guess.charAt(i)+""+formats[formatIndex].charAt(1);
		}
		return scoreString;
	}

	public static String getWordN(int n, String prompt) {
		Scanner s = new Scanner(System.in);	

		String word = "";
		
		while(true) {
			System.out.print(prompt);
			word = s.nextLine();
			if(verifyWord(word, n)) break;
			clearN(prompt.length()+word.length());
		}

		clearN(prompt.length()+word.length());
		return word;
	}

	public static boolean verifyWord(String s, int length) {
		for(int i = 0; i<s.length(); i++) {
			if(!Character.isLetter(s.charAt(i))) return false;
		}
		return s.length() == length;
	}

  public static void clearN(int n) {
    clearN(n, 1);
  }
  
	public static void clearN(int n, int u) {
    for(int i = 0; i < u; i++) {
		  System.out.printf("\033[1A\r");
		  for(int j = 0; j < n; j++) {
			  System.out.print(" ");
		  }
		  System.out.print("\r");
	  }
  }
}
