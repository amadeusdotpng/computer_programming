from collections import deque

class Node:
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

    # This is actually rotating to the left
    def _rr_rotate(self):
        a, b = self.value, self.r_child.value
        A = self.l_child
        B, C = self.r_child.l_child, self.r_child.r_child
        
        self.value = b
        self.l_child = Node(a)
        self.l_child.l_child = A
        self.l_child.r_child = B
        self.r_child = C

        self.l_child._update_height()
        self._update_height()

    # This is actually rotating to the right
    def _ll_rotate(self):
        a, b = self.value, self.l_child.value
        A = self.r_child
        B, C = self.l_child.r_child, self.l_child.l_child

        self.value = b
        self.r_child = Node(a)
        self.r_child.r_child = A
        self.r_child.l_child = B
        self.l_child = C

        self.r_child._update_height()
        self._update_height()

    def _rl_rotate(self):
        self.r_child._ll_rotate()
        self._rr_rotate()

    def _lr_rotate(self):
        self.l_child._rr_rotate()
        self._ll_rotate()

    def _ensure_balance(self):
        balance_factor = self._balance_factor()
        z_subtree = self.l_child if balance_factor > 1 else self.r_child if balance_factor < -1 else None

        if balance_factor > 1: 
            z_balance_factor = z_subtree._balance_factor()
            if z_balance_factor >= 0: self._ll_rotate()
            else: self._lr_rotate()

        elif balance_factor < -1:
            z_balance_factor = z_subtree._balance_factor()

            if z_balance_factor <= 0: self._rr_rotate()
            else: self._rl_rotate()

    def _min_and_parent(self):
        if not self.r_child:
            return self, None
        
        P = self
        N = self.l_child
        while N.l_child:
            P = N
            N = N.l_child

        return N, P

    def _max_and_parent(self):
        if not self.r_child:
            return self, None
        
        P = self
        N = self.r_child
        while N.r_child:
            P = N
            N = N.r_child

        return N, P

    def _replace_delete(self):
        if self.l_child:
            max_node, parent = self.l_child._max_and_parent()
            if parent is None:
                parent = self

            self.value = max_node.value
            if self.l_child.r_child: parent.r_child = max_node.l_child
            else: parent.l_child = max_node.l_child
            parent._update_height()
            parent._ensure_balance()
        elif self.r_child:
            min_node, parent = self.r_child._min_and_parent()
            if parent is None:
                parent = self

            self.value = min_node.value
            if self.r_child.l_child: parent.l_child = min_node.r_child
            else: parent.r_child = min_node.r_child
            parent._update_height()
            parent._ensure_balance()

        self._update_height()
        self._ensure_balance()

    def insert(self, v):
        if v < self.value:
            if self.l_child: self.l_child.insert(v)
            else: self.l_child = Node(v)
        else:
            if self.r_child: self.r_child.insert(v)
            else: self.r_child = Node(v)

        self._update_height()
        self._ensure_balance()
        

    def delete(self, v):
        if self.l_child and v == self.l_child.value: self.l_child._replace_delete()
        elif self.r_child and v == self.r_child.value: self.r_child._replace_delete()
        
        elif self.l_child and v < self.value: self.l_child.delete(v)
        elif self.r_child and v > self.value: self.r_child.delete(v)

        self._update_height()
        self._ensure_balance()

    def __str__(self):
        if self.l_child or self.r_child:
            return f'({self.value}+{self.height} {self.l_child} {self.r_child})'
        return f'{self.value}+{self.height}'

class Tree:
    def __init__(self):
        self.root = None
        self.height = 0
        
    def insert(self, v):
        if self.root:
            self.root.insert(v)
        else:
            self.root = Node(v)
        self.height = self.root.height

    def delete(self, v):
        if self.root:
            if v == self.root.value: self.root._replace_delete()
            else: self.root.delete(v)
        else:
            raise Exception("Empty Tree")

    def __str__(self):
        return str(self.root)

def is_balanced(T: Tree) -> bool:
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

if __name__ == '__main__':
    from random import randrange, shuffle
    T = Tree()
    # R = [25, 12, 51, 60, 29, 25, 70, 44, 75, 11, 80, 92, 80, 41, 22, 10, 2, 84, 3, 75, 62, 72, 80, 33, 16]
    R = [randrange(250) for _ in range(100)]
    print(R)
    for v in R:
        T.insert(v)
        print(T)
        print()
        if not is_balanced(T):
            print(f'was inserting {v}')
            raise Exception("unbalanced")

    shuffle(R)
    for v in R:
        T.delete(v)
        print(T)
        print()
        if not is_balanced(T):
            print(f'was removing {v}')
            raise Exception("unbalanced")

