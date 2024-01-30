from collections import deque
from typing import List, Set, Tuple


def get_edges(coord: Tuple):
    r, c = coord
    return (r+1, c), (r+1, c+1), (r, c+1), (r-1, c+1), (r-1, c), (r-1, c-1), (r, c-1), (r+1, c-1)

def dfs(board: List, dictionary: Set):
    prefixes = set(w[:i+1] for w in dictionary for i in range(len(w)))

    Q = deque([tuple([(r,c)]) for r in range(len(board)) for c in range(len(board[r]))])
    found_words = {}

    while Q:
        chain = Q.pop()

        last_coord = chain[-1]
        word = ''.join(board[coord[0]][coord[1]] for coord in chain)

        if word in dictionary:
            found_words[word] = chain

        for edge in get_edges(last_coord):
            if edge in chain:
                continue
            r, c = edge
            
            if not (0 <= r <= len(board)-1 and 0 <= c <= len(board[r])-1):
                continue

            new_chain = (*chain, edge)
            new_word = ''.join(board[coord[0]][coord[1]] for coord in new_chain)

            if new_word not in prefixes:
                continue
            
            Q.append(new_chain)

    return found_words
        

if __name__ == '__main__':
    words = set(w.strip().upper() for w in open('20k.txt'))
    board = [''.join(line.split()).upper() for line in open('boggle.in')]

    found_words = dfs(board, words)
    longest_path = set(max(found_words.values(), key=lambda w: len(w)))

    print('longest path on the board')
    print('\n'.join(' '.join('.' if (r,c) not in longest_path else board[r][c] 
              for c in range(len(board[r]))) 
              for r in range(len(board)))
    )

    print(f'word count: {len(found_words)}')
    print(f'longest word: {max(found_words.keys(), key=lambda w: len(w))}')
    print(f'longest word path: {longest_path}')
    