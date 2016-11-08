#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2016/11/8 16:51


# RSA算法中加密方公布的密钥是n和e，解密方使用n和d解密

# p和q必须为素数，在实际运用中通常为很大的数
p = 5
q = 7

n = p * q
z = (p - 1) * (q - 1)

e = 5  # 加密方选择e，e必须和z只有一个公约数
d = 5  # (e * d - 1)必须能够被z整除 , 由于long int无法表示过大的数字，所以d取5


def run():
    raw_msg = [12, 15, 22, 5]
    en, de = [], []
    sec_code, de_msg = [], []
    print "下面是一个RSA加解密算法的简单演示:\n"
    print "报文\t加密\t   加密后密文\n"
    for item in raw_msg:
        en_key_item = pow(item, e)
        en.append(en_key_item)
        sec_code_item = en_key_item % n
        sec_code.append(sec_code_item)
        print "%d\t%d\t\t%d" % (item, en_key_item, sec_code_item)

    print "\n"
    print "---------------------------"
    print "----------执行解密---------"
    print "---------------------------"

    print "原始报文\t密文\t加密\t解密报文\n"
    for key,item in enumerate(sec_code):
        de_key_item = pow(item,d)
        de_msg_item = de_key_item % n
        de_msg.append(de_msg_item)
        print "%d\t\t%d\t%d\t\t%d" % (raw_msg[key], item, de_key_item, de_msg_item)

if __name__ == '__main__':
    run()



