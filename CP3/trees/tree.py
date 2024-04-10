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


    # This is actually rotating the node to the left
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

    # This is actually rotating the node to the right
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

    def insert(self, v):
        if v < self.value:
            if self.l_child: self.l_child.insert(v)
            else: self.l_child = Node(v)
        else:
            if self.r_child: self.r_child.insert(v)
            else: self.r_child = Node(v)

        self._update_height()
        self._ensure_balance()

    def _replace_with_min(self, P, N):
        if not self.l_child:
            N.value = self.value
            if P == N: P.r_child = self.r_child
            else: P.l_child = self.r_child
        else:
            self.l_child._replace_with_max(self, N)
        self._update_height()
        self._ensure_balance()

    def _replace_with_max(self, P, N):
        if not self.r_child:
            N.value = self.value
            if P == N: P.l_child = self.l_child
            else: P.r_child = self.l_child
        else:
            self.r_child._replace_with_max(self, N)

        self._update_height()
        self._ensure_balance()

    def _replace_delete(self):
        if self.l_child:
            self.l_child._replace_with_max(self, self)
        elif self.r_child:
            self.r_child._replace_with_min(self, self)

        self._update_height()
        self._ensure_balance()

    def delete(self, v):
        if self.l_child and v == self.l_child.value:
            if self.l_child.l_child or self.l_child.r_child:
                self.l_child._replace_delete()
            else:
                self.l_child = None

        elif self.r_child and v == self.r_child.value:
            if self.r_child.l_child or self.r_child.r_child:
                self.r_child._replace_delete()
            else:
                self.r_child = None
        
        elif self.l_child and v < self.value:
            self.l_child.delete(v)

        elif self.r_child and v > self.value:
            self.r_child.delete(v)

        self._update_height()
        self._ensure_balance()

    def __str__(self):
        if self.l_child or self.r_child:
            return f'({self.value} {self.l_child} {self.r_child})'
        return f'{self.value}'

class BinaryTree:
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
            if v == self.root.value:
                if self.root.l_child or self.root.r_child:
                    self.root._replace_delete()
                else:
                    self.root = None
            else: self.root.delete(v)
        else:
            raise Exception("Empty Tree")

    def __str__(self):
        return str(self.root)
