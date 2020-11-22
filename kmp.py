# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-14 18:08:13
# @Last Modified by:   lock
# @Last Modified time: 2017-12-14 23:31:06


# 只是字符串匹配，还不是真正的kmp
def kmp(string, match):
    n = len(string)
    m = len(match)
    i = 0
    j = 0
    count_times_used = 0
    while i < n:
        count_times_used += 1
        if match[j] == string[i]:
            if j == m - 1:
                print "Found '%s' start at string '%s' %s index position, find use times: %s" % (match, string, i - m + 1, count_times_used,)
                return
            i += 1
            j += 1
        elif j > 0:
            j = j - 1
        else:
            i += 1

kmp("asfdehhaassdsdasasedwa", "sase")
kmp("12s3sasexxx", "sase")
