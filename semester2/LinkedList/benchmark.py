# This is really ugly code

from linkedlist import LinkedList
from collections import deque
import timeit

def list_insert_right(n, L):
    for i in range(n):
        L.append(i)

def list_insert_left(n, L):
    for i in range(n):
        L.insert(0, i)

def list_pop_right(n, L):
    for i in range(n-1):
        L.pop()
        
def list_pop_left(n, L):
    for i in range(n-1):
        L.pop(0)
        
def deque_insert_right(n, L):
    for i in range(n):
        L.append(i)

def deque_insert_left(n, L):
    for i in range(n):
        L.appendleft(i)

def deque_pop_right(n, L):
    for i in range(n):
        L.pop()

def deque_pop_left(n, L):
    for i in range(n):
        L.popleft(0)

if __name__ == '__main__':
    job = int(input())

    if job == 0:
        print(f'{"ll_insert_right":>15} {"time":<23}')
        for i in range(25):
            L = LinkedList()
            durations = timeit.Timer(lambda: list_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')

        print(f'{"ll_insert_left":>15} {"time":<23}')
        for i in range(25):
            L = LinkedList()
            durations = timeit.Timer(lambda: list_insert_left(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
    
    elif job == 1:
        print(f'{"ll_pop_right":>15} {"time":<23}')
        for i in range(16):
            L = LinkedList()
            L.extend([i for i in range(2**i)])
            durations = timeit.Timer(lambda: list_pop_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
        
        print(f'{"ll_pop_left":>15} {"time":<23}')
        for i in range(25):
            L = LinkedList()
            L.extend([i for i in range(2**i)])
            durations = timeit.Timer(lambda: list_pop_left(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
    
    elif job == 2:
        print(f'{"l_insert_right":>15} {"time":<23}')
        for i in range(25):
            L = list()
            durations = timeit.Timer(lambda: list_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
        
        print(f'{"l_insert_left":>15} {"time":<23}')
        for i in range(25):
            L = list()
            durations = timeit.Timer(lambda: list_insert_left(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')

    elif job == 3: 
        print(f'{"l_pop_right":>15} {"time":<23}')
        for i in range(25):
            L = [i for i in range(2**i)]
            durations = timeit.Timer(lambda: list_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
    
        print(f'{"l_pop_left":>15} {"time":<23}')
        for i in range(25):
            L = [i for i in range(2**i)]
            durations = timeit.Timer(lambda: list_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
        
    elif job == 4:
        print(f'{"d_insert_right":>15} {"time":<23}')
        for i in range(25):
            L = deque()
            durations = timeit.Timer(lambda: deque_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
        
        print(f'{"d_insert_left":>15} {"time":<23}')
        for i in range(25):
            L = deque()
            durations = timeit.Timer(lambda: deque_insert_left(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
    
    elif job == 5:
        print(f'{"d_pop_right":>15} {"time":<23}')
        for i in range(25):
            L = deque([i for i in range(2**i)])
            durations = timeit.Timer(lambda: deque_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')
        
        print(f'{"d_pop_left":>15} {"time":<23}')
        for i in range(25):
            L = deque([i for i in range(2**i)])
            durations = timeit.Timer(lambda: list_insert_right(2**i, L)).repeat(repeat=1, number=1)[0]
            print(f'{2**i:>14}: {durations:<23}')
        print('')

