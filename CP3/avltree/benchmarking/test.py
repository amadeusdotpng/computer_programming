from avltree import AVLTree
from random import shuffle, seed
from collections import deque
import unittest

def is_balanced(T: AVLTree) -> bool:
    if T.root is None:
        return True

    Q = deque([T.root])
    while Q:
        N = Q.pop()
        if not (-1 <= N._balance_factor() <= 1):
            return False

        if N.l_child:
            Q.append(N.l_child)
        if N.r_child:
            Q.append(N.r_child)

    return True

class AVLTreeTesting(unittest.TestCase):

    def test_insert_deletion(self):
        N = 4000
        seed(0xdeadbeef)

        T = AVLTree()
        K = list(range(N))
        V = list(range(N))

        shuffle(K)
        shuffle(V)

        for k, v in zip(K, V):
            last = str(T)
            T[k] = v
            self.assertTrue(is_balanced(T), f'\nInserting: {k}\nBefore:\n{last}\nAfter:\n{T}')

        shuffle(K)
        for k in K:
            last = str(T)
            del T[k]
            self.assertTrue(is_balanced(T), f'\nDeleting: {k}\nBefore:\n{last}\nAfter:\n{T}')
        self.assertEqual(T.root, None)

            
if __name__ == '__main__':
    unittest.main()
