这篇文章记录在学习Python爬虫过程中遇到的标准库与第三方库
___

## <a name="index"/>目录
* [urllib](#one)
    * urlencode()
* [urllib2](#two)
    * urlopen()
    * Request()
    * URLError
    * HTTPError
* [BeautifulSoup](#three)
    



## <a name="one"/>urllib
#### urllib.urlencode(query[, doseq])
format需要传给Request的data
```Python
values = {'name':'WHY',
         'location':'SDU',
         'language':'Python'}

# data == name=WHY&location=SDU&language=Python
data = urlencode(values) 
```

## <a name="one"/>urllib2
#### urllib2.urlopen(url[, data][, proxies][, context])
receive an url and fetch all the source codes from a given web page.
```Python
req = Request('https://zhihu.com')
response = urlopen(req).read()
```


提交data有两种方式：**GET method** 和 **POST method**          
* **GET request**: 直接将需要传给server的data附到url上     
```Python
# data == name=WHY&location=SDU&language=Python
request = urlopen('http://www.someserver.com/register.cgi?%s' % data).read()
```
* **POST request**: 通过urllib2.Request method将data传给server
```Python
# data == name=WHY&location=SDU&language=Python
req = Request('http://www.someserver.com/register.cgi', data)
request = urlopen(req).read()
```

urlopen()返回的response/或者HTTPError有两个method: **info**, **geturl**                        
* **geturl()**: 返回真实的URL, 这个很有用，因为urlopen(或者opener对象使用的)或许会有重定向。获取的URL或许跟请求URL不同。
```Python
old_url = 'http://rrurl.cn/b1UZuP'  
req = Request(old_url)  
response = urlopen(req)    
print 'Real url :' + response.geturl() 
```
* **info()**: 返回请求所需要的headers 
```Python
raw_url = 'https://www.baidu.com'
response = urlopen(raw_url)
print response.info() 
```

#### urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable]):
* 比起直接通过urlopen fetch codes, 建议先通过urllib2.Request封装。 
* data通常为username and password，需要用urllib.urlencode格式化
* 发送request时需要模仿浏览器发送request的行为（避免被封）。这就需要向server提供request header。主要是三方面：**host(主机)**， **referer(所在链接)**， **user-agent(客户端代号)**    
```Python
# add headers to urllib2.Request
headers = {
          'Host':'http://www.baidu.com',
          'Referer':'http://baidu.com/',
          'User-Agent':'Mozilla/5.0'
          }
req = Request('http://www.baidu.com', headers = headers)
response = urlopen(req).read()

# or use add_header method
# ...
req = Request('http://www.baidu.com')
for key in headers:
    req.add_header(key, headers[key])
response = urlopen(req).read()    
```

#### URLError
* 产生原因：     
    * 没有网络连接，即无法上网    
    * 没有路由到特定服务器     
    * 服务器不存在异常      
 
* **URLError**有attribute`reason`，是一个tuple：
```Python
req = Request('http://www.baibai.com')
try:
    urlopen(req)
except URLError as e:
    print e
    # <urlopen error [Errno -2] Name or service not known> 
    print e.reason
    # [errno -2] Name or service not known
```

#### HTTPError     
1. 在利用urlopen方法发出一个请求时，服务器上都会对应一个应答对象response和一个状态码，urllib2会处理response(如要求重定向），如处理不了的，返回HTTPError。
2. 因为默认的处理器处理了重定向(300+号码)，并且100-299范围的号码指示成功，所以只能看到400-599的错误号码（状态码）。
3. classic的错误代码有: "404:page not found", "403: request forbidden", "401: need request authorization"。

**HTTPError**有attribute`code`，是一个integer：
```Python
try:
    urlopen('http://bbs.csdn.net/callmewhy')
except HTTPError as e:
    print e
    # HTTP Error 403: Forbidden
    print 'Error code:', e.code 
    # Error code: 403
```
**HTTPError**是**URLError**的子类，错误处理时如果两个Error需要同时存在，则子类一定要放在父类的前面，不然会被包含被覆盖。或者可以这么处理：
```Python
try:
    urlopen('http://bbs.csdn.net/callmewhy')
except URLError as e:
    if hasattr(e, 'code'):
        print 'Error code:', e.code
    elif hasattr(e, 'reason'):
        print 'Reason', e.reason
else:
    print 'No exceptions were raised' 
```


## <a name="three"/>BeautifulSoup
#### 官方简介      
Beautiful Soup is a **Python library** for **pulling data out of HTML and XML files**. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree.

#### 安装            
在terminal中键入：
```
(venv)$ pip install beautifulsoup4
```

#### 教程                  
##### 作为演示的source code:
```html
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
```

##### 创建beautifulsoup对象的方法：
```Python
soup = BeautifulSoup(html)

# or从本地创建：
soup = BeautifulSoup(open('index.html'))
```

##### prettify(): 格式化并输出soup对象的内容：
```Python
print soup.prettify()
"""
<head>
  <title>
   The Dormouse's story
  </title>
"""
```

##### BeautifulSoup的四个Objects
**Tag**          
HTML中的一个个标签，如下面的**title加上内容就算一个Tag**
```Python
<title>The Dormouse's story</title>
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
```

用BeautifulSoup获取Tags：     
```Python
#soup = BeautifulSoup(html)
print soup.title
#<title>The Dormouse's story</title>

# 只能显示遇到的第一个符合要求的Tag
print soup.a
#<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
```

查看Objects的类型是否是Tag：     
```Python
print type(soup.a)
#<class 'bs4.element.Tag'>
```

Tag的属性：
* **.name**
```Python
# soup = BeautifulSoup(html)
print soup.name            # [document]
print soup.a.name          # a
print soup.head.name       # head
```

* **.attrs**/**tag.has_attr**
生成一个dict, attrs属性可以修改和删除。
```Python
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
print soup.p.attrs         #{'class': ['title'], 'name': 'dromouse'}
print soup.p['class']      #['title']
print soup.p.get('class')  #['title']
del soup.p['class']

print tag.has_attr('class') and not tag.has_attr('id')
```

**NavigableString**          
.string: 输出Tag里面包含的String, 与.contents的区别在于**输出结果不带Tag**, 另外，如果tag包含多个子节点（可以输出的string), 则string 方法无法确应该调用哪个子节点的内容, .string 的输出结果是 None
```Python
# soup = BeautifulSoup(html)
print soup.head.string
print soup.title.string
The Dormouse's story
The Dormouse's story

print type(soup.head.string)
#<class 'bs4.element.NavigableString'>

print soup.html.string
#None
```

**BeautifulSoup**    
BeautifulSoup 对象表示的是一个文档的全部内容。大部分时候可以把它当作 Tag 对象并分别获取它的类型，名称，以及属性：
```Python
#soup = BeautifulSoup(html)
print soup.name  # [document]
print soup.attrs # {}
print type(soup) # <type 'unicode'>
```

**Comment**    
Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号，但是如果不好好处理它，可能会对我们的文本处理造成意想不到的麻烦。
```Python
#<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>
#soup = BeautifulSoup(html)
print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
print soup.a.string  #.string输出的注释把注释符号去掉了。
# Elsie 
print type(soup.a.string)
# <class 'bs4.element.Comment'>
```

##### 遍历文档树
(1) 直接子节点
* **.contents**            
将tag的**子节点**以**列表**的方式输出, 可以通过列表索引A[i]获取元素, **注意输出结果要相应的带上Tag**
```Python
# soup = BeautifulSoup(html)
print soup.head.contents
print soup.title.contents
# [<title>The Dormouse's story</title>]
# [u"The Dormouse's story"]

# 输出第一个符合条件的Tag的contents
print soup.p.contents  
# [<b>The Dormouse's story</b>]
```

* **.children**            
生成一个list generator. 可以用for循环输出所有的结果：
```Python
# soup = BeautifulSoup(html)
for child in soup.body.children:
    print child
"""
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>


<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>


<p class="story">...</p>
"""
```

(2) 所有子孙节点
* **.descendants**
```Python
html = """
<html><head><title>The Dormouse's story</title></head>
"""
soup = BeautifulSoup(html)
for child in soup.descendants:
    print child
"""
<html><head><title>The Dormouse's story</title></head>
</html>
<head><title>The Dormouse's story</title></head>
<title>The Dormouse's story</title>
The Dormouse's story

"""
```

(3) 多个内容      
* **.strings**    
```Python
soup = BeautifulSoup(html)
for string in soup.strings:
    print repr(string)  # repr(): 用转义字符代表空格
    # u"The Dormouse's story"
    # u'\n\n'
    # u"The Dormouse's story"
    # u'\n\n'
    # u'Once upon a time there were three little sisters; and their names were\n'
    # u'Elsie'
    # u',\n'
    # u'Lacie'
    # u' and\n'
    # u'Tillie'
    # u';\nand they lived at the bottom of a well.'
    # u'\n\n'
    # u'...'
    # u'\n'
```

* **.stripped_strings**    
使用 .stripped_strings 可以去除输出多余的空白内容
```Python
for string in soup.stripped_strings:
    print(repr(string))
    # u"The Dormouse's story"
    # u"The Dormouse's story"
    # u'Once upon a time there were three little sisters; and their names were'
    # u'Elsie'
    # u','
    # u'Lacie'
    # u'and'
    # u'Tillie'
    # u';\nand they lived at the bottom of a well.'
    # u'...'
```

(4) 父节点
* **.parent**
包含该Tag的Tag
```Python
# soup = BeautifulSoup(html)
print soup.head.parent.name
print soup.p.parent.name
print soup.title.string.parent.name
# html
# body
# title
```

* **.parents**       
生成一个list generator
```Python
for parent in soup.title.string.parents:
    print parent.name
    # title
    # head
    # html
    # [document]
```

(5) 兄弟节点
* **.next_sibling**/**.previous_sibling**/**.next_siblings**/**.previous_siblings**          
兄弟节点可以理解为和本节点处在统一级的节点，.next_sibling属性获取了该节点的下一个兄弟节点，.previous_sibling则与之相反，如果节点不存在，则返回 None。 **注意**：空白或者换行也可以被视作一个节点。    
```Python
# soup = BeautifulSoup(html)
print soup.p.next_sibling # None
print soup.p.next_sibling.next_sibling


for sibling in soup.a.next_siblings:
    print repr(sibling
    # u',\n'
    # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # u' and\n'
    # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # u'; and they lived at the bottom of a well.'
    # None
```

(6) 前后节点
* **.next_element**/**.previous_element**/**.next_elements**/**.previous_elements**        
与 .next_sibling, .previous_sibling 不同，它并不是针对于兄弟节点，而是在所有节点，不分层次.
```Python
# <head><title>The Dormouse's story</title></head>
print soup.head.next_element
#<title>The Dormouse's story</title>

# <html><head><title>The Dormouse's story</title></head>
# soup = BeautifulSoup(html)
for element in soup.html.next_elements:
    print element
#<head><title>The Dormouse's story</title></head>
#<title>The Dormouse's story</title>
#The Dormouse's story
```

##### 搜索文档树
(1) find_all( name, attrs, recursive, text, **kwargs)          
* name        
传字符串        
```Python
print soup.find_all('b')
# [<b>The Dormouse's story</b>]
```

传正则表达式: Beautiful Soup会通过正则表达式的match()来匹配内容.即找出所有以b开头的标签,这表示<body>和<b>标签都应该被找到.                    
```Python
import re
for tag in soup.find_all(re.compile("^b")):
    print tag.name 
# body
# b
```

传列表: Beautiful Soup会将与列表中任一元素匹配的内容返回.            
```Python
soup.find_all(["a", "b"])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```

传True: True 可以匹配任何值,下面代码查找到所有的tag.     
```Python
for tag in soup.find_all(True):
    print tag.name
# html
# head
# title
# body
# p
# b
# p
# a
# a
```

* keyword    
```Python
soup.find_all(id='link2')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

soup.find_all(href=re.compile("elsie"))
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.find_all(href=re.compile("elsie"), id='link1')
# [<a class="sister" href="http://example.com/elsie" id="link1">three</a>]

soup.find_all("a", class_="sister") # 因为class 是 python 的关键词, 所以加下划线
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```

当有些tag属性在搜索不能使用,比如HTML5中的 data-* 属性, 则可以通过 find_all() 方法的 attrs 参数定义一个字典参数来搜索包含特殊属性的tag.    
```Python
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
data_soup.find_all(attrs={"data-foo": "value"})
# [<div data-foo="value">foo!</div>]
```

* limit           
可以使用 limit 参数限制返回结果的数量
```Python
soup.find_all("a", limit=2)
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
```

* recursive    
调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False.     
```Python
# 示例代码
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
...

soup.html.find_all("title")
# [<title>The Dormouse's story</title>]

soup.html.find_all("title", recursive=False)
# []
```

(2) find( name, attrs, recursive, text, **kwargs)           
它与 find_all()唯一的区别是find_all()的返回结果是包含元素的列表,而 find()直接返回结果     

(3) find_parents()/find_parent()        
用来搜索当前节点的父辈节点,搜索方法与普通tag的搜索方法相同,搜索文档搜索文档包含的内容                

(4) find_next_siblings()/find_next_sibling()    
find_next_siblings() 方法返回所有符合条件的后面的兄弟节点,find_next_sibling() 只返回符合条件的后面的第一个tag节点                         

(5) find_previous_siblings()/find_previous_sibling()             
find_previous_siblings() 方法返回所有符合条件的前面的兄弟节点,find_previous_sibling()方法返回第一个符合条件的前面的兄弟节点              

(6) find_all_next()/find_next()     
find_all_next() 方法返回所有符合条件的节点, find_next()方法返回第一个符合条件的节点          

(7) find_all_previous()/find_previous()            
find_all_previous() 方法返回所有符合条件的节点, find_previous()方法返回第一个符合条件的节点 

##### CSS选择器      
在写 CSS 时，**标签名不加任何修饰，类名前加点，id名前加#**，在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是list          
```Python
# 通过标签名查找
print soup.select('a')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# 通过类名查找
print soup.select('.sister')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# 通过id名查找
print soup.select('#link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]

# 组合查找
print soup.select('p #link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]

# 直接子标签查找
print soup.select("head > title")
#[<title>The Dormouse's story</title>]

# 属性查找
print soup.select('a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]

print soup.select('p a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```
