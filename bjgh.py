#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import cookielib

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
}

url = 'http://www.bjguahao.gov.cn/index.htm'

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

req = urllib2.Request(url = url, headers=headers)
response = urllib2.urlopen(req)
for item in cookie:
	print item.name
	print item.value

loginUrl = 'http://www.bjguahao.gov.cn/quicklogin.htm'
postData = urllib.urlencode({
	'mobileNo':"15011316991",
    'password':"zxt114123",
    'yzm':"",
    'isAjax':"true"
	})
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Referer': 'http://www.bjguahao.gov.cn/index.htm'
}
request = urllib2.Request(url= loginUrl, headers = headers, data = postData)
resp = urllib2.urlopen(request)
for item in cookie:
	print item.name
	print item.value


isLoginUrl = 'http://www.bjguahao.gov.cn/islogin.htm'
postData = urllib.urlencode({
	'isAjax':"true"
	})
req = urllib2.Request(url = isLoginUrl, headers = headers, data = postData)
req = urllib2.urlopen(req)
print req.read()

# print response.read()


