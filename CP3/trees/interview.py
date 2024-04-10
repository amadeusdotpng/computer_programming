from collections import deque
import unittest
from tree import BinaryTree
from test import is_balanced
from random import seed, shuffle, choice, randrange

# Delete a Node from the BST
# --------------------------
# The TSBBST has a delete() function
# and i'm too lazy to rewrite it and remove
# the self-balancing stuff.

# Find the in-order successor of a given node in the BST
# ------------------------------------------------------
def inorder_successor(T: BinaryTree, v):
    # DFS
    Q = deque([T.root])
    V = set()
    found_big = False
    found_num = None
    f = lambda x: x is not None and x not in V
    while Q:
        N = Q[-1]
        children = list(filter(f, [N.r_child, N.l_child]))
        if children:
            for child in children: Q.append(child); V.add(child)
            
        else:
            P = Q.pop()
            if P.value > v:
                found_big = True
                found_num = (
                    P.value
                    if found_num is None 
                    else min(P.value, found_num)
                )

            if found_big and P.value < v:
                print(f'I early returned with the value {v}')
                return found_num
    return found_num

# Convert a sorted array into a balanced BST
# ------------------------------------------
# Don't use a self-balancing tree cos that's
# cheating
class BasicNode:
    def __init__(self, value):
        self.value = value
        self.height = 1

        self.l_child = None
        self.r_child = None

    def _update_height(self):
        l_height = self.l_child.height if self.l_child else 0
        r_height = self.r_child.height if self.r_child else 0
        self.height = 1 + max(l_height, r_height)

    def _balance_factor(self):
        l_height = self.l_child.height if self.l_child else 0
        r_height = self.r_child.height if self.r_child else 0
        return l_height - r_height

def sorted_to_BST(V):
    assert list(sorted(V)) == V
    def recursive_insert(N: BasicNode, lo, hi):
        if lo == hi:
            return

        mid = (lo+hi) // 2
        lo_mid = (lo + mid) // 2
        hi_mid = (mid+1+lo) // 2

        N.l_child = BasicNode(V[lo_mid])
        N.r_child = BasicNode(V[hi_mid])

        N._update_height()

        recursive_insert(N.l_child, lo, mid)
        recursive_insert(N.r_child, mid+1, hi)

    # Kickstart since we need an initial middle node
    L = 0
    H = len(V)
    M = (L+H) // 2

    N = BasicNode(V[M])

    L_M = (L + M) // 2
    H_M = (M+1+H) // 2

    N.l_child = BasicNode(V[L_M])
    N.r_child = BasicNode(V[H_M])

    N._update_height()

    recursive_insert(N.l_child, L, M)
    recursive_insert(N.r_child, M+1, H)

    return N

# Rotate left and rotate right
# ----------------------------
# TSBBST has a _rr_rotate() to rotate left
# and an _ll_rotate() to rotate right.

class InterviewUnitTest(unittest.TestCase):
    seed(0xdeadbeefcafebabe)
    V = [randrange(5000) for _ in range(1000)]

    def test_deletion(self):
        local_V = self.V[::]
        T = BinaryTree()
        for v in local_V:
            T.insert(v)
            self.assertTrue(is_balanced(T))

        shuffle(local_V)
        for v in local_V[:-1]:
            T.delete(v)
            self.assertTrue(is_balanced(T))
        self.assertEqual(T.root.value, local_V[-1])

    def test_inorder_successor(self):
        T = BinaryTree()
        for v in self.V:
            T.insert(v)
        sorted_V = list(sorted(list(set(self.V))))
        C = choice(sorted_V[:-1])
        C_index = sorted_V.index(C)
        res = inorder_successor(T, C)
        self.assertEqual(res, sorted_V[C_index+1])

    def test_sorted_to_BST(self):
        def basic_balanced(N: BasicNode) -> bool:
            Q = deque([N])
            while Q:
                N = Q.pop()
                if not (-1 <= N._balance_factor() <= 1):
                    return False

                if N.l_child:
                    Q.append(N.l_child)
                if N.r_child:
                    Q.append(N.r_child)

            return True

        root = sorted_to_BST(list(sorted(self.V)))
        self.assertTrue(basic_balanced(root))

if __name__ == '__main__':
    unittest.main()
