# Python 

### nice_download.py 多线程文件下载器
```
理论在大型文件下载，带宽充足的情况下，可增加数十倍下载速度
原理是多线程对目标文件分块下载
1,发送head请求获取目标文件总大小，以及当前是否支持分块下载(详情:http协议header头range及response的content-range)，现在基本都支持
2,下载前创建一个和要下载文件一样大小的文件
3,根据1中获得的文件大小分块多线程,各个线程下载不同的数据块
小型文件可能看不出加速效果，在大型文件上就会拉大差距
关于http的range特性：
有些文件下载器在下载中断之后可以在中断位置继续下载，而不必重新开始的原因就是利用了支持range的特性
记录了中断时的文件偏移位置,在实现时只要在中断异常的时候记录文件偏移位置到临时文件
下次继续下载读取临时文件中的偏移即可支持断点下载,下载完成时删除记录文件偏移的临时文件即可
说明：
nice_download.py是多线程模式,所以去除断点下载功能，否则维护临时文件偏移位置比维护单一进程的临时文件偏移位置要复杂的多
查看帮助：python nice_download.py -h
```
![](https://github.com/LockGit/Py/blob/master/img/download.gif)


### 基于tensorflow的验证码识别
```
依赖:
pip install tensorflow
pip install numpy

0x01,cd tensorflow
0x02,模型训练：python train.py
0x03,验证验证：python cnn_test.py

已有大多相关案例，测试相关总结与截图如下:
```
![](https://github.com/LockGit/Hacking/blob/master/img/cnn_test.png)
[详相说明相关截图](https://github.com/LockGit/Hacking#基于机器学习tensorflow的复杂验证码识别)
总结文档：[基于机器学习(TensorFlow)的复杂验证码识别.pdf](https://github.com/LockGit/Hacking/blob/master/res/doc/基于机器学习(TensorFlow)的复杂验证码识别.pdf)


### ac.py 字符串搜索算法（tire树+AC自动机)
```
学习记录:
如果你的本地只有几个，几十个词，那么没有必要使用，直接存配置文件，字典查找即可，
这比向api发起http请求要快的多。但如果词的数目不断增加，那么后期将不利于维护，
需要服务化。

这个算法存在于实际场景,判断某个单词是否是敏感词，就涉及到字符串查找。
敏感词被封装成了一个api接口,使用起来也很方便,直接向api提交单词,
看返回结果就知道是否命中,命中了则字符串存在,表明查找到了。

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

复制了别人画的图，大致就是一种如下的树结构,需要用语言构造这棵树即可:
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


### dispatch.py 轮转队列 | 协程实现
```
你的手头上会有多个任务，每个任务耗时很长，而你又不想同步处理，而是希望能像多线程一样交替执行。
yield 没有逻辑意义，仅是作为暂停的标志点。
程序流可以在此暂停，也可以在此恢复。而通过实现一个调度器，完成多个任务的并行处理。
通过轮转队列依次唤起任务，并将已经完成的任务清出队列，模拟任务调度的过程。
核心代码：
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


### base64_str.py base64编码原理
```
base64编码原理，使用Python实现base64编码，可能有bug，未完全完善版
1,准备一个包含64个字符的数组
2,对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit
3,得到4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串
4,如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节,Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，
表示补了多少字节，解码的时候，会自动去掉。

Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%

例：
➜  Py git:(master) ✗ python base64_str.py lock
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


### kmp.py   kmp字符串查找算法
```
➜  Py git:(master) ✗ python kmp.py
Found 'sase' start at string 'asfdehhaassdsdasasedwa' 15 index position, find use times: 23
Found 'sase' start at string '12s3sasexxx' 4 index position, find use times: 9

核心算法：
def kmp(string, match):
    n = len(string)
    m = len(match)
    i = 0
    j = 0
    count_times_used = 0
    while i < n:
        count_times_used += 1
        if match[j] == string[i]:
            if j == m - 1:
                print "Found '%s' start at string '%s' %s index position, find use times: %s" % (match, string, i - m + 1, count_times_used,)
                return
            i += 1
            j += 1
        elif j > 0:
            j = j - 1
        else:
            i += 1
```


### compress.py 字符串压缩
```
针对连续重复较多的字符压缩，否则不起压缩效果
➜  Py git:(master) ✗ python compress.py
原始字符串:xAAACCCBBDBB111
压缩后:x1A3C3B2D1B213
执行解压...
x
A
A
A
C
C
C
B
B
D
B
B
1
1
1
解压完毕
解压后:xAAACCCBBDBB111
```

### hashtable.py  hash表实现
```
hash_table = HashTable(5); # 分配5块
hash_table.set(1,'x')
print hash_table.get(1)

核心代码：
class Item(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable(object):
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in xrange(self.size)]

    def hash_function(self, key):
        return key % self.size

    def set(self, key, value):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                item.value = value
                return
        self.table[hash_index].append(Item(key, value))

    def get(self, key):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                return item.value
        return None

    def remove(self, key):
        hash_index = self.hash_function(key)
        for i, item in enumerate(self.table[hash_index]):
            if item.key == key:
                del self.table[hash_index][i]
```


### interpreter.py Python解释器理解
```
Python会执行其他3个步骤：词法分析，语法解析和编译。
这三步合起来把源代码转换成code object,它包含着解释器可以理解的指令。而解释器的工作就是解释code object中的指令。
核心代码
class Interpreter:
    def __init__(self):
        self.stack = []

    def load_value(self, number):
        self.stack.append(number)

    def print_answer(self):
        answer = self.stack.pop()
        print(answer)

    def add_two_values(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def run_code(self, what_to_execute):
            instructions = what_to_execute["instructions"]
            numbers = what_to_execute["numbers"]
            for each_step in instructions:
                instruction, argument = each_step
                if instruction == "load_value":
                    number = numbers[argument]
                    self.load_value(number)
                elif instruction == "add_two_values":
                    self.add_two_values()
                elif instruction == "print_answer":
                    self.print_answer()
```


### linked_list.py 快速查找单链表中间节点
```
➜  Py git:(master) py linked_list.py
普通遍历方式,单链表中间节点为:n3,索引为:2，遍历一次链表，在从0遍历到中间位置
快慢指针方式,单链表中间节点为:n3,索引为:2，只遍历一次链表

核心代码：
class Node(object):
  def __init__(self,data,next):
    self.data=data
    self.next=next

n1 = Node('n1',None)
n2 = Node('n2',n1)
n3 = Node('n3',n2)
n4 = Node('n4',n3)
n5 = Node('n5',n4)

head = n5   # 链表的头节点

p1 = head   # 一次步进1个node
p2 = head   # 一次步进2个node

step = 0
while (p2.next is not None and p2.next.next is not None):
  p2 = p2.next.next
  p1 = p1.next
  step = step + 1
print '快慢指针方式,单链表中间节点为:%s,索引为:%s，只遍历一次链表' % (p1.data,step)
```

### K最近邻算法
```
这个算法比svm简单很多
只需使用初中所学的两点距离公式（欧拉距离公式），计算目标点到各组的距离，看绿点和哪组更接近。
k代表取当前要分类的点最近的k个点，这k个点如果其中属于红点个数占多数，我们就认为绿点应该划分为红组，反之，则划分为黑组。
k值与分类数成正相关，现在是2个分组，那么k值取3，假设是3个分组，那么k值就要取5
参考说明：https://zh.wikipedia.org/wiki/最近鄰居法
依赖：
pip install numpy
pip install matplotlib

下图中标注较大的红点在计算之后被分配到红组
执行：python knn.py
```
![](https://github.com/LockGit/Py/blob/master/img/knn.png)


### 支持向量机 svm.py
```
迟早会忘记的svm
属分类算法，目标是寻找一个最优超平面，比knn算法复杂
demo为线性可分离数据

参考1：https://zh.wikipedia.org/zh-hans/支持向量机
参考2：http://blog.csdn.net/viewcode/article/details/12840405
参考3：http://blog.csdn.net/lisi1129/article/details/70209945?locationNum=8&fps=1

依赖：
pip install numpy
pip install matplotlib

执行：python svm.py
```
![](https://github.com/LockGit/Py/blob/master/img/svm.png)


### (前序，中序，后序，层序) btree.py
```
➜  Py git:(master) ✗ python btree.py
前序遍历： root A C D F G B E
中序遍历： C F D G A root B E
后序遍历： F G D C A E B root
层序遍历： root A B C E D F G
构造树结构如下图
```
![](https://github.com/LockGit/Py/blob/master/img/btree.png)


### Scrapy 爬虫测试
```
安装依赖：
pip install Scrapy 
pip install sqlalchemy 
pip install sqlacodegen
pip install mysql-connector

创建db：CREATE DATABASE crawl DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci

创建表：crawl_360/readme/sql.sql 文件

sqlacodegen创建models：
sqlacodegen --outfile=models.py mysql://root@localhost:3306/crawl --tables butian


找测试的目标抓取页面：http://butian.360.cn/Loo 页面被披露漏洞的企业列表

创建项目: scrapy startproject crawl_360

目录结构:
➜  crawl_360 tree
.
├── crawl_360
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── items.py
│   ├── items.pyc
│   ├── middlewares.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __init__.pyc
│   │   ├── db.py
│   │   ├── db.pyc
│   │   ├── models.py
│   │   └── models.pyc
│   ├── pipelines.py
│   ├── pipelines.pyc
│   ├── reademe
│   │   └── sql.sql
│   ├── settings.py
│   ├── settings.pyc
│   └── spiders
│       ├── __init__.py
│       ├── __init__.pyc
│       ├── butian.py
│       └── butian.pyc
└── scrapy.cfg

生成一个爬虫：
cd crawl_360 && scrapy genspider butian butian.360.cn/Loo

编写爬虫代码 (xpath代码30多行)

爬取：scrapy crawl butian

另：selenium也是一款非常不错的工具，可是使用selenium调用Browser driver更加逼真真实用户操作
```

