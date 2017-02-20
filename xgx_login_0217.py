#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
import hashlib

def m5(s):
    m = hashlib.md5()
    m.update(s)
    mm = m.hexdigest()
    return mm

url = "http://passport.xueguoxue.com"
def login():
    global url
    header = {}
    data = {}
    s = requests.Session()
    r = s.get(url)
    l1 = re.compile(r'xueguoxue_session=(.*?);')
    l2 = l1.findall(r.headers['set-cookie'])
    l2 = str(l2)[2:-2]
    l3 = re.compile(r'csrfToken":"(.*?)"')
    l4 = l3.findall(r.content)
    l4 = str(l4)[2:-2]
    header['cookie'] = "xueguoxue_session=" + l2
    data['_token'] = l4
    data['phone'] = "13141032576"
    data['password'] = m5('123456')
    r1 = s.post(url+"/login",headers=header,data=data)
    l5 = re.compile(r'course_xueguoxue_session=(.*?);')
    l6 = l5.findall(r1.headers['set-cookie'])
    l6 = str(l6)[2:-2]
    return l6
