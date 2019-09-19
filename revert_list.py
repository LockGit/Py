# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-09-05 10:53:46
# @Last Modified by:   lock
# @Last Modified time: 2019-06-10 16:21:00

class Node():

	def __init__(self, value):
		self.next = None
		self.value = value


class DoubleNode:

	def __init__(self, value):
		self.value = value
		self.next = None
		self.pre = None


class RevertList():

    @classmethod
    def revert_linked_list(cls, head):
        pre = None
        while head is not None:
            next = head.next
            head.next = pre
            pre = head
            head = next
        return pre

    @classmethod
    def revert_double_linked_list(cls, head):
        pre = None
        while head is not None:
            next = head.next
            head.next = pre
            head.pre = next
            pre = head
            head = next
        return pre


if __name__ == '__main__':
	node = Node(1);
	node.next = Node(2);
	node.next.next = Node(3)
	print node.value
	print node.next.value
	print node.next.next.value
	print 'start revert list ...'
	newNode = RevertList.revert_linked_list(node)
	print newNode.value
	print newNode.next.value
	print newNode.next.next.value

	node2 = DoubleNode(1)
	node2.next = DoubleNode(2)
	node2.next.pre = node2
	node2.next.next = DoubleNode(3)
	node2.next.next.pre = node2.next
	node2.next.next.next = DoubleNode(4)
	node2.next.next.next.pre = node2.next.next
	node2.next.next.next.next = DoubleNode(5)
	node2.next.next.next.next.pre = node2.next.next.next
	node2.next.next.next.next.next = DoubleNode(6)
	node2.next.next.next.next.next.pre = node2.next.next.next
