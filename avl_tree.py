#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# Created by Vim
"""
平衡二叉搜索树
1、若它的左子树不为空，则左子树上所有的节点值都小于它的根节点值。
2、若它的右子树不为空，则右子树上所有的节点值均大于它的根节点值。
3、它的左右子树也分别可以充当为二叉查找树。
4、每个节点的左子树和右子树的高度差至多等于1。
"""


class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0


class AvlTree(object):
    def __init__(self):
        self.root = None

    def find(self, key):
        if self.root is None:
            return None
        else:
            return self._find(key, self.root)

    def _find(self, key, node):
        if node is None:
            return None
        elif key < node.key:
            return self._find(key, self.left)
        elif key > node.key:
            return self._find(key, self.right)
        else:
            return node

    def find_min(self):
        if self.root is None:
            return None
        else:
            return self._find_min(self.root)

    def _find_min(self, node):
        if node.left:
            return self._find_min(node.left)
        else:
            return node

    def find_max(self):
        if self.root is None:
            return None
        else:
            return self._find_max(self.root)

    def _find_max(self, node):
        if node.right:
            return self._find_max(node.right)
        else:
            return node

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def single_left_rotate(self, node):
        k1 = node.left
        node.left = k1.right
        k1.right = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.left), node.height) + 1
        return k1

    def single_right_rotate(self, node):
        k1 = node.right
        node.right = k1.left
        k1.left = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.right), node.height) + 1
        return k1

    def double_left_rotate(self, node):
        node.left = self.single_right_rotate(node.left)
        return self.single_left_rotate(node)

    def double_right_rotate(self, node):
        node.right = self.single_left_rotate(node.right)
        return self.single_right_rotate(node)

    def put(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self.root = self._put(key, self.root)

    def _put(self, key, node):
        if node is None:
            node = Node(key)
        elif key < node.key:
            node.left = self._put(key, node.left)
            if (self.height(node.left) - self.height(node.right)) == 2:
                if key < node.left.key:
                    node = self.single_left_rotate(node)
                else:
                    node = self.double_left_rotate(node)
        elif key > node.key:
            node.right = self._put(key, node.right)
            if (self.height(node.right) - self.height(node.left)) == 2:
                if key < node.right.key:
                    node = self.double_right_rotate(node)
                else:
                    node = self.single_right_rotate(node)

        node.height = max(self.height(node.right), self.height(node.left)) + 1
        return node

    def delete(self, key):
        self.root = self.remove(key, self.root)

    def remove(self, key, node):
        if node is None:
            raise KeyError, 'Error,key not in tree'
        elif key < node.key:
            node.left = self.remove(key, node.left)
            if (self.height(node.right) - self.height(node.left)) == 2:
                if self.height(node.right.right) >= self.height(node.right.left):
                    node = self.single_right_rotate(node)
                else:
                    node = self.double_right_rotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
        elif key > node.key:
            node.right = self.remove(key, node.right)
            if (self.height(node.left) - self.height(node.right)) == 2:
                if self.height(node.left.left) >= self.height(node.left.right):
                    node = self.single_left_rotate(node)
                else:
                    node = self.double_left_rotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
        elif node.left and node.right:
            if node.left.height <= node.right.height:
                min_node = self._find_min(node.right)
                node.key = min_node.key
                node.right = self.remove(node.key, node.right)
            else:
                max_node = self._find_max(node.left)
                node.key = max_node.key
                node.left = self.remove(node.key, node.left)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
        else:
            if node.right:
                node = node.right
            else:
                node = node.left

        return node


if __name__ == '__main__':
    avlTree = AvlTree()
    avlTree.put(1)
    avlTree.put(2)
    avlTree.put(3)
    avlTree.put(4)
    avlTree.put(5)
    avlTree.put(6)
    avlTree.put(7)
    avlTree.put(8)
    print avlTree.find_max().key
    avlTree.put(9)
    print avlTree.find_max().key
    print avlTree.find_min().key
