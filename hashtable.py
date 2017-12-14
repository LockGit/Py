# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-15 00:49:17
# @Last Modified by:   lock
# @Last Modified time: 2017-12-15 01:00:13
class Item(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable(object):

    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in xrange(self.size)]

    def hash_function(self, key):
        return key % self.size

    def set(self, key, value):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                item.value = value
                return
        self.table[hash_index].append(Item(key, value))

    def get(self, key):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                return item.value
        return None

    def remove(self, key):
        hash_index = self.hash_function(key)
        for i, item in enumerate(self.table[hash_index]):
            if item.key == key:
                del self.table[hash_index][i]

if __name__ == '__main__':
    hash_table = HashTable(5);
    hash_table.set(1,'x')
    hash_table.set(1,'m')
    hash_table.set(2,'y')
    hash_table.set(3,'z')
    print hash_table.get(1)
    print hash_table.get(2)
    print hash_table.get(3)