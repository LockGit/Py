# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-15 00:11:32
# @Last Modified by:   lock
# @Last Modified time: 2017-12-15 00:34:55


def compress(string):
    compressed = []
    count = 0
    temp = string[0]

    for i in range(0, len(string)):
        if temp == string[i]:
            count = count + 1
        else:
            compressed.append(str(temp) + str(count))
            count = 1
            temp = string[i]

        if i == len(string) - 1:
            compressed.append(str(temp) + str(count))

    return ''.join([str(x) for x in compressed])


def decompress(string):
	print '执行解压...'
	decompress_list = []
	for j in xrange(0, len(string) - 1):
		if j % 2 == 0:
			for i in xrange(0, int(string[j + 1])):
				decompress_list.append(string[j])
				print string[j]
	print '解压完毕'
	return ''.join(decompress_list)

def main():
    string = "xAAACCCBBDBB111"
    print '原始字符串:%s' % (string,)
    print '压缩后:%s' % (compress(string),)
    print '解压后:%s' % (decompress(compress(string)),)

if __name__ == '__main__':
    main()
