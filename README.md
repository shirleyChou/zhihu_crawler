
### 介绍
zhihu_crawler基于Python 2.7.6编写的，并在Xubuntu上编译通过
[问题](http://www.zhihu.com/question/29693016)  
Python 2.7.6
### 环境配置及使用说明
首先，建议安装**Python的虚拟环境**到你的系统上：		
Ubuntu用户可以如此安装：		
```Python
$ sudo apt-get install python-virtualenv		
```
如何你使用的是Mac OS X，你可以这样安装：		
```Python
$ sudo easy_install virtualenv		
```

然后，在zhihu_crawler文件夹里创建虚拟环境并激活虚拟环境：		
**注：指令不适用于windows平台**		
> ~/zhihu_crawler$ virtualenv venv
> ~/zhihu_crawler$ source venv/bin/activate

在激活的虚拟环境里使用pip安装Python的第三方库：		
> (venv)$ pip install -r requirements.txt		

**注：以下的所有工程都需要在激活的虚拟环境下进行**

class Question
 |-get_tags		(问题标签)
 |-get_question		(问题标题)
 |-ques_description	(问题描述)
 |-answer_num		(问题回答数量)
 |-top_answer		(排在最前面的回答)   待保存 题目？
 |-top_i_answers	(排在前几名的回答）  待保存 题目？
 |-all_answers		(全部答案)          待保存 题目？
 |-specific_answer	(指定某个作者的答案)  待保存 题目？
 
class Author
 |-get_people_name	(获取用户姓名)
 |-get_people_location	(获取用户所在地点)
 |-get_people_career	(获取用户的职业介绍)
 |-get_people_educate	(获取用户的教育情况)
 |-get_self_description (获取用户的自我介绍)
 |-get_agree_num	(获取得到的赞同数)
 |-get_thanks_num	(获取得到的感谢数)
 |-get_topics		(获取people擅长的话题)
 |-answers_num		(获取回答问题的数量)
 |-top_vote_answers	(获取得到排名最高的前几个答案) 待保存在哪？
 |-specific_answer      (指定该作者回答的一个问题) 待保存在哪？
 |-newest_answer	(获取最新回答的答案) 待保存在哪？ 
 |-column		(获取作者的专栏) object 
 
class Collection
 |-name			(收藏夹名称)
 |-num			(收藏夹文章数)
 |-title		(获取收藏夹文章的题目)
 |-specific_collection	(备份收藏夹指定题目的文章) ？？
 |-all_columns		(备份该收藏夹所有文章) ？？
 
class Column
 |-title		(专栏名称)
 |-owner		(获取专栏创建者)
 |-followers		(获取专栏关注人数)
 |-description		(获取专栏描述)
 |-num			(获取专栏文章数)
 |-posts		(获取专栏所有文章)

class ColumnArticles
 |-column		(文章所在专栏)
 |-author		(文章作者)
 |-title		(文章的标题)
 |-agree_num		(文章的赞同数)
 |-comment_num		(文章的评论数)
