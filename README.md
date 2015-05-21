
## 介绍
zhihu_crawler是一个用于抓取[知乎](http://www.zhihu.com/)上的[问题](http://www.zhihu.com/question/29693016)、[用户](http://www.zhihu.com/people/xie-ke-41)以及[专栏](http://zhuanlan.zhihu.com/niceliving)里相关信息的项目。  

zhihu_crawler基于**Python 2.7.6编写，并在Xubuntu 14.04上编译通过**。在其他系统上使用可能存在一定的问题。  


## 环境配置
在使用前，首先建议安装Python的虚拟环境virtualenv：  
Ubuntu用户可以如此安装：  
```Python
$ sudo apt-get install python-virtualenv  
```
如何你使用的是Mac OS X，你可以这样安装：  
```Python
$ sudo easy_install virtualenv  
```
windows请百度^_^  



接着在zhihu_crawler文件夹里创建并激活虚拟环境：  
```Python
~/zhihu_crawler$ virtualenv venv  
~/zhihu_crawler$ source venv/bin/activate
```


在激活的虚拟环境里使用pip安装zhihu.py需要使用的第三方库：  
```Python
(venv)$ pip install -r requirements.txt  
```

## 使用说明
**注**：  
1. 请在激活的虚拟环境下进行项目的使用  
2. 在正式使用之前请先调用**zhihu.create_cookies**以便模拟登陆知乎！  
3. 在看到"cookies file created!"以后会生成"cookies.json"文件，请保证其与"zhihu.py"在同一个文件夹中  

```Python
$ python
>>> import zhihu
Please run "zhihu.create_cookies()" for further operation.
>>> zhihu.create_cookies()
email: <你的知乎登陆邮箱>
password: <你的知乎登陆密码> 
Please check "captcha.gif" for captcha
captcha: <请将在zhihu_crawler文件夹中生成的captcha.gif的验证码手动输入在此>
cookies file created!
```

zhihu.py里包含的class, method和method的作用如下， 仅支持以Markdown格式保存内容。**具体的使用方法和效果请参考usg_exp.py**  

```Python
class Question
 |-get_tags               (问题标签)
 |-get_question           (问题标题)
 |-ques_description       (问题描述)
 |-answer_followers       (问题关注者人数)
 |-answer_num             (问题回答数量)
 |-top_answer             (排在最前面的回答)
 |-top_i_answers	      (排在前几名的回答）
 |-all_answers		      (全部答案)

 
class Author
 |-get_people_name	      (获取用户姓名)
 |-get_people_location	  (获取用户所在地点)
 |-get_people_career	  (获取用户的职业介绍)
 |-get_people_educate	  (获取用户的教育情况)
 |-get_self_description   (获取用户的自我介绍)
 |-get_agree_num	      (获取得到的赞同数)
 |-get_thanks_num	      (获取得到的感谢数)
 |-get_topics		      (获取people擅长的话题)
 |-answers_num		      (获取回答问题的数量)
 |-all_answers		      (获得该作者的所有答案)
 |-top_vote_answers	      (获取得到排名最高的前几个答案)
 |-newly_creates_answers  (获取最新回答的前几个答案)


class Column
 |-title		          (专栏名称)
 |-owner		          (获取专栏创建者)
 |-followers		      (获取专栏关注人数)
 |-description		      (获取专栏描述)
 |-num			           (获取专栏文章数)
 |-posts		          (获取专栏所有文章)

class ColumnArticles
 |-column		          (文章所在专栏)
 |-author		          (文章作者)
 |-title		          (文章的标题)
 |-agree_num		      (文章的评论数)
 |-comment_num		      (文章的评论数)
 |-save			          (保存文章内容)
```
