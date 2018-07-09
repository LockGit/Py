# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-06-09 22:48:14
# @Last Modified by:   lock
# @Last Modified time: 2018-06-29 12:38:35
# -*- coding: utf-8 -*-
import optparse
import itertools
import random


# 洗牌
def shuffle(n, m=-1):
    if m == -1:
        m = n
    l = range(n)
    for i in range(len(l) - 1):
        x = random.randint(i, len(l) - 1)
        l[x], l[i] = l[i], l[x]
        if i == m - 1:
            break
    return [l[idx] for idx in range(n) if idx >= 0 and idx < m]


# 生成4张牌
def Get4Card():
    card = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
    cardidxs = shuffle(52, 4)
    return [card[idx] for idx in cardidxs]


def GenAllExpr(card_4, ops_iter):
    try:
        while True:
            l = list(ops_iter.next()) + card_4
            its = itertools.permutations(l, len(l))
            try:
                while True:
                    yield its.next()
            except StopIteration:
                pass
    except StopIteration:
        pass


def CalcRes(expr, isprint=False):
    opmap = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b,
             '/': lambda a, b: a / (b + 0.0)}
    expr_stack = []
    while expr:
        t = expr.pop(0)
        if type(t) == int:
            expr_stack.append(t)
        else:
            if len(expr_stack) < 2:
                return False
            else:
                a = expr_stack.pop()
                b = expr_stack.pop()
                if isprint:
                    print a, t, b, '=', opmap[t](a, b)
                try:
                    expr_stack.append(opmap[t](a, b))
                except ZeroDivisionError:
                    return False
    return expr_stack[0]


if __name__ == "__main__":
    parser = optparse.OptionParser('usage -n 1,2,3,4')
    parser.add_option('-n', dest='nums', type='string', help='specify num list')
    (options, args) = parser.parse_args()
    nums = options.nums
    if nums is None:
        input_card = Get4Card()
    else:
        input_card = [int(x) for x in nums.split(',')]
    card = input_card
    if len(input_card) != 4:
        print(parser.usage)
        exit(0)
    print card
    ops = itertools.combinations_with_replacement('+-*/', 3)  # 一个24点的计算公式可以表达成3个操作符的形式
    allexpr = GenAllExpr(card, ops)  # 数和操作符混合，得到所有可能序列
    for expr in allexpr:
        res = CalcRes(list(expr))
        if res and res == 24:
            CalcRes(list(expr), True)  # 输出计算过程
            print "Success"
            break
