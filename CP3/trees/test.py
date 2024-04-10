from tree import BinaryTree
from random import randrange, shuffle
from collections import deque
import unittest


def is_balanced(T: BinaryTree) -> bool:
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
class TreeTesting(unittest.TestCase):
    N = 10000

    def test_insert_deletion(self):
        T = BinaryTree()
        V = [randrange(self.N) for _ in range(self.N)]

        for v in V:
            T.insert(v)
            self.assertTrue(is_balanced(T))

        shuffle(V)
        for v in V:
            T.delete(v)
            self.assertTrue(is_balanced(T))
        self.assertEqual(T.root, None)


if __name__ == '__main__':
    unittest.main()
