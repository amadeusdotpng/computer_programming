from typing import List

# Incremental Resizing Hash Table
class IHashTable:
    def __init__(self, length: int = 8):
        self.size: int = 0
        self.MAX_LOAD_FACTOR: int = 70 # 70%

        self.key_table: List = [None]*length
        self.value_table: List = [None]*length
        
        self.cindex = 0
        self.ckey_table: List = []
        self.cvalue_table: List = []

        self.DELETED = object()

    def _upsize(self):
        new_length = len(self.key_table)*2
        self.key_table, self.ckey_table = [None]*new_length, self.key_table
        self.value_table, self.cvalue_table = [None]*new_length, self.value_table
        self.cindex = 0
        while self.ckey_table[self.cindex] is None or self.ckey_table[self.cindex] == self.DELETED:
            self.cindex += 1

        self._clean()

    def _get_index(self, k, k_table):
        index = hash(k) % len(k_table)
        while k_table[index] and (k_table[index] != k or k_table[index] == self.DELETED):
            index = (index + 1) % len(k_table)

        return index

    def _clean(self):
        if self.cindex >= len(self.ckey_table):
            return

        k = self.ckey_table[self.cindex]
        index = self._get_index(k, self.key_table)

        self.key_table[index] = k
        self.value_table[index] = self.cvalue_table[self.cindex]

        self.ckey_table[self.cindex] = self.DELETED
        self.cvalue_table[self.cindex] = None
        
        while (self.cindex < len(self.ckey_table) and 
               (self.ckey_table[self.cindex] is None or 
                self.ckey_table[self.cindex] == self.DELETED)):
            self.cindex += 1

        
    def __setitem__(self, k, v):
        # check if needs to resize
        if (self.size / len(self.key_table) * 100) >= self.MAX_LOAD_FACTOR:
            self._upsize()
            
        index = self._get_index(k, self.key_table)

        if self.key_table[index] is None:
            self.size += 1

        self.key_table[index] = k
        self.value_table[index] = v

        self._clean()

    def __contains__(self, k):
        oindex = self._get_index(k, self.key_table)
        cindex = self._get_index(k, self.ckey_table)

        return self.key_table[oindex] == k or self.ckey_table[cindex] == k

    def __getitem__(self, k):
        index = self._get_index(k, self.key_table)
        if self.key_table[index] == k:
            return self.value_table[index]

        index = self._get_index(k, self.ckey_table)
        if self.ckey_table[index] == k:
                return self.cvalue_table[index]

        raise KeyError(f'The key "{k}" of type {type(k).__name__} is not in the table.')

    def __delitem__(self, k):
        index = self._get_index(k, self.key_table)
        if self.key_table[index] and self.key_table != self.DELETED:
            self.value_table[index] = None
            self.key_table[index] = self.DELETED
            self.size -= 1
            return

        index = self._get_index(k, self.ckey_table)
        if self.ckey_table[index] and self.key_table != self.DELETED:
            self.value_table[index] = None
            self.key_table[index] = self.DELETED
            self.size -= 1
            return
