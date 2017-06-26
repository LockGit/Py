# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-06-26 15:51:28
# @Last Modified by:   lock
# @Last Modified time: 2017-06-26 15:55:53
def calc(s):
    if type(s) != list:s = s.split(' ')
    operaList = ['+', '-', '*', '/'];
    for key, item in enumerate(s):
        if item in operaList:
            val = eval(s[key - 2] + item + s[key - 1])
            s.insert(key - 2, str(val)) 
            for x in ['1','2','3']:del s[key - 1] 
            calc(s)
    return sum(map(eval, s))
def translate(calcStr):
    element, calcList,s,stackStr,i = '', [],[],[],0
    for key,item in enumerate(calcStr):
        if item.isdigit():
            element = element + item
            if key == len(calcStr)-1:calcList.append(element)
        else:
            if element != '':
                calcList.append(element)
                element = ''
            if item in ['+', '-', '*', '/', '(', ')']:
                calcList.append(item)
    calcList.insert(0,'(')
    calcList.append(')')
    calcList.append('#')
    while calcList[i] != "#":
        if (calcList[i].isdigit()):
            stackStr.append(calcList[i])
        elif calcList[i] == '(':
            s.append(calcList[i])
        elif calcList[i] == ')':
            while s[-1] != '(':
                stackStr.append(s.pop())
            s.pop()
        elif calcList[i] in ['+', '-']:
            while s[-1] != '(':
                stackStr.append(s.pop())
            s.append(calcList[i])
        elif calcList[i] in ['*', '/']:
            while s[-1] in ['*', '/']:
                stackStr.append(s.pop())
            s.append(calcList[i])
        i = i + 1
    return stackStr
if __name__ == '__main__':
    s = '11111111111111*9999999999999+(99-(12/4)+10)'
    print translate(s)
    print str(calc(translate('11111111111111*9999999999999+(99-(12/4)+10)'))) == str(11111111111111*9999999999999+(99-(12/4)+10)),str(calc(translate(s))) , str(11111111111111*9999999999999+(99-(12/4)+10))
    print str(calc(translate('12+1+12+33*9+4'))) == str(12+1+12+33*9+4),str(calc(translate('12+1+12+33*9+4'))) , str(12+1+12+33*9+4)



