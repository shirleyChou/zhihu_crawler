#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import time
import json
import functools

import requests
from bs4 import BeautifulSoup
import html2text

reload(sys)
sys.setdefaultencoding('utf8')

# global var
_cookies_name = 'cookies.json'
_session = None
_headers = {'Host': 'www.zhihu.com',
            'Referer': 'http://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0',
            'X-Requested-With': 'XMLHttpRequest'}

# Zhihu login URL
_zhihu_url = 'http://www.zhihu.com'
_zhihu_login_url = _zhihu_url + '/login'
_captcha_url_prefix = _zhihu_url + '/captcha.gif?r='

# zhihu column URL
_column_prefix = 'http://zhuanlan.zhihu.com/'
_column_GET_user = _column_prefix + 'api/columns/{0}'
_column_GET_posts = _column_GET_user + '/posts/{1}'
_column_GET_posts_limit = _column_GET_posts[:-4] + '?limit=10&offset={1}'

# regex
_re_question_url = re.compile(r'http://www\.zhihu\.com/question/\d+/?$')
_re_author_url = re.compile(r'http://www\.zhihu\.com/people/[^/]+/?$')
_re_column_url = re.compile(r'http://zhuanlan\.zhihu\.com/([^/]+)/?$')
_re_column_article_url = re.compile(
    r'http://zhuanlan\.zhihu\.com/([^/]+)/(\d+)/?$')
_re_collection_url = re.compile(r'http://www\.zhihu\.com/collection/\d+/?$')


def _init():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(_headers)
        if os.path.isfile(_cookies_name):
            with open(_cookies_name, 'r') as f:
                cookies_dict = json.load(f)
                _session.cookies.update(cookies_dict)
        else:
            print 'Please run "zhihu.create_cookies()" for further operation.'
    else:
        raise Exception('Please don\'t call function _init() manually.')


def create_cookies():
    if not os.path.isfile(_cookies_name):
        email = raw_input('email:')
        password = raw_input('password:')

        captcha_url = get_captcha_url()
        save_captcha(captcha_url)
        print 'Please check "captcha.gif" for captcha'
        captcha = raw_input('captcha:')
        os.remove('captcha.gif')

        r, msg = login(email, password, captcha)
        if r == 0:
            print 'cookies file created!'
        elif r == 1:
            print 'Failed to login. Error message is:' + msg
            print 'Please check the error message and try again.'
    else:
        print '%s has been created! Please delete it first.' % _cookies_name


def get_captcha_url():
    return _captcha_url_prefix + str(int(time.time() * 1000))


def save_captcha(url):
    global _session
    r = _session.get(url)
    with open('captcha.gif', 'w') as f:
        f.write(r.content)


def login(email=None, password=None, captcha=None):
    global _session
    data = {'email': email, 'password': password,
            'captcha': captcha, 'rememberme': 'y'}
    r = _session.post(_zhihu_login_url, data)

    j = r.json()
    status = int(j['r'])
    msg = j['msg']
    if status == 0:
        with open(_cookies_name, 'wb') as f:
            data = json.dumps(_session.cookies.get_dict())
            f.write(data)
            cookies_dict = json.loads(data)
            _session.cookies.update(cookies_dict)
    return status, msg


def set_class_variable(attr):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self):
            value = getattr(self, attr) if hasattr(self, attr) else None
            if value is None:
                self.make_soup()
                value = func(self)
                setattr(self, attr, value)
                return value
            else:
                return value
        return wrapper
    return decorator


def valid_name(text):
    invalid_char = ['\\', '/', ':', '*', '?', '<', '>', '|', '"']
    valid = ''
    for char in text:
        if char not in invalid_char:
            valid += char
    return valid


def create_file(path, filename, mode, defaultpath, defaultname):
    if path is None or '.':
        path = os.path.join(os.getcwd(), valid_name(defaultpath))
    if os.path.isdir(path) is False:
        os.makedirs(path)
    if filename is None:
        filename = valid_name(defaultname)
    temp = filename
    i = 0
    while os.path.isfile(os.path.join(path, filename) + '.' + mode):
        i += 1
        temp = filename + str(i)
    return os.path.join(path, temp) + '.' + mode


