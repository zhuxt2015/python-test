# -*- coding: utf-8 -*-

import urllib2
import re


class Youku_Spider(object):

     # 申明相关属性
    def __init__(self, url):
        self.url = url
        self.datas = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Referer': 'http://www.772s.com/'
        }

    def youku_spider(self):
        # 获取主页面
        req = urllib2.Request(self.url, headers=self.headers)

        html = urllib2.urlopen(req).read()
        urls = re.findall(
            '<a href="(.*?)".*?style="font-weight: bold;color: #3C9D40;".*?class="s xst">.*?</a>', html)
        for u in urls:
            self.get_accounts(u)

    def get_accounts(self, url):
        # url = 'http://www.772s.com/thread-12381-1-1.html'

        req = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(req)
        data = response.read()
        result = data

        accounts = re.findall(
            '<font.*?color="#555555">(.*?)</font>', result, re.S)
        items = []
        for item in accounts:
            items.append(item)

        with open('youkuvip.txt', 'a') as f:
            for account in items:
                f.write(account + '\n')

#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：优酷vip帐号爬虫
#   版本：0.1
#   作者：zhuxt
#   日期：2016-10-17
#   语言：Python 2.7
#   功能：将网上共享的优酷vip帐号存储到本地txt文件。
#---------------------------------------
"""
youkuvip = Youku_Spider('http://yk.772s.com/')
youkuvip.youku_spider()
