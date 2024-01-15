class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return f'{self.value}'


class LinkedList:
    def __init__(self):
        self.node_count = 0
        self.head = None
        self.tail = None

    def __add__(self, other):
        '''Dunder function for "+". Merges the current list and another
           iterable.

        Parameters
        ----------
        other: iterable
            Another list to add to the linked list.

        Returns
        -------
        out: LinkedList
            A LinkedList containing the elements of the old and other list.
        '''
        out = LinkedList()
        out.extend(self)
        out.extend(other)
        return out

    def __delitem__(self, index):
        '''Dunder function for "del list[index]".

        Parameters
        ----------
        index: int
            Index of element to delete.
        '''
        if type(index) == int:
            self._removenode(index)

    def __getitem__(self, index):
        '''Dunder function for "list[index]".

        Parameters
        ----------
        index: int
            Index of element to retrieve.

        Returns
        -------
        out: Node
            Node at the specified index.
        '''
        if type(index) == int:
            return self._getnode(index)
            
    def __setitem__(self, index, value):
        '''Dunder function for "list[index]".

        Parameters
        ----------
        index: int
            Index of element to replace.

        value: T
            Value to replace the element at the specified index.
        '''
        node = self._getnode(index)
        node.value = value

    def __len__(self):
        '''Dunder function for "len(list)".

        Returns
        -------
        node_count: int
            The length of the list.
        '''
        return self.node_count

    def _getnode(self, index):
        '''Helper function for traversing the list.

        Parameters
        ----------
        index: int
            Index of node to traverse to.

        Returns
        -------
        current_node: Node
            The node at the specified index.
        '''
        if -self.node_count > index or index > self.node_count-1:
            raise IndexError('list index out of range')

        current_node = self.head
        for i in range(index % self.node_count):
            current_node = current_node.next
        return current_node

    def _addnode(self, raw_index, value):
        '''Helper function for adding a new node to the list.

        Parameters
        ----------
        raw_index: int
            Index in which to insert the new node.

        value: T
            Value of the new element to be inserted.
        '''
        insert_node = Node(value)

        if not self.head:
            self.head = insert_node
            self.tail = insert_node
            self.node_count += 1
            return

        index = raw_index % self.node_count
        if -self.node_count > raw_index or raw_index > self.node_count:
            raise IndexError('list index out of range')

        if raw_index == self.node_count:
            self.tail.next = insert_node
            self.tail = insert_node
        elif index == 0:
            insert_node.next = self.head
            self.head = insert_node
        else:
            prev_node = self._getnode(index-1)
            next_node = prev_node.next
            
            prev_node.next = insert_node
            insert_node.next = next_node
        self.node_count +=1

    def _removenode(self, raw_index):
        '''Helper function for removing a node from the list.

        Parameters
        ----------
        raw_index: int
            Index of the node to delete.

        Returns
        -------
        curr_node: Node
            The node at the specified index.
        '''
        if not self.node_count:
            return
        index = raw_index % self.node_count

        if -self.node_count > raw_index or raw_index > self.node_count-1:
            raise IndexError('list index out of range')

        if index == 0:
            curr_node = self.head
            next_node = curr_node.next
            self.head = next_node
            self.node_count -= 1
            return curr_node
        elif index == self.node_count-1:
            prev_node = self._getnode(index-1)
            curr_node = prev_node.next
            self.tail = prev_node
            self.tail.next = None
            self.node_count -= 1
            return curr_node
        else:
            prev_node = self._getnode(index-1)
            curr_node = prev_node.next
            next_node = curr_node.next
            prev_node.next = next_node
            self.node_count -= 1
            return curr_node

            
    def append(self, value):
        '''Adds a new node containing the specified value to the end of the
           list.

        Parameters
        ----------
        value: T
            Value of the new element to be appended.
        '''
        self._addnode(self.node_count, value)

    def extend(self, other):
        '''Merges an iterable to the end of the list.

        Parameters
        ----------
        other: iterable
            The iterable to merge with the list.
        '''
        for value in other:
            self._addnode(self.node_count, value)

    def insert(self, index, value):
        '''Inserts a new node containing the specified value at the specified
           index.

        Parameters
        ----------
        index: int
            Index in which to insert the new element.

        value: T
            Value of the new element to be inserted.
        '''
        self._addnode(index, value)

    def clear(self):
        '''Erases all elements from the list.
        '''
        self.__init__()

    def pop(self, index=-1):
        '''Removes the node at the end of the list or at the specified index.

        Parameters
        ----------
        index: int, default=-1
            Index in which to insert the new element.

        Returns
        -------
        popped_node: Node
            The node removed from the list at the at the end of the list or at
            the specified index.
        '''
        return self._removenode(index)

    # can totally be optimized to iterating and removing at the same function
    def remove(self, value_):
        '''Removes the first instance of the specified value.

        Parameters
        ----------
        value_: T
            Value to be removed.
        '''
        for i, value in enumerate(self):
            if value == value_:
                self._removenode(i)

    def count(self, value):
        '''Counts the number of instances of the specified value in the list.

        Parameters
        ----------
        value_: T
            Value to be counted.

        Returns
        -------
        c: int
            The number of instances of the specified value.
        '''
        c = 0
        for node in self:
            if node == value:
                c += 1
        return c

    def index(self, value_):
        '''Finds the index of the first instance of the specified value in the
           list.

        Parameters
        ----------
        value_: T
            Value to find the index of.

        Returns
        -------
        index: int
            The index of the first instance of the specified value.
        '''
        for index, value in enumerate(self):
            if value == value_:
                return index

    def reverse(self):
        '''Reverses the list.
        '''
        for i in range(self.node_count-1):
            self._addnode(i, self._removenode(-1))

    def __str__(self):
        '''Dunder function for "print(list)" to make it look like Python's
           normal list.
        '''
        out = ''
        current_node = self.head
        while current_node:
            out += f'{current_node}, '
            current_node = current_node.next
        return f"[{out[:-2]}]"
