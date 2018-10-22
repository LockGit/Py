# !/usr/bin/env python
# encoding: utf-8
# author: Lock
# Created by Vim
"""
算法过程：
（1）、建堆：从len/2到第一个节点0处一直调用调整堆的过程，其中len为数组长度，len/2表示节点深度。
（2）、调整堆：比较节点i和它的孩子节点left(i),right(i)，选出三者最大者，如果最大值不是节点i而是它的一个孩子节点，那便交换节点i和该节点，然后再调用调整堆过程，这是一个递归的过程。调整堆的过程时间复杂度与堆的深度有关系，是lgn的操作。
（3）、堆排序：主要利用上面两个过程进行。首先是根据元素构建堆，然后将堆的根节点取出(一般是与最后一个节点进行交换)，将前面len-1个节点继续进行堆调整的过程，然后再将根节点取出，这样一直到所有节点都取出。
"""


def build_heap(seq):
    length = len(seq)
    for item in range(0, int((length / 2)))[::-1]:
        adjust_heap(seq, item, length)


def adjust_heap(seq, root, length):
    left_child = 2 * root + 1
    right_child = 2 * root + 2
    root_max = root
    if left_child < length and seq[left_child] > seq[root_max]:
        root_max = left_child
    if right_child < length and seq[right_child] > seq[root_max]:
        root_max = right_child
    if root_max != root:  # 如果做了堆调整,则root_max的值等于左节点或者右节点的，进行对调值操作
        seq[root_max], seq[root] = seq[root], seq[root_max]
        adjust_heap(seq, root_max, length)


def heap_sort(seq):
    length = len(seq)
    build_heap(seq)  # 建立初始堆
    for i in range(0, length)[::-1]:
        seq[0], seq[i] = seq[i], seq[0]  # 将根节点取出与最后一位做对调
        adjust_heap(seq, 0, i)  # 对前面len-1个节点继续进行堆调整过程
    return seq


if __name__ == "__main__":
    arr = [2, 1, 3, 8, 12, 5, 5, 6, 4, 10, 0]
    print(arr)
    heap_sort(arr)
    print(arr)
