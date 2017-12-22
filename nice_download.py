#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2017/12/21 18:28
# 多线程文件下载器,默认单线程

import sys
import optparse
import threading
import requests
import re
import time


class Download(object):
    def __init__(self, config_dict):
        self.url = config_dict['url']
        self.filename = self.clear_name(config_dict['url'].split('/')[-1])
        self.thread = config_dict['thread']
        self.user_agent = config_dict['user_agent']
        self.fileSize = 0
        self.supportThread = True
        self.show_print = (config_dict['show_print'] == 'yes') and True or False

    # 移除文件名的一些特殊字符
    def clear_name(self, filename):
        (filename, _) = re.subn(ur'[\\\/\:\*\?\"\<\>\|]', '', filename)
        return filename

    # 初始化目标文件信息
    def init_file_info(self):
        headers = {
            'User-Agent': self.user_agent,
            'Range': 'bytes=0-4'
        }
        try:
            r = requests.head(self.url, headers=headers)
            rang_content = r.headers['content-range']
            self.fileSize = int(re.match(ur'^bytes 0-4/(\d+)$', rang_content).group(1))
            return True
        except Exception, e:
            print 'can not support breakpoint download,msg:%s' % (e.message,)

        try:
            self.fileSize = int(r.headers['content-length'])
        except Exception, e:
            self.supportThread = False
            print 'can not support multi thread download , error:%s' % (e.message,)
        return False

    def start_part_download(self, thread_id, start_index, stop_index):
        try:
            headers = {'Range': 'bytes=%d-%d' % (start_index, stop_index,), 'User-Agent': self.user_agent}
            r = requests.get(self.url, headers=headers, stream=True, allow_redirects=True)
            if r.status_code == 206:
                with open(self.filename, "rb+") as fp:
                    fp.seek(start_index)
                    fp.write(r.content)
            if self.show_print:
                sys.stdout.write('thread %s download part size:%.2f KB\n' % (thread_id, (r.content.__len__()) / 1024))
                sys.stdout.flush()
        except Exception, e:
            if self.show_print:
                sys.stdout.write('下载出现错误,错误位置:%s,状态码:%s,错误信息:%s\n' % (start_index, r.status_code, e.message))
                sys.stdout.flush()

    def run(self):
        print 'Start...'
        start_time = time.time()
        self.init_file_info()
        # 创建一个和要下载文件一样大小的文件
        with open(self.filename, "wb") as fp:
            fp.truncate(self.fileSize)

        if self.fileSize > 0:
            if self.supportThread is False and self.thread > 1:
                print 'sorry,only support single thread'
                self.thread = 1
            print 'Thread count is:%s' % (self.thread,)
            part = self.fileSize / self.thread
            for i in xrange(0, self.thread):
                start_index = part * i
                stop_index = start_index + part
                if i == self.thread - 1:
                    stop_index = self.fileSize
                download_args = {'thread_id': i, 'start_index': start_index, 'stop_index': stop_index}
                worker = threading.Thread(target=self.start_part_download, kwargs=download_args)
                worker.setDaemon(True)
                worker.start()
            # 等待所有线程下载完成
            main_thread = threading.current_thread()
            for t in threading.enumerate():
                if t is main_thread:
                    continue
                t.join()
            print 'Success.\nTime:%.2fs , Size:%.2fKB' % (time.time() - start_time, self.fileSize / 1024)
        else:
            print 'Can not download'


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='python %s.py [options]' % (sys.argv[0],))
    parser.add_option('-u', dest='url', type='string', help='specify download resource url')
    parser.add_option('-t', dest='thread', type='int', help='specify download thread count', default=1)
    parser.add_option('-p', dest='show_print', type='string', help='yes/no,show print info,default enable', default='yes')
    parser.add_option("-a", dest="user_agent", help="specify request user agent", default='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0')
    (options, args) = parser.parse_args()
    if options.url is None:
        parser.print_help()
        exit()
    config = {
        'url': options.url,
        'thread': options.thread,
        'user_agent': options.user_agent,
        'show_print': options.show_print
    }
    try:
        Download(config).run()
    except KeyboardInterrupt:
        print '\nCancel Download'
