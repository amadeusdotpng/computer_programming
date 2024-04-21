from collections import deque

class _Node:
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

    def _balance_factor(self):
        l_height = self.l_child.height if self.l_child else 0
        r_height = self.r_child.height if self.r_child else 0
        return l_height - r_height


    # Right Right Rotation
    # ------------------
    # This is actually rotating the node to the left.
    # This is for when A is RIGHT-heavy and the RIGHT-subtree
    # of C is taller than its left-subtree.
    # e.g.
    #                       A (4)
    #                      / \
    #              -> (1) B   C (3) <- Unbalanced! Rotate
    #                        / \        node A to the Left!
    #                   (1) D   E (2)
    #                            \
    #                             F (1)
    # We only have to do a simple left rotation on A.
    def _rr_rotate(self):
        a_key, b_key = self.key, self.r_child.key
        a_val, b_val = self.value, self.r_child.value
        A = self.l_child
        B, C = self.r_child.l_child, self.r_child.r_child
        
        self.key = b_key
        self.value = b_val
        self.l_child = _Node(a_key, a_val)
        self.l_child.l_child = A
        self.l_child.r_child = B
        self.r_child = C

        self.l_child._update_height()
        self._update_height()

    # Left Left Rotation
    # ------------------
    # This is actually rotating the node to the right.
    # This is for when A is LEFT-heavy and the LEFT-subtree
    # of B is taller than its right-subtree.
    # e.g.
    #                   (4) A
    #                      / \
    #              -> (3) B   C (1) <- Unbalanced! Rotate
    #                    / \           node A to the Right!
    #               (2) D   E (1)
    #                  /
    #             (1) F
    # We only have to do a simple right rotation on A.
    def _ll_rotate(self):
        a_key, b_key = self.key, self.l_child.key
        a_val, b_val = self.value, self.l_child.value
        A = self.r_child
        B, C = self.l_child.r_child, self.l_child.l_child

        self.key = b_key
        self.value = b_val
        self.r_child = _Node(a_key, a_val)
        self.r_child.r_child = A
        self.r_child.l_child = B
        self.l_child = C

        self.r_child._update_height()
        self._update_height()

    # Right Left Rotation
    # -------------------
    # This is for when A is RIGHT-heavy but the LEFT-subtree
    # of C is taller than its right-subtree.
    # e.g.
    #                       A (4)
    #                      / \
    #              -> (1) B   C (3) <- Unbalanced! Must rotate C to the right first
    #                        / \       before rotating A to the left or else it will
    #                   (2) D   E (1)  still be unbalanced if we rotate A to the left
    #                      /           first.
    #                 (1) F              
    #
    # We must rotate C to the Right first (_ll_rotate) then rotate A
    # to the left (_rr_rotate).
    def _rl_rotate(self):
        self.r_child._ll_rotate()
        self._rr_rotate()


    # Left Right Rotation
    # -------------------
    # This is for when A is LEFT-heavy but the RIGHT-subtree
    # of B is taller than its left-subtree.
    # e.g.
    #                   (4) A
    #                      / \
    #              -> (3) B   C (1) <- Unbalanced! Must rotate C to the left first
    #                    / \           before rotating A to the right or else it will
    #               (1) D   E (2)      still be unbalanced if we rotate A to the right
    #                        \         first.
    #                         F (1)
    # We must rotate B to the left first (_rr_rotate) then rotate A
    # to the right (_ll_rotate).
    def _lr_rotate(self):
        self.l_child._rr_rotate()
        self._ll_rotate()

    def _ensure_balance(self):
        balance_factor = self._balance_factor()

        if balance_factor > 1: 
            z_subtree = (
                       self.l_child if balance_factor > 1 
                  else self.r_child if balance_factor < -1
                  else None
            )
            z_balance_factor = z_subtree._balance_factor()
            if z_balance_factor >= 0: self._ll_rotate()
            else: self._lr_rotate()

        elif balance_factor < -1:
            z_subtree = (
                       self.l_child if balance_factor > 1 
                  else self.r_child if balance_factor < -1
                  else None
            )
            z_balance_factor = z_subtree._balance_factor()

            if z_balance_factor <= 0: self._rr_rotate()
            else: self._rl_rotate()


    def _set(self, k, v):
        if k == self.key:
            self.value = v
        elif k < self.key:
            if self.l_child: self.l_child._set(k, v)
            else: self.l_child = _Node(k, v)
        else:
            if self.r_child: self.r_child._set(k, v)
            else: self.r_child = _Node(k, v)

        self._update_height()
        self._ensure_balance()

    def _get(self, k):
        if k == self.key:
            return self.value
        elif k < self.key:
            if self.l_child: return self.l_child._get(k)
        else:
            if self.r_child: return self.r_child._get(k)

        raise KeyError(k)


    # Deletion Stuff
    # --------------
    def _left_replace(self):
        if self.l_child.r_child is None:
            self.key = self.l_child.key
            self.value = self.l_child.value
            self.l_child = self.l_child.l_child

            self._update_height()
            self._ensure_balance()
            return

        # Find the right-most node in the left-subtree
        P = self
        N = self.l_child
        Q = deque([P])
        while N.r_child:
            Q.append(N)
            P = N
            N = N.r_child

        self.key = N.key
        self.value = N.value
        P.r_child = N.l_child

        while Q:
            N = Q.pop()
            N._update_height()
            N._ensure_balance()

    def _right_replace(self):
        if self.r_child.l_child is None:
            self.key = self.r_child.key
            self.value = self.r_child.value
            self.r_child = self.r_child.r_child

            self._update_height()
            self._ensure_balance()
            return

        # Find the left-most node in the right-subtree
        P = self
        N = self.r_child
        Q = deque([P])
        while N.l_child:
            Q.append(N)
            P = N
            N = N.l_child

        self.key = N.key
        self.value = N.value
        P.l_child = N.r_child

        while Q:
            N = Q.pop()
            N._update_height()
            N._ensure_balance()

    def _del(self, k):
        if self.l_child and k == self.l_child.key:
            if self.l_child.l_child: self.l_child._left_replace()
            elif self.l_child.r_child: self.l_child._right_replace()
            else: self.l_child = None

        elif self.r_child and k == self.r_child.key:
            if self.r_child.l_child: self.r_child._left_replace()
            elif self.r_child.r_child: self.r_child._right_replace()
            else: self.r_child = None

        elif self.l_child and k < self.key:
            self.l_child._del(k)

        elif self.r_child and k > self.key:
            self.r_child._del(k)


        self._update_height()
        self._ensure_balance()

    # Contains
    # --------
    def __contains__(self, k):
        if k == self.key:
            return True
        elif k < self.key:
            if self.l_child: k in self.l_child
        else:
            if self.r_child: k in self.r_child

        return False

    def __str__(self):
        if self.l_child or self.r_child:
            return f'({self.key}->{self.value} {self.l_child} {self.r_child})'
        return f'{self.key}->{self.value}'

class AVLTree:
    def __init__(self):
        self.root: (_Node | None) = None

    def depth(self) -> int:
        return self.root.height if self.root else 0

    def __setitem__(self, k, v):
        if self.root: self.root._set(k, v)
        else: self.root = _Node(k, v)

    def __getitem__(self, k):
        if self.root: self.root_get(k)
        else: raise KeyError(k)

    def __delitem__(self, k):
        if self.root:
            if k == self.root.key:
                if self.root.l_child: self.root._left_replace()
                elif self.root.r_child: self.root._right_replace()
                else: self.root = None
            else: 
                self.root._del(k)
        else:
            raise KeyError(k)

    def __contains__(self, k):
        return k in self.root

    def __str__(self):
        return str(self.root)
