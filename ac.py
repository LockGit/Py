# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-05-08 16:32:38
# @Last Modified by:   lock
# @Last Modified time: 2017-05-08 22:48:16
import time
import logging
import sys

log = logging.getLogger('dict_word')


_word_cells = {}
#预先生成好组成单词的字符
for c in [chr(i) for i in range(ord('a'), ord('z') + 1)]:
    _word_cells[unicode(c)] = 1
for c in [chr(i) for i in range(ord('A'), ord('Z') + 1)]:
    _word_cells[unicode(c)] = 1
for c in [chr(i) for i in range(ord('0'), ord('9') + 1)]:
    _word_cells[unicode(c)] = 1


#固定的英文单词组成部分
_word_cells[u'_'] = 1
_word_cells[u'-'] = 1

# 缓存
_cache = {
    'acm': None,
    'load_time': 0
}

#词默认等级
DEFAULT_RANK=1


def isWordCell(a):
    '''
    当前字符是否为单词的非边界,或者是组成部分
    :param a:
    :return:
    '''
    return a in _word_cells



class Node(object):
    '''
    Node树节点
    :next : 用dict字典结构模拟动态链表
    :fail : 辅助初始值None
    :param isWord : 当前树节点是否为存在的单词
    :param rank : 等级
    '''
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.rank = 0


class Ahocorasick(object):
    def __init__(self):
        self.__root = Node()


    def make(self):
        '''
        build the fail function
        构建自动机，失效函数
        '''
        tmpQueue = []
        tmpQueue.append(self.__root)
        while (len(tmpQueue) > 0):
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if p.next.has_key(k):
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None:
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])


    def addWord(self, word, rank=1,line=0):
        '''
        @param word: add word to Tire tree
        添加关键词到Tire树中
        '''
        word = word.lower()
        tmp = self.__root
        for i in range(0, len(word)):
            if not tmp.next.has_key(word[i]):
                tmp.next[word[i]] = Node()
            tmp = tmp.next[word[i]]
        tmp.isWord = True
        tmp.rank = rank
        tmp.line = line


    def search(self, content):
        '''
        @return  如果查找到了返回一个list，list中item类型为tuple, 并且包含了匹配的起,终点位置index
        '''
        #不区分大小写
        raw_content=content
        content = content.lower()

        p = self.__root
        result = []
        startWordIndex = 0
        endWordIndex = -1
        currentPosition = 0

        content_len = len(content)
        while currentPosition < content_len:
            word = content[currentPosition]
            #print 'word:', word
            # 检索状态机，直到匹配
            while p.next.has_key(word) == False and p != self.__root:
                p = p.fail

            if p.next.has_key(word):
                if p == self.__root:
                    # 若当前节点是根且存在转移状态，则说明是匹配词的开头，记录词的起始位置
                    startWordIndex = currentPosition
                # 转移状态机的状态
                p = p.next[word]
            else:
                p = self.__root

            if p.isWord:
                # 若状态为词的结尾，则把词放进结果集
                # 判断当前这些位置是否为单词的边界
                if startWordIndex > 0 and isWordCell(content[startWordIndex - 1]) and isWordCell(content[startWordIndex]):
                    # 当前字符和前面的字符都是字母,那么它是连续单词
                    # print '前面不是单词边界', [startWordIndex > 0, str(content[startWordIndex - 1].encode('utf-8')),isWordCell(content[startWordIndex - 1]),str(content[startWordIndex].encode('utf-8')),isWordCell(content[startWordIndex])]
                    currentPosition += 1
                    continue

                if currentPosition < content_len - 1 and isWordCell(content[currentPosition + 1]) and isWordCell(content[currentPosition]):
                    # print '后面不是单词边界'
                    currentPosition += 1
                    continue

                result.append((startWordIndex, currentPosition, raw_content[startWordIndex:currentPosition + 1], p.rank,p.line))

            currentPosition += 1
        return result



def load_acm(filename):
    '''
    加载词表
    :param filename:
    :return:
    词表 分为很多行 
    每行 有2列组成
    词 [tab] 等级
    exp:
    sharen [\t]  2
    '''
    import os.path

    mtime = os.path.getmtime(filename)
    if _cache['load_time'] < mtime or _cache['acm'] is None:
        log.info('start load data')
        _cache['load_time'] = mtime
        start_time = time.time()
        acm = Ahocorasick()

        with open(filename) as fp:
            line_count = 0
            for line in fp:
                line_count += 1
                w = line.strip().decode('utf-8')
                arr2 = w.split('\t')
                # 默认等级
                if len(arr2) == 1:
                    arr2.append(DEFAULT_RANK)
                try:
                    acm.addWord(arr2[0], int(arr2[1]), line_count)
                except Exception as e:
                    print 'error', e
                    print 'line', line_count, line
        acm.make()
        _cache['acm'] = acm
        log.info('load ok time:%.2f' % (time.time() - start_time))
    else:
        # print 'hit cache'
        pass
        

    return _cache['acm']

def help():
    print "example: python ac.py str\n"


if __name__ == '__main__':

    args = sys.argv
    if len(args) != 2:
        help()
        exit()

    # 预加载
    acm = load_acm('./word.md')
    # 指定搜索的文本
    content = args[1]
    search_result = acm.search(content)
    if len(search_result) > 0:
        print 'Good ! Find it, the item is:\n%s'%(search_result)
    else:
        print 'Sorry, The item not in file dict'

