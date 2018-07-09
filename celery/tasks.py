#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2018/5/2 11:19

from celery import Celery

app = Celery('TASK', broker='redis://127.0.0.1', backend='redis://127.0.0.1')


@app.task
def add(x, y):
    print 'start ...'
    print 'get param :%s,%s' % (x, y,)
    return x + y
