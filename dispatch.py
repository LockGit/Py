# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2016-05-18 23:47:54
# @Last Modified by:   lock
# @Last Modified time: 2016-05-18 23:47:54
from collections import deque
class Runner(object):
    def __init__(self, tasks):
        self.tasks = deque(tasks)

    def next(self):
        return self.tasks.pop()

    def run(self):
        while len(self.tasks):
            task = self.next()
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.tasks.appendleft(task)

def task(name, times):
    for i in range(times):
        yield
        print(name, i)

Runner([
    task('hsfzxjy', 5),
    task('Jack', 4),
    task('Bob', 6)
]).run()
