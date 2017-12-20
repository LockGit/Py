# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-20 22:53:58
# @Last Modified by:   lock
# @Last Modified time: 2017-12-20 23:27:23

#常规做法,遍历一次链表，获得长度step,在从0的位置遍历到step/2的位置
class Node(object):
  def __init__(self,data,next):
    self.data=data
    self.next=next

n1 = Node('n1',None)
n2 = Node('n2',n1)
n3 = Node('n3',n2)
n4 = Node('n4',n3)
n5 = Node('n5',n4)

head = n5 
step = 0
while head.next is not None:
  step = step+1
  head = head.next


head = n5 
for x in xrange(0,step/2):
  head = head.next


print '普通遍历方式,单链表中间节点为:%s,索引为:%s，遍历一次链表，在从0遍历到中间位置' % (head.data,step/2)


#快慢指针方式,遍历一次链表，快指针到达链表末尾，慢指针到达链表中间
class Node(object):
  def __init__(self,data,next):
    self.data=data
    self.next=next

n1 = Node('n1',None)
n2 = Node('n2',n1)
n3 = Node('n3',n2)
n4 = Node('n4',n3)
n5 = Node('n5',n4)

head = n5   # 链表的头节点
 
p1 = head   # 一次步进1个node
p2 = head   # 一次步进2个node

step = 0 
while (p2.next is not None and p2.next.next is not None):
  p2 = p2.next.next
  p1 = p1.next
  step = step + 1


print '快慢指针方式,单链表中间节点为:%s,索引为:%s，只遍历一次链表' % (p1.data,step)
    

