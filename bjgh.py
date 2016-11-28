#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import cookielib
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
}

url = 'http://www.bjguahao.gov.cn/index.htm'
# 获取cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

req = urllib2.Request(url=url, headers=headers)
response = urllib2.urlopen(req)
# for item in cookie:
#     print item.name
#     print item.value

loginUrl = 'http://www.bjguahao.gov.cn/quicklogin.htm'
postData = urllib.urlencode({
    'mobileNo': "15011316991",
    'password': "zxt114123",
    'yzm': "",
    'isAjax': "true"
})
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Referer': 'http://www.bjguahao.gov.cn/index.htm'
}
# 登陆
request = urllib2.Request(url=loginUrl, headers=headers, data=postData)
resp = urllib2.urlopen(request)
# for item in cookie:
#     print item.name
#     print item.value


isLoginUrl = 'http://www.bjguahao.gov.cn/islogin.htm'
postData = urllib.urlencode({
    'isAjax': "true"
})
req = urllib2.Request(url=isLoginUrl, headers=headers, data=postData)
req = urllib2.urlopen(req)
# print req.read()

url = 'http://www.bjguahao.gov.cn/dpt/appoint/163-200002321.htm'
# 进入预约页面
response = urllib2.urlopen(url)
# print response.read()
html = response.read()
# print html
tds = re.findall(
    '<td.*?class="ksorder_kyy">.*?预约.*?value="(.*?)".*?</td>', html, re.S)
# 有可预约的医生
if len(tds) > 0:
    params = tds[0].split('_')
    print '上午or 下午：', params[1]
    print '日期：', params[2]
    doctorUrl = 'http://www.bjguahao.gov.cn/dpt/partduty.htm'
    postData = urllib.urlencode({
        'hospitalId': "163",
        'departmentId': "200002321",
        'dutyCode': params[1],
        'dutyDate': params[2],
        'isAjax': "true"
    })
    # 获取doctorId，dutySourceId
    request = urllib2.Request(url=doctorUrl, data=postData)
    response = urllib2.urlopen(request)
    jsonResult = json.loads(response.read())
    # print jsonResult
    dutySourceId = jsonResult['data'][0]['dutySourceId']
    totalFee = jsonResult['data'][0]['totalFee']
    doctorTitleName = jsonResult['data'][0]['doctorTitleName']
    doctorId = jsonResult['data'][0]['doctorId']
    print 'dutySourceId:%s,totalFee:%s,doctorTitleName:%s,doctorId:%s' % (dutySourceId, totalFee, doctorTitleName, doctorId)
    # s = json.loads(
    #     '{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
    # print s
    # print dutySourceId
    # 预约操作
    yuyueUrl = 'http://www.bjguahao.gov.cn/order/confirm/163-200002321-%s-%s.htm' % (
        doctorId, dutySourceId)
    print yuyueUrl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Referer': 'http://www.bjguahao.gov.cn/order/confirm/163-200002321-200654115-39159370.htm'
    }
    browser = webdriver.Chrome()
    browser.get(yuyueUrl)
    # ck = json.dumps(cookie)
    ck = {'JSESSIONID', 'SESSION_COOKIE'}
    for item in cookie:
        if item.name == 'JSESSIONID':
            ck['JSESSIONID'] = item.value
        if item.name == ''
        # print "name: ", item.name
        # print "value: ", item.value

    # ck['JSESSIONID'] = cookie['JSESSIONID']
    print json.dumps(ck)

    sys.exit()
    browser.add_cookie(cookie)
    elem = browser.find_element_by_name('hqyzm')
    elem.send_keys(Keys.ARROW_DOWN)
    # request = urllib2.Request(
    #     url=yuyueUrl, headers=headers)
    # response = urllib2.urlopen(request)
    # # print response.read()
    # url = 'http://www.bjguahao.gov.cn/v/sendorder.htm'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    #     'Referer': 'http://www.bjguahao.gov.cn/order/confirm/163-200002321-200654115-39356094.htm',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    # }
    # # request = urllib2.Request(url=url, headers=headers)

    # response = urllib2.urlopen(url)
    # print response.read()
