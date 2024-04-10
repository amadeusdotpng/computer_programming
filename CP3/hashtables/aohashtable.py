from typing import List

# All at Once Resizing Hash Table
class AOHashTable:
    def __init__(self, length: int = 8):
        self.size: int = 0
        self.MAX_LOAD_FACTOR: int = 70 # 70%

        self.key_table: List = [None]*length
        self.value_table: List = [None]*length

        self.DELETED = object()

    def _upsize(self):
        new_length = len(self.key_table)*2
        nkey_table = [None]*new_length
        nvalue_table = [None]*new_length

        for index in range(len(self.key_table)):
            k = self.key_table[index]
            v = self.value_table[index]
            if k is None or k == self.DELETED:
                continue

            nindex = self._get_index(k, nkey_table) 
            nkey_table[nindex] = k
            nvalue_table[nindex] = v

        self.key_table = nkey_table
        self.value_table = nvalue_table

    def _get_index(self, k, table):
        index = hash(k) % len(table)
        while table[index] and table[index] != k and table[index] != self.DELETED:
            index = (index + 1) % len(table)

        return index
        
    def __setitem__(self, k, v):
        if (self.size / len(self.key_table) * 100) > self.MAX_LOAD_FACTOR:
            self._upsize()
        index = self._get_index(k, self.key_table)

        if self.key_table[index] is None:
            self.size += 1

        self.key_table[index] = k
        self.value_table[index] = v


    def __contains__(self, k):
        index = self._get_index(k, self.key_table)

        return self.key_table[index] == k

    def __getitem__(self, k):
        index = self._get_index(k, self.key_table)
        if self.key_table[index] == k:
            return self.value_table[index]

        raise KeyError(f'The key "{k}" of type {type(k).__name__} is not in the table.')

    def __delitem__(self, k):
        index = self._get_index(k)
        if self.key_table[index] and self.key_table != self.DELETED:
            self.value_table[index] = None
            self.key_table[index] = self.DELETED
            count += 1