class Question:
    def __init__(self, url):
        if not _re_question_url.match(str(url)):
            raise Exception('Hmmm.. Unvalid URL! Please change.')
        else:
            self.url = str(url)
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    # 获取问题标签
    @property
    def get_tags(self):
        items = self.soup.find_all('a', class_='zm-item-tag')
        tags = [unicode(item.string.strip()) for item in items]
        return tags

    # 获取问题标题
    @property
    def get_question(self):
        raw_question = self.soup.find(
            'h2',
            class_='zm-item-title zm-editable-content')
        return raw_question.string.strip()

    # 获取问题描述
    @property
    def ques_description(self):
        data = self.soup.find('div', class_='zm-editable-content')
        return html2text.html2text(str(data))

    # 获取问题关注者人数
    @property
    def ques_followers(self):
        num = self.soup.find('div', class_='zg-gray-normal').a.strong.string
        return '关注者人数为' + num

    # 获取问题回答数
    @property
    def answer_num(self):
        raw_html = self.soup.find('h3', id='zh-question-answer-num')
        num = raw_html.get('data-num')
        self.num = num
        return '回答人数为：' + num

    # 获取排在最前面的回答
    @property
    def top_answer(self):
        self.answer_num
        top = self.soup.find('div', class_=' zm-editable-content clearfix')
        answer = html2text.html2text(str(top))
        return answer

    # 获取排名前几位的回答
    def top_i_answers(self, num):
        self.answer_num
        if not isinstance(num, int) or abs(num) != num:
            print 'Ohh! Please enter positive integer:'
        elif num > int(self.num):
            print 'Sorry, The number of answers for' \
                'this question is %s. Please enter again.' % self.num
        elif num == 1:
            return self.top_answer
        elif num > 1:
            find = self.soup.find_all(class_=' zm-editable-content clearfix',
                                      limit=num)
            for index, answer in enumerate(find):
                print '第%d个答案:\n' % (index+1)
                print html2text.html2text(str(answer))

    # 获取所有回答
    @property
    def all_answers(self):
        self.answer_num
        find = self.soup.find_all(class_=' zm-editable-content clearfix',
                                  limit=self.num)
        for index, answer in enumerate(find):
            print '第%d个答案:\n' % (index+1)
            print html2text.html2text(str(answer))


