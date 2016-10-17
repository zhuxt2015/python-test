# -*_ encoding: utf-8 -*-
__author__ = 'zhuxt'
import string
import urllib2
import re

#----------- 处理页面上的各种标签 -----------


class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")

    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<", "<"), (">", ">"), ("&", "&"), ("&", "\""), (" ", " ")]

    def Replace_Char(self, x):
        x = self.BgnCharToNoneRex.sub("", x)
        x = self.BgnPartRex.sub("\n    ", x)
        x = self.CharToNewLineRex.sub("\n", x)
        x = self.CharToNextTabRex.sub("\t", x)
        x = self.EndCharToNoneRex.sub("", x)

        for t in self.replaceTab:
            x = x.replace(t[0], t[1])
        return x


class Baidu_Spider(object):
    # 申明相关属性
    def __init__(self, url):
        self.myUrl = url + '?see_lz=1'
        self.datas = []
        self.myTool = HTML_Tool()
        print u'已启动百度贴吧爬虫，啦啦啦啦'

    def baidu_tieba(self):
        # 读取页面信息，并从utf-8转码
        myPage = urllib2.urlopen(self.myUrl).read().decode('utf-8')
        # 计算楼主发布内容总共有多少页
        endPage = self.page_counter(myPage)
        # 获取贴吧的标题
        title = self.get_title(myPage)
        print u'文章名称： ' + title
        # 保存楼主发布的内容
        self.save_data(self.myUrl, title, endPage)

    # 计算一共有多少页
    def page_counter(self, myPage):
        myMatch = re.search(r'<span class="red">(\d+?)</span>', myPage, re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            print u'爬虫报告：发现楼主共有%d页的原创内容' % endPage
        else:
            endPage = 0
            print u'爬虫报告：无法计算楼主发布内容有多少页！'
        return endPage

    def get_title(self, myPage):
        myMatch = re.search(r'<h3.*?>(.*?)</h3>', myPage, re.S)
        if myMatch:
            title = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        # 文件名中不能包含\ / : * ? " < > |
        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace(
            '?', '').replace('"', '').replace('>', '').replace('<', '').replace('|', '')
        return title

    # 保存
    def save_data(self, url, title, endPage):
        # 加载页面数据到数组中
        self.get_data(url, endPage)
        f = open(title + '.txt', 'w+')
        f.writelines(self.datas)
        f.close
        print u'文章内容已经保存到本地txt文件中'
        print u'请按任意键推出'
        raw_input()

    # 获取数据
    def get_data(self, url, endPage):
        url = url + '&pn='
        for i in range(1, endPage + 1):
            print u'爬虫报告：爬虫%s号正在爬去数据中...' % i
            myPage = urllib2.urlopen(url + str(i)).read()
            # 处理myPage中html代码并转储到datas中
            self.deal_data(myPage.decode('utf-8'))

    def deal_data(self, mypage):
        myItems = re.findall('id="post_content.*?>(.*?)</div>', mypage, re.S)
        for item in myItems:
            data = self.myTool.Replace_Char(
                item.replace('\n', '').replace('<br>', '').encode('utf-8'))
            self.datas.append(data + '\n')


#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：百度贴吧爬虫
#   版本：0.1
#   作者：zhuxt
#   日期：2016-10-13
#   语言：Python 2.7
#   操作：输入网址后自动只看楼主并保存到本地文件
#   功能：将楼主发布的内容打包txt存储到本地。
#---------------------------------------
"""

# 以某小说贴吧为例子
# http://tieba.baidu.com/p/3932392401?see_lz=1&pn=1

print u'请输入贴吧地址最后的数字串'
bdurl = 'http://tieba.baidu.com/p/' + \
    str(raw_input(u'http://tieba.baidu.com/p/'))

# 调用
mySpider = Baidu_Spider(bdurl)
mySpider.baidu_tieba()
