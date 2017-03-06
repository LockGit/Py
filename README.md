# Python 

### dispatch.py 轮转队列
```
你的手头上会有多个任务，每个任务耗时很长，而你又不想同步处理，而是希望能像多线程一样交替执行。

yield 没有逻辑意义，仅是作为暂停的标志点。程序流可以在此暂停，也可以在此恢复。而通过实现一个调度器，完成多个任务的并行处理。

通过轮转队列依次唤起任务，并将已经完成的任务清出队列，模拟任务调度的过程。
```


### base64.py base64加密原理
```
Base64加密原理，使用Python实现Base64加密，可能有bug，未完全完善版
例：
➜  Py git:(master) ✗ python base64.py lock
bG9jaw==
➜  Py git:(master) ✗ echo -n lock|base64
bG9jaw==

```

### rsa.py RSA算法演示
```
➜  py python rsa.py
下面是一个RSA加解密算法的简单演示:

报文    加密       加密后密文

12      248832          17
15      759375          15
22      5153632         22
5       3125            10


---------------------------
----------执行解密---------
---------------------------
原始报文        密文    加密    解密报文

12              17      1419857         12
15              15      759375          15
22              22      5153632         22
5               10      100000          5
```

### Python 沙箱逃逸
```
重温2012.hack.lu的比赛题目，在这次挑战中，需要读取'./1.key'文件的内容。
他们首先通过删除引用来销毁打开文件的内置函数。然后它们允许您执行用户输入。看看他们的代码稍微修改的版本：

def make_secure():
    UNSAFE = ['open',
              'file',
              'execfile',
              'compile',
              'reload',
              '__import__',
              'eval',
              'input']
    for func in UNSAFE:
        del __builtins__.__dict__[func]
from re import findall
# Remove dangerous builtins
make_secure()
print 'Go Ahead, Expoit me >;D'
while True:
    try:
        # Read user input until the first whitespace character
        inp = findall('\S+', raw_input())[0]
        a = None
        # Set a to the result from executing the user input
        exec 'a=' + inp
        print 'Return Value:', a
    except Exception, e:
    print 'Exception:', e
由于没有在__builtins__中引用file和open，所以常规的编码技巧是行不通的。但可以在Python解释器中挖掘出另一种代替file或open引用的方法。

另类读取文件的方式：
().__class__.__bases__[0].__subclasses__()[40]('1.key').read()
这个方法依然可以读取到1.key的内容，coder,hack,geek可以深入了解下，本人测试时的python版本为：Python 2.7.12
```

