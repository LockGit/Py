# Python 

### ac.py 一个字符串搜索算法（tire树+AC自动机)
```
这个算法在实际场景中的确使用到了，判断某个单词是否是敏感词，这就涉及到字符串查找。
开发项目的时候,敏感词被封装成了一个api接口,开发人员使用起来也很方便,直接向api提交单词,
看返回结果就知道是否命中,命中了则字符串存在,表明查找到了。

隐约记得AC自动机，某种状态树结构，但是一直没有真正去看过这个接口实现。今天正好遇到了,剥离出来,复习知识点。
需要数据结构与算法知识：
参考文档1(海量数据处理之Tire树（字典树))：
      http://blog.csdn.net/ts173383201/article/details/7858598
参考文档2(AC自动机总结)：
      http://blog.csdn.net/mobius_strip/article/details/22549517

trie的核心思想是空间换时间,跟彩虹表的思想一致,但trie树不是彩虹表,
简而言之,trie树利用字符串的公共前缀来降低查询时间的开销以达到提高效率的目的。

它有3个基本性质：
      根节点不包含字符，除根节点外每一个节点都只包含一个字符。
      从根节点到某一节点，路径上经过的字符连接起来，为该节点对应的字符串。
      每个节点的所有子节点包含的字符都不相同。

复制了别人画的图，大致就是一种如下的树结构,问题还是在于如何用语言构造这棵树:
```
![](https://github.com/LockGit/Py/blob/master/img/tire.png)

```
fail 指针的理解图解,以下内容需要仔细读
参考：http://www.cnblogs.com/crazyacking/p/4659501.html
```
![](https://github.com/LockGit/Py/blob/master/img/ac_fail_pointer.png)

```
树上的词分别是：
{ he , hers , his , she}
按图所示分成3层。看到第三层，是"she"，其中：
①s指向root
②h先找到s的fail指针
发现是0号指针，不是h，然后h就不高兴了，再问问s的fail指针root：“你有没有儿子和我同名叫h的”
root说：“有，你指向他吧”，然后h就高兴的指向了第一行的h.
③e开始找了，首先问他老爸h：“你的fail指针指着谁”
h说：“图上第一行那个h啊”
然后e就屁颠屁颠地跑去问图上第一行那个h：“你有没有名字和我一样的儿子啊”
图上第一行那个h说：“有，他地址是xxx”
最后e的fail指针就指向xxx地址，也就是第一行那个e了
发现这样，如果一个字符串查到第三行的e以后的字符才不匹配，那说明他前面应该有个‘he’
刚好e的失败指针指向的是第一行的‘he...’的那个e；
这样就不用从h开始再找一遍，而是接着第一行的e继续往后找，从而节省了时间.
```

```
➜  ~ du -h word.md && wc -l word.md
1.0M  word.md
57193 word.md

本地测试了一下，57000条记录大于占1M硬盘空间，那么6M的空间大约包含记录34W条记录,
我传到github的word.md没有几个字符,只做了演示,而且每个单词还加了rank等级，\t制表符,实际占用空间应该更小,
生产环境甚至可以直接将这些数据缓存到内存中。
```
![](https://github.com/LockGit/Py/blob/master/img/cmd.png)
```
测试搜索指定字符串：

查找到了
➜  ~ python ac.py lock
Good ! Find it, the item is:
[(0, 3, 'lock', 1, 2)]

查找到了
➜  ~ python ac.py stop
Good ! Find it, the item is:
[(0, 3, 'stop', 2, 3)]

没有查找到
➜  ~ python ac.py test
Sorry, The item not in file dict

如果查找到了返回一个list，list中item类型为tuple, 并且包含了在树中匹配的起,终点位置index
```

### calc24.py 算24游戏小程序
```
游戏规则：给定4个数，可以执行的运算有 + - * / , 求出算的结果是24的算法过程

get help：
➜  Py git:(master) ✗ py calc24.py -h
Usage: usage -n 1,2,3,4

Options:
  -h, --help  show this help message and exit
  -n NUMS     specify num list
  
exp:
➜  Py git:(master) ✗ py calc24.py -n 10,8,9,4
[10, 8, 9, 4]
9 - 10 = -1
4 + -1 = 3
8 * 3 = 24
Success

or random test:
➜  Py git:(master) ✗ py calc24.py
[9, 10, 3, 6]
10 - 9 = 1
3 + 1 = 4
6 * 4 = 24
Success

~~~python轮子很强大~~~
```

### rpn.py 逆波兰表达式 python 版实现
```
逆波兰表达式被广泛应用于编译原理中，是一种是由波兰数学家扬·武卡谢维奇1920年引入的数学表达式方式，在逆波兰记法中，
所有操作符置于操作数的后面，因此也被称为后缀表示法。逆波兰记法不需要括号来标识操作符的优先级。
以利用堆栈结构减少计算机内存访问。
➜  Py git:(master) ✗ python rpn.py
['11111111111111', '9999999999999', '*', '99', '12', '4', '/', '-', '10', '+', '+']
True 111111111111098888888888995 111111111111098888888888995
True 326 326
```


### dispatch.py 轮转队列
```
你的手头上会有多个任务，每个任务耗时很长，而你又不想同步处理，而是希望能像多线程一样交替执行。

yield 没有逻辑意义，仅是作为暂停的标志点。程序流可以在此暂停，也可以在此恢复。而通过实现一个调度器，完成多个任务的并行处理。

通过轮转队列依次唤起任务，并将已经完成的任务清出队列，模拟任务调度的过程。
```

### coroutine.py 通过gevent第三方库实现协程
```
上面的dispatch.py通过yield提供了对协程的支持,模拟了任务调度。而下面的这个gevent第三方库就更简单了。

第三方的gevent为Python提供了比较完善的协程支持。通过greenlet实现协程，其基本思想是：
    当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。
    由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。

由于切换是在IO操作时自动完成，所以gevent需要修改Python自带的一些标准库，这一过程在启动时通过monkey patch完成：

依赖：
pip install gevent

执行：
➜  Py git:(master) ✗ python coroutine.py
GET: https://www.python.org/
GET: https://www.yahoo.com/
GET: https://github.com/
91430 bytes received from https://github.com/.
47391 bytes received from https://www.python.org/.
461975 bytes received from https://www.yahoo.com/.

```


### base64.py base64加密原理
```
Base64加密原理，使用Python实现Base64加密，可能有bug，未完全完善版
1,准备一个包含64个字符的数组
2,对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit
3,得到4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串
4,如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节,Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，
表示补了多少字节，解码的时候，会自动去掉。

Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%

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
原始报文        密文      加密            解密报文

12              17      1419857         12
15              15      759375          15
22              22      5153632         22
5               10      100000          5
```

### selenium.py 自动化测试demo
```
坑1：
  执行 python selenium.py 始终无法唤醒chrome。
  最终发现chromedriver很早之前安装的，没有进行：brew upgrade chromedriver，导致执行脚本时报错
  upgrade chromedriver 之后解决问题，官方文档说明了selenium支持好几个Browser driver。
  演示时用的是Chrome，python的unittest模块，文档上说也可以用pytest

大致支持这以下几种DOM查找,不同语言的接口略微的小区别
  driver.findElement(By.id(<element ID>))
  driver.findElement(By.name(<element name>))
  driver.findElement(By.className(<element class>))
  driver.findElement(By.tagName(<htmltagname>))
  driver.findElement(By.linkText(<linktext>))
  driver.findElement(By.partialLinkText(<linktext>))
  driver.findElement(By.cssSelector(<css selector>))
  driver.findElement(By.xpath(<xpath>))

支持Using Selenium with remote WebDriver
  支持远程WebDriver，默认监听4444端口
  启动：brew services start selenium-server-standalone
  停止：brew services stop selenium-server-standalone
  访问http://127.0.0.1:4444 点击console,
  新建正在测试所使用的webdriver,对于正在运行driver的测试程序，可以截图看当前测试程序的运行位置
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

### revert_list.py 反转链表
```
➜  Py git:(master) ✗ py revert_list.py
1
2
3
start revert list ...
3
2
1
```

### palindrome.py python版回文数，相对其他语言代码量少
```
life is short , use python
-(1)时间复杂度：O(n)，空间复杂度：O(1)。从两头向中间扫描
-(2)时间复杂度：O(n)，空间复杂度：O(1)。先从中间开始、然后向两边扩展
```
