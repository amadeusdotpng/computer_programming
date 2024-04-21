import sys

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.height = 1

        self.l_child = None
        self.r_child = None

    def _update_height(self):
        l_height = self.l_child.height if self.l_child else 0
        r_height = self.r_child.height if self.r_child else 0
        self.height = max(l_height, r_height) + 1

    def _set(self, k, v):
        if k == self.key:
            self.value = v
        if k < self.key:
            if self.l_child: self.l_child._set(k, v)
            else: self.l_child = Node(k, v)
        else:
            if self.r_child: self.r_child._set(k, v)
            else: self.r_child = Node(k, v)

        self._update_height()

    def _get(self, k):
        if k == self.key:
            return self.value
        if k < self.key:
            if self.l_child: self.l_child._get(k)
        else:
            if self.r_child: self.r_child._get(k)

        raise KeyError(k)

    def __str__(self):
        if self.l_child or self.r_child:
            return f'({self.key}->{self.value} {self.l_child} {self.r_child})'
        return f'{self.key}->{self.value}'

class UBTree:
    def __init__(self):
        self.root = None
    
    def depth(self) -> int:
        return self.root.height if self.root else 0

    def __setitem__(self, k, v):
        if self.root: self.root._set(k, v)
        else: self.root = Node(k, v)

    def __getitem__(self, k):
        if self.root: self.root._get(k)
        else: raise KeyError(k)

    def __str__(self):
        return str(self.root)
