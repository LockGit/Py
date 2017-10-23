# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-06-25 00:48:56
# @Last Modified by:   lock
# @Last Modified time: 2017-06-25 01:39:49

# 时间复杂度：O(n)，空间复杂度：O(1)。从两头向中间扫描

s = "abcmnmcba"


def check(s):
    start = 0
    end = len(s) - 1
    while start < end:
        if s[start:start + 1] != s[end:end + 1]:
            print s[start:start + 1] + '---' + s[end:end + 1]
            return False
        start = start + 1
        end = end - 1
    return True

# print check(s)


s2 = '12311211321'

# 时间复杂度：O(n)，空间复杂度：O(1)。先从中间开始、然后向两边扩展
def check2(s):
    if len(s) % 2 == 0:
        mid = len(s) / 2
        start, end = mid - 1, mid
    if len(s) % 2 == 1:
        mid = len(s) / 2
        start, end = mid - 1, mid+1
    while mid > 0:
        if s[start:start+1] != s[end:end+1]:
            return False
        start = start - 1
        end = end + 1
        mid = mid - 1
    return True

print check2(s2)
