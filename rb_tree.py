#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# Created by Vim
"""
红黑树多用在内部排序，即全放在内存中的，微软STL的map和set的内部实现就是红黑树。
B树多用在内存里放不下，大部分数据存储在外存上时。因为B树层数少，因此可以确保每次操作，读取磁盘的次数尽可能的少。
在数据较小，可以完全放到内存中时，红黑树的时间复杂度比B树低。反之，数据量较大，外存中占主要部分时，B树因其读磁盘次数少，而具有更快的速度。
"""


class RBTree(object):
    def __init__(self):
        self.nil = RBTreeNode(0)
        self.root = self.nil


class RBTreeNode(object):
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'black'
        self.size = None


# 左旋转
def left_rotate(T, x):
    y = x.right
    x.right = y.left
    if y.left != T.nil:
        y.left.parent = x
    y.parent = x.parent
    if x.parent == T.nil:
        T.root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y


# 右旋转
def right_rotate(T, x):
    y = x.left
    x.left = y.right
    if y.right != T.nil:
        y.right.parent = x
    y.parent = x.parent
    if x.parent == T.nil:
        T.root = y
    elif x == x.parent.right:
        x.parent.right = y
    else:
        x.parent.left = y
    y.right = x
    x.parent = y


# 红黑树的插入
def rb_insert(T, z):
    y = T.nil
    x = T.root
    while x != T.nil:
        y = x
        if z.key < x.key:
            x = x.left
        else:
            x = x.right
    z.parent = y
    if y == T.nil:
        T.root = z
    elif z.key < y.key:
        y.left = z
    else:
        y.right = z
    z.left = T.nil
    z.right = T.nil
    z.color = 'red'
    rb_insert_fix_up(T, z)
    return "%s,%s,%s" % (z.key, "颜色为", z.color)


# 红黑树的上色
def rb_insert_fix_up(T, z):
    while z.parent.color == 'red':
        if z.parent == z.parent.parent.left:
            y = z.parent.parent.right
            if y.color == 'red':
                z.parent.color = 'black'
                y.color = 'black'
                z.parent.parent.color = 'red'
                z = z.parent.parent
            else:
                if z == z.parent.right:
                    z = z.parent
                    left_rotate(T, z)
                z.parent.color = 'black'
                z.parent.parent.color = 'red'
                right_rotate(T, z.parent.parent)
        else:
            y = z.parent.parent.left
            if y.color == 'red':
                z.parent.color = 'black'
                y.color = 'black'
                z.parent.parent.color = 'red'
                z = z.parent.parent
            else:
                if z == z.parent.left:
                    z = z.parent
                    right_rotate(T, z)
                z.parent.color = 'black'
                z.parent.parent.color = 'red'
                left_rotate(T, z.parent.parent)
    T.root.color = 'black'


def rb_transplant(T, u, v):
    if u.parent == T.nil:
        T.root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v
    v.parent = u.parent


def rb_delete(T, z):
    y = z
    y_original_color = y.color
    if z.left == T.nil:
        x = z.right
        rb_transplant(T, z, z.right)
    elif z.right == T.nil:
        x = z.left
        rb_transplant(T, z, z.left)
    else:
        y = tree_minimum(z.right)
        y_original_color = y.color
        x = y.right
        if y.parent == z:
            x.parent = y
        else:
            rb_transplant(T, y, y.right)
            y.right = z.right
            y.right.parent = y
        rb_transplant(T, z, y)
        y.left = z.left
        y.left.parent = y
        y.color = z.color
    if y_original_color == 'black':
        rb_delete_fix_up(T, x)


# 红黑树的删除
def rb_delete_fix_up(T, x):
    while x != T.root and x.color == 'black':
        if x == x.parent.left:
            w = x.parent.right
            if w.color == 'red':
                w.color = 'black'
                x.parent.color = 'red'
                left_rotate(T, x.parent)
                w = x.parent.right
            if w.left.color == 'black' and w.right.color == 'black':
                w.color = 'red'
                x = x.parent
            else:
                if w.right.color == 'black':
                    w.left.color = 'black'
                    w.color = 'red'
                    right_rotate(T, w)
                    w = x.parent.right
                w.color = x.parent.color
                x.parent.color = 'black'
                w.right.color = 'black'
                left_rotate(T, x.parent)
                x = T.root
        else:
            w = x.parent.left
            if w.color == 'red':
                w.color = 'black'
                x.parent.color = 'red'
                right_rotate(T, x.parent)
                w = x.parent.left
            if w.right.color == 'black' and w.left.color == 'black':
                w.color = 'red'
                x = x.parent
            else:
                if w.left.color == 'black':
                    w.right.color = 'black'
                    w.color = 'red'
                    left_rotate(T, w)
                    w = x.parent.left
                w.color = x.parent.color
                x.parent.color = 'black'
                w.left.color = 'black'
                right_rotate(T, x.parent)
                x = T.root
    x.color = 'black'


def tree_minimum(x):
    while x.left != T.nil:
        x = x.left
    return x


# 中序遍历
def mid_sort(x):
    if x is not None:
        mid_sort(x.left)
        if x.key != 0:
            print('key:', x.key, 'x.parent', x.parent.key)
        mid_sort(x.right)


if __name__ == '__main__':
    nodes = [11, 2, 14, 1, 7, 15, 5, 8, 4]
    T = RBTree()
    for node in nodes:
        print '插入数据', rb_insert(T, RBTreeNode(node))
    print('中序遍历')
    mid_sort(T.root)
    rb_delete(T, T.root)
    print('中序遍历')
    mid_sort(T.root)
    rb_delete(T, T.root)
    print('中序遍历')
    mid_sort(T.root)
