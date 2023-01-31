import random
import os
import re

def main():
	listPath = 'words.txt'
	
	while True:
		lives = 6
		guesses = set()
		report = ''
		with open(listPath, 'r') as f:
			target = random.choice(f.readlines()).strip().upper()

		while True:
			os.system('clear')
			display_report(report, target, guesses, lives)
			if report == target:
				print('Congratulations! You won!')
				break;
			if lives <= 0:
				print('Game over! The word was: {}'.format(target))
				break;
			guess = get_guess(guesses).upper()
			guesses.add(guess)
			new_report = get_report(guesses, target)
			if len(new_report) == len(report):
				lives -= 1
			report = new_report
		if not try_again():
			clear_n(1)
			print('Thank you for playing!')
			break;

def get_report(gs, t):
	report = ''
	for c in t:
		if c.upper() in gs:
			report += c.upper()
	return report

def display_report(r, t, gs, l):
	states = ["  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
              "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
              "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
              "  +---+\n  |   |\n \\O   |\n  |   |\n      |\n      |\n=========",
              "  +---+\n  |   |\n \\O/  |\n  |   |\n      |\n      |\n=========",
              "  +---+\n  |   |\n \\O/  |\n  |   |\n /    |\n      |\n=========",
              "  +---+\n  |   |\n \\O/  |\n  |   |\n / \\  |\n      |\n========="]

	stateIndex=6-l
	print(states[stateIndex]+'\n')
	
	for c in t:
		if c.upper() in r.upper():
			print(c+' ', end='')
		else:
			print('_ ', end='')
	
	letters = list('QWERTYUIOPASDFGHJKLZXCVBNM')
	for i in range(len(letters)):
		c = letters[i]
		if c in gs:
			letters[i] = '-'

	print('\n\n{:s}\n{:^19s}\n{:^19s}\n\n'.format(' '.join(letters[:10]), ' '.join(letters[10:19]), ' '.join(letters[19:])))

def try_again():
	while True:
		g = input('Would you like to play again? (Y/N): ').strip().upper()
		if g == 'Y':
			return True
		if g == 'N': 
			return False
		print('Please enter Y or N.')
	
def get_guess(gs):
	while True:
		g = input('Guess: ').strip().upper()
		if len(g) == 1 and re.match('[A-Z]', g) and g not in gs:
			return g.upper()
		clear_n(2)
		print('Please enter a valid one-letter guess!')
	
def clear_n(n):
	print('\33[2K\r', end='')
	for i in range(n):
		print('\33[A\33[2K\r', end='')

if __name__ == '__main__':
	main()
