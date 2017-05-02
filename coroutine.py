# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-05-03 00:06:17
# @Last Modified by:   lock
# @Last Modified time: 2017-05-03 00:06:22
from gevent import monkey; monkey.patch_all()
import gevent
import urllib2

def f(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))

gevent.joinall([
        gevent.spawn(f, 'https://www.python.org/'),
        gevent.spawn(f, 'https://www.yahoo.com/'),
        gevent.spawn(f, 'https://github.com/'),
])