class Author:
    def __init__(self, url):
        if not _re_author_url.match(str(url)):
            raise Exception('Hmmm.. Unvalid URL! Please change.')
        else:
            if not url.endswith('/'):
                url += '/'
            self.url = str(url)
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            #with open('author.html', 'wb') as f:
                #f.write(r.content)

    # 获取用户名字
    @property
    def get_people_name(self):
        name = self.soup.find('div', class_='zm-profile-header').span.string
        #self_intro = self.soup.find('span', class_='bio').get('title')
        #return name + ':' + self_intro
        return name

    # 获取用户所在地点
    @property
    def get_people_location(self):
        locate = self.soup.find('span', class_='location item').get('title')
        return locate

    # 获取用户的职业介绍
    @property
    def get_people_career(self):
        profession = self.soup.find('span', class_='business item') \
            .get('title')
        employment = self.soup.find('span', class_='employment item') \
            .get('title')
        position = self.soup.find('span', class_='position item').get('title')
        return '行业: ' + profession \
            + '\n' + '公司： ' + employment + '\n' + '职位: ' + position

    # 获取用户的教育情况
    @property
    def get_people_educate(self):
        educate = self.soup.find('span', class_='education item').get('title')
        find = self.soup.find('span', class_='education-extra item')
        educate_extra = find.get('title')
        return educate + '|' + educate_extra

    # 获取用户的自我介绍
    @property
    def get_self_description(self):
        content = self.soup.find('div', attrs={'data-name': 'description'})
        return content.span.span.span.string.strip().replace('\n', '')

    # 获取得到的赞同数
    @property
    def get_agree_num(self):
        agree = self.soup.find('span', class_='zm-profile-header-user-agree') \
            .strong.string
        return '赞同： ' + agree

    # 获取得到的感谢数
    @property
    def get_thanks_num(self):
        thanks = self.soup.find(
            'span', class_='zm-profile-header-user-thanks').strong.string
        return '感谢： ' + thanks

    # 获取people擅长的话题
    @property
    def get_topics(self):
        result = self.soup.find_all('h3', class_='zg-gray-darker')
        t = [unicode(item.string).encode('utf-8') for item in result]
        vote = []
        topic = []
        for item in result:
            vote.append(item.find_next('p', class_='meta').span.contents[1])
        combine = zip(t, vote)
        for index, value in enumerate(combine):
            topic.append('擅长话题 [' + value[0] + '] 的点赞数为' + value[1])
        return topic

        #value = p.get_topics
            #for val in value:
                #print val

    # 获取回答问题的数量
    @property
    def answers_num(self):
        start = self.url.find('m')
        num = self.soup.find('a', class_='item',
                             href=self.url[start+1:]+'answers').span.string
        return int(num)

    # 获得该作者的所有答案
    @property
    def all_answers(self):
        url = self.url + 'answers'
        payload = {'order_by': 'created'}
        page = 0
        num = self.answers_num
        while num > 0:
            num -= 20
            page += 1
            payload['page'] = str(page)
            r = _session.get(url, params=payload)
            soup = BeautifulSoup(r.content)
            raw_html = soup.find_all('a', class_='question_link')
            for item in raw_html:
                text = item.parent.parent.div.textarea.next_element
                title = item.string
                file_name = create_file('.', None, 'md',
                                        self.get_people_name,
                                        title+'-'+self.get_people_name+'的回答')
                with open(file_name, 'w+') as f:
                    f.write(html2text.html2text(str(text).strip()))

    # 获取得到排名最高的前几个答案
    def top_vote_answers(self, num):
        url = self.url + 'answers'
        if not isinstance(num, int) or abs(num) != num:
            print 'Ohh! Please enter positive integer:'
        if self.answers_num < num:
            print 'Sorry. the num of questions the author answered' \
                'is smaller than your expected'
        else:
            temp = num
            payload = {'order_by': 'vote_num'}
            for i in range((num-1)//20 + 1):
                if temp > 20:
                    item = 20
                    temp -= 20
                else:
                    item = temp
                payload['page'] = str(i+1)
                r = _session.get(url, params=payload)
                soup = BeautifulSoup(r.content)
                raw_html = soup.find_all('a', class_='question_link',
                                         limit=item)
                for item in raw_html:
                    text = item.parent.parent.div.textarea.next_element
                    title = item.string
                    file_name = create_file(
                        '.', None, 'md',
                        self.get_people_name+'排名前'+str(num)+'的回答',
                        title+'-'+self.get_people_name+'的回答')

                    with open(file_name, 'w+') as f:
                        f.write(html2text.html2text(str(text).strip()))

    # 获取最新回答的前几个答案
    def newly_creates_answers(self, num):
        url = self.url + 'answers'
        if not isinstance(num, int) or abs(num) != num:
            print 'Ohh! Please enter positive integer:'
        if self.answers_num < num:
            print 'Sorry. the num of questions the author answered' \
                'is smaller than your expected'
        else:
            temp = num
            payload = {'order_by': 'created'}
            for i in range((num-1)//20 + 1):
                if temp > 20:
                    item = 20
                    temp -= 20
                else:
                    item = temp
                payload['page'] = str(i+1)
                r = _session.get(url, params=payload)
                soup = BeautifulSoup(r.content)
                raw_html = soup.find_all('a', class_='question_link',
                                         limit=item)
                for item in raw_html:
                    text = item.parent.parent.div.textarea.next_element
                    title = item.string
                    file_name = create_file(
                        '.', None, 'md',
                        self.get_people_name+'最新创建的'+str(num)+'个回答',
                        title+'-'+self.get_people_name+'的回答'
                    )

                    with open(file_name, 'w+') as f:
                        f.write(html2text.html2text(str(text).strip()))


# 备份某专栏所有文章
# 记住是不要翻页的
class Column:
    def __init__(self, url, title=None,
                 article_num=None, column_owner=None,
                 followers=None, description=None):

        match = _re_column_url.match(str(url))
        if not match:
            raise Exception('Hmmm. Unvalid URL! Please change.')
        else:
            self._in_name = match.group(1)
            self._url = str(url)
        self._title = title
        self._column_owner = column_owner
        self._followers = followers
        self._description = description
        self._article_num = article_num
        self.soup = None

    def make_soup(self):
        global _session
        if self.soup is None:
            assert isinstance(_session, requests.Session)
            origin_host = _session.headers.get('Host')
            _session.headers.update(Host='zhuanlan.zhihu.com')
            response = _session.get(_column_GET_user.format(self._in_name))
            _session.headers.update(Host=origin_host)
            self.soup = response.json()

    # 专栏名称
    @property
    @set_class_variable('_title')
    def title(self):
        return self.soup['name']

    # 获取专栏创建者
    @property
    @set_class_variable('_column_owner')
    def owner(self):
        return self.soup['creator']['name']

    # 获取专栏关注人数
    @property
    @set_class_variable('_followers')
    def followers(self):
        return int(self.soup['followersCount'])

    # 获取专栏描述
    @property
    @set_class_variable('_description')
    def description(self):
        return self.soup['description']

    # 获取专栏文章数
    @property
    @set_class_variable('_article_num')
    def num(self):
        return int(self.soup['postsCount'])

    # 获取专栏所有文章
    @property
    def posts(self):
        global _session
        origin_host = _session.headers.get('Host')
        for offset in range(0, (self.num-1)//10 + 1):
            _session.headers.update(Host='zhuanlan.zhihu.com')
            response = _session.get(
                _column_GET_posts_limit.format(self._in_name, offset*10))
            soup = response.json()
            _session.headers.update(Host=origin_host)
            for article in soup:
                url = _column_prefix + article['url'][1:]
                author = Author(article['author']['profileUrl'])
                title = article['title']
                agree_num = article['likesCount']
                comment_num = article['commentsCount']
                yield ColumnArticles(url, self, author, title,
                                     agree_num, comment_num)


class ColumnArticles:
    def __init__(self, url, column=None, author=None,
                 title=None, argee_num=None, comment_num=None):
        match = _re_column_article_url.match(str(url))
        if not match:
            raise Exception('Hmmm. Unvalid URL! Please change.')
        else:
            self._url = str(url)
            self._column = column
            self._author = author
            self._title = title
            self._argee_num = argee_num
            self._comment_num = comment_num
            self.soup = None
            self._slug = match.group(1)
            self._article_code = match.group(2)

    def make_soup(self):
        if self.soup is None:
            global _session
            assert isinstance(_session, requests.Session)
            origin_host = _session.headers.get('Host')
            _session.headers.update(Host='zhuanlan.zhihu.com')
            self.soup = _session.get(
                _column_GET_posts.format(self._slug, self._article_code)) \
                .json()
            _session.headers.update(Host=origin_host)

    # 文章所在专栏
    @property
    @set_class_variable('_column')
    def column(self):
        column_name = self.soup['column']['name']
        column_url = _column_prefix + self.soup['column']['slug']
        return Column(column_url, title=column_name)

    # 文章作者
    @property
    @set_class_variable('_author')
    def author(self):
        return self.soup['author']['name']

    # 文章的标题
    @property
    @set_class_variable('_title')
    def title(self):
        return self.soup['title']

    # 文章的赞同数
    @property
    @set_class_variable('_argee_num')
    def agree_num(self):
        return self.soup['likesCount']

    # 文章的评论数
    @property
    @set_class_variable('_comment_num')
    def comment_num(self):
        return self.soup['commentsCount']

    # 保存文章内容
    def save(self, filepath=None, filename=None):
        self.make_soup()
        if isinstance(self.author, Author):
            author = self.author.get_people_name
        else:
            author = self.author
        file_name = create_file(filepath, filename, 'md',
                                self.soup['column']['name'],
                                self.title + '-' + author)
        with open(file_name, 'wb') as f:
            f.write(html2text.html2text(self.soup['content']))


_init()
