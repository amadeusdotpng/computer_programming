from collections import deque
from typing import Set
import sys

def get_next_words(word: str, dictionary: Set):
    word = [s for s in word]
    word_set = set()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Modifications
    for i in range(len(word)):
        for c in alphabet:
            if c == word[i]:
                continue

            next_word = word[::]
            next_word[i] = c
            word_set.add(''.join(next_word))

    # Add
    for i in range(len(word)+1):
        for c in alphabet:
            next_word = word[::]
            next_word.insert(i, c)
            word_set.add(''.join(next_word))

    # Remove
    for i in range(len(word)):
        word_set.add(''.join(c for j,c in enumerate(word) if i != j))

    return set(w for w in word_set if w in dictionary)

def bfs(root_word: str, goal_word: str, dictionary: Set):
    Q = deque([tuple([root_word])])
    visited = {root_word: 0}
    solutions = set()

    max_depth = None
    while Q:
        chain = Q.popleft()
        depth, last_word = len(chain)-1, chain[-1]

        if last_word == goal_word:
            solutions.add(chain)
            if not max_depth:
                max_depth = depth
            continue

        for next_word in get_next_words(last_word, dictionary):
            if max_depth and depth+1 > max_depth:
                continue

            if next_word in visited and visited[next_word] < depth+1:
                continue

            new_chain = (*chain, next_word)

            visited[next_word] = depth+1
            Q.append(new_chain)

    return solutions, max_depth


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('please include the starting and ending words in the arguments')

    else:
        words = set(W.strip().upper() for W in open('20k.txt'))

        start = sys.argv[1].upper()
        end = sys.argv[2].upper()

        paths, length= bfs(start, end, words)
        print(f'number of transformations: {length}')
        print('\n'.join(' -> '.join(t) for t in paths))
