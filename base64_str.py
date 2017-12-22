# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2016-09-14 00:33:53
# @Last Modified by:   lock
# @Last Modified time: 2016-09-14 00:49:09
import string
import sys
def get_payloads():
    payloads = list(string.ascii_uppercase)
    payloads = payloads + list(string.ascii_lowercase)
    for i in xrange(0,10):
        payloads.append(i)
    payloads.extend(['+','-'])
    return payloads

def encode(s):
    if s=='':
        return ''
    if len(s)%3==1:
        s = s+'00'
    elif len(s)%3==2:
        s = s+'0'
    bin_code,tmp = [],[]
    for i in xrange(0,len(s),3):
        code = s[i:i+3]
        for j in code:
            if j=='0':
                bin_code.append('0'*8*len(j))
            else:
                bin_code.append(bin(ord(j)).replace('0b','0')) # 10进制 to 2进制

    base_str = ''.join(map(str,bin_code))
    translate_list = []
    for bit in xrange(0,len(base_str),6):
        split_code = base_str[bit:bit+6]
        translate_list.append(str(int(split_code,2))) #二进制 to 十进制
    payloads = get_payloads()
    for i in translate_list:
        if i=='0':
            tmp.append('=')
        else:
            tmp.append(payloads[int(i)])
    return ''.join(map(str,tmp))

def help():
    print 'args error!\nexample:\n\tpython base64.py lock'
    exit()

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 2 or len(args)==1:
        help()
    print(encode(s = args[1]))
