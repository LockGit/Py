#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# Created by Vim
from random import choice
import random
import sys

def calc_red_package(m,c):
	if c*0.01*100>m:
		print '红包总金额为:%s元不能划分成%s个红包'%(m/100.0,c,)
		exit()
		
	all = {}
	val = m/c
	left = m-(val*c)
	for i in range(0,c):
		all[i] = [1,val]

	if left>0:
		rand = random.randint(0,c-1)
		all[rand].append(all[rand][-1]+left)

	pos = {}
	for index in all:
		stop=random.randint(0,val)
		pos[index] = stop

	res = []

	if len(pos)>=2:
		for point in pos:
			left = pos[point]
			if left==0:
				left=1
			if point==0:
				res.append(left/100.0)
				last_right = all[point][-1]-left
			else:
				right = last_right
				if point==(c-1):
					res.append((left+right)/100.0)
					end = all[point][-1]-left
					randMax = random.randint(0,len(res)-1)
					res[randMax] = (res[randMax]*100 + end)/100.0
				else:
					res.append((left+right)/100.0)
					last_right = all[point][-1]-left
	else:
		res.append((all[0][-1])/100.0)

	print res

	for key,item in enumerate(res):
		print '第 %s 个红包金额:%s元' %(key+1,item)
	print '验证:红包总金额 is %s元, 分配后 res sum is %s元'%(m/100.0,sum(res),)


if __name__ == '__main__':
	m = 1000 # 红包金额，单位：分
	c = 4 # 红包个数
	if len(sys.argv)==3:
		m = int(float(sys.argv[1])*100)
		c = int(sys.argv[2])
	calc_red_package(m,c)



