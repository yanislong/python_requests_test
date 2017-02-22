#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
import hashlib
import xgx_config
import bs4

def m5(s):
    m = hashlib.md5()
    m.update(s)
    mm = m.hexdigest()
    return mm

url = xgx_config.url_test
def login():
    global url
    header = {}
    data = {}
    s = requests.Session()
    r = s.get(url + "/login?redirect_url=" + url,allow_redirects=False)
    url2 = r.headers['location']
    r1 = s.get(url2)
    l1 = re.compile(r'xueguoxue_session=(.*?);')
    l2 = l1.findall(r1.headers['set-cookie'])
    l2 = str(l2)[2:-2]
    html1 = bs4.BeautifulSoup(r1.content)
    t_token = html1.find(attrs={"name":"csrf-token"})['content']
#    html = bs4.BeautifulSoup(r.content)
#    print html.input['value']
#    l4 = html.find(id='x-csrf-token')['value']
    header['cookie'] = "xueguoxue_session=" + l2
    data['_token'] = t_token
    data['phone'] = xgx_config.phone
    data['password'] = m5(xgx_config.password)
    r2 = s.post(xgx_config.url_pp_test + "/login", headers=header, data=data)
    l5 = re.compile(r'course_xueguoxue_session=(.*?);')
    l6 = l5.findall(r2.headers['set-cookie'])
    l6 = str(l6)[2:-2]
    return l6

if __name__ == '__main__':
    login()
