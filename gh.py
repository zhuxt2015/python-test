#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import cookielib
import json
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time


class BJGH(object):

    def __init__(self):
        self.domain = 'http://www.bjguahao.gov.cn'
        self.Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
        self.Referer = self.domain
        self.headers = {
            'User-Agent': self.Agent,
            'Referer': self.Referer
        }
        self.mobile = '15011316991'
        self.password = 'zxt114123'
        # 获取cookie
        self.cookie = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handler)
        urllib2.install_opener(self.opener)
        # 暂停的时间间隔 秒
        self.interval = 60
        self.count = 1

    def start(self):
        while (1 == 1):
            self.gh()
            print '扫描 第%s次 时间: %s' % (self.count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            # print '协和 扫描 第%s次,%s'  ％  (self.count, time.strftime('%Y-%m-%d
            # %H:%M:%S', time.localtime))
            time.sleep(3)
            self.count = self.count + 1

    # 如果有号，发邮件
    def gh(self):
        # 首先获取cookie
        # url = 'http://www.bjguahao.gov.cn/index.htm'
        # self.getResponse(url)
        # 登陆
        postData = urllib.urlencode({
            'mobileNo': self.mobile,
            'password': self.password,
            'yzm': "",
            'isAjax': "true"
        })
        appointUrl = 'http://www.bjguahao.gov.cn/dpt/appoint/1-200004043.htm'
        # appointUrl = 'http://www.bjguahao.gov.cn/dpt/appoint/163-200002327.htm'
        html = self.getResponse(appointUrl)
        tds = re.findall(
            '<td.*?class="ksorder_kyy">.*?预约.*?value="(.*?)".*?</td>', html, re.S)
        if len(tds) > 0:
            self.sendEmail()
            time.sleep(self.interval)

    def getResponse(self, url, postData=None):
        req = urllib2.Request(url=url, headers=self.headers, data=postData)
        response = urllib2.urlopen(req)
        return response.read()

    def sendEmail(self):
        # 第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性
        msg = MIMEText('有号了，快去挂号！！！！！', 'plain', 'utf-8')
        msg['From'] = 'zxt362158@163.com <zxt362158@163.com>'
        msg['Subject'] = Header('北京挂号', 'utf-8').encode()
        msg['To'] = '594754793@qq.com <594754793@qq.com>'
        # 输入Email地址和口令:
        from_addr = 'zxt362158@163.com'
        password = 'zxtwy123'
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.163.com'
        # 输入收件人地址:
        to_addr = '594754793@qq.com'
        # 发送邮件
        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

        # 程序入口
bjgh = BJGH()
bjgh.start()
