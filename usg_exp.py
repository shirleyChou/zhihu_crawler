# !/usr/bin/env python
# encoding: utf-8

from zhihu import Question, Author, Column, ColumnArticles

def exp_question():
    q = Question('http://www.zhihu.com/question/29693016')

    # 获取问题标签
    for tag in q.get_tags:
        print tag,
    # 校园招聘 实习生 社会招聘 面试技巧 互联网求职


    # 获得问题标题
    print q.get_question
    # 互联网求职路上，你见过哪些写得很好、很用心的面经？最好能分享自己的面经、心路历程。


    # 获取问题描述
    """以markdown形式输出"""
    print q.ques_description
    # 技术类、非技术类的都行；校招、社招的都行。诚然，此问题并不局限于分享面经，也可以授之以渔而非授之以鱼。...


    # 获取问题关注者人数
    print q.ques_followers
    # 关注者人数为1323


    # 获取问题回答数
    print q.answer_num
    # 回答人数为：17


    # 获取排在最前面的回答
    print q.top_answer
    # 第1个答案:
    # 自问自答。开这个问题的初衷是希望知乎上的CS大牛们能分享一下自己的求职心路历程，既然大家都这么羞涩，我只好抛砖引玉（一般来说，需要二次跳转查看的答案传播面都不会太广）。


    # 获取排名前几位的回答
    print q.top_i_answers(2)
    # ...
    # 第2个答案:
    # [@Michael282694](http://www.zhihu.com/people/7303e4f770e8055f3bedc4cf3b192325)说我不回答就要拉黑我，心理感觉到了深深的恐惧（她说她准备了5把刀）
    # ...


    # 获取所有回答
    print q.all_answers
    # ......
    # 第17个答案:
    # 最近在找工作，有一些体会，稍后整理一下。


def exp_author():
    a = Author('http://www.zhihu.com/people/xie-ke-41')

    # 获取用户名字
    print a.get_people_name
    # 谢科


    # 获取用户所在地点
    print a.get_people_location
    # 旧金山 (San Francisco)


    # 获取用户的职业介绍
    print a.get_people_career
    # 行业: 互联网
    # 公司： Twitter
    # 职位: 搜索引擎


    # 获取用户的教育情况
    print a.get_people_educate
    # 康奈尔大学|PhD in IS (中途跑路中)


    # 获取用户的自我介绍
    print a.get_self_description
    # I don't usually answer questions. But when I do, I do it good. 抱歉，不做免费咨询，暂时不准备跳槽


    # 获取得到的赞同数
    print a.get_agree_num
    # 赞同： 16282


    # 获取得到的赞同数
    print a.get_thanks_num
    # 赞同： 16282


    # 获取people擅长的话题
    value = a.get_topics
    for val in value:
        print val
    # 擅长话题 [健身] 的点赞数为48
    # 擅长话题 [吉他手] 的点赞数为0
    # 擅长话题 [数据挖掘] 的点赞数为7245
    # 擅长话题 [Python] 的点赞数为3106
    # 擅长话题 [算法] 的点赞数为0
    # 擅长话题 [机器学习] 的点赞数为980


    # 获取回答问题的数量
    print a.answers_num
    # 39


    # 获得该作者的所有答案
    print a.all_answers
    # 生成文件夹 [谢科]


    # 获取得到排名最高的前几个答案
    print a.top_vote_answers(21)
    # 生成文件夹 [谢科排名前21的回答]


    # 获取最新回答的前几个答案
    print a.newly_creates_answers(2)
    # 生成文件夹 [谢科最新创建的2个回答]



def exp_column():
    c = Column('http://zhuanlan.zhihu.com/niceliving')

    # 专栏名称
    print c.title
    # 好好住


    # 获取专栏创建者
    print c.owner
    # 冯驌


    # 获取专栏关注人数
    print c.followers
    # 66125


    # 获取专栏描述
    print c.description
    # 好好住家居研究院官方知乎专栏，踏踏实实做轻松打造好家的实用攻略。新浪微博@好好住家居研究院 @总有可取处-实用家居，微信号 myhomedeco


    # 获取专栏文章数
    print c.num
    # 50


    # 获取专栏所有文章, 调用ColumnArticles类
    print c.posts
    # <generator object posts at 0xb6d474dc>
    for post in c.posts:
        print isinstance(post, ColumnArticles)
        #True


        # 文章所在专栏
        print post.column
        # <zhihu.Column instance at 0xb74cb1cc>


        # 文章作者
        print post.author
        # <zhihu.Author instance at 0xb6da788c>
        print isinstance(post.author, Author)
        # True


        # 文章的标题
        print post.title
        # ...
        # 只用一件老家具，打造vintage复古家
        # ...


        # 文章的赞同数
        print post.agree_num
        #
        # 92
        # ...


        # 文章的评论数
        print post.comment_num
        # ...
        # 6
        # ...


        # 保存文章内容
        post.save(filepath='.')
        # 保存所有文章到文件夹 [好好住]


def exp_column_article():
    c = ColumnArticles('http://zhuanlan.zhihu.com/niceliving/20030578')

    # 文章所在专栏
    print c.column
    # <zhihu.Column instance at 0xb6cdcb6c>


    # 文章作者
    print c.author
    # 冯驌


    # 文章的标题
    print c.title
    # 这些收纳技巧是从分类强迫症患者身上学的


    # 文章的赞同数
    print c.agree_num
    # 467


    # 文章的评论数
    print c.comment_num
    # 30


    # 保存文章内容
    c.save(filepath='.')
    # 在文件夹 [好好住] 下生成文件 [这些收纳技巧是从分类强迫症患者身上学的-冯驌.md]


exp_question()
exp_author()
exp_column()
exp_column_article()
