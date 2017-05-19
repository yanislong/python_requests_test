#!/usr/bin/python
# -*- coding=utf-8 -*-

import requests
import hashlib

def pw_md5(reg_pw):
    passwd = hashlib.md5()
    passwd.update(reg_pw)
    return passwd.hexdigest()

def check_phone(data_phone=13100000000):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/check-unique"
    header = {}
    param = {}
    param['type'] = "nick_name"
    param['value'] = ''
#    param['type'] = 'phone'
#    param['value'] = data_phone
    r = requests.get(url,params=param)
    print r.url
    print r.content

def register():
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/register"
    header = {}
    data = {}
    data['phone'] =  '13166666009'
    data['nick_name'] = "!123"#unichr(0x9fcb)+'123'#unichr(2935)+unichr(9876)+unichr(1300)
    data['msg_code'] = '12312312111111' * 9
    data['password'] = pw_md5('123456')
    r = requests.post(url, headers=header, data=data)
    print r.content

def send_code():
    phone = '13112341234'
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/send-msg-code/" + phone
    r = requests.post(url,params={'type':'phone','value':'13112312312'})
    print r.content

def user_login():
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/login"
    data = {}
    data['phone'] = "\n13112341234\n"
    data['password'] = '\n\t' +pw_md5('123456') + '\n'
    r = requests.post(url, data=data)
    print r.content

if __name__ == "__main__":
    data_p = ['','1','12345678901','" or 1=1--','13141032576','13112332100',r'"13166666100"',u'13166666000\n\t ']
#    check_phone(data_p[7])
#    for i in data_p:
#        check_phone(i)
    register()
#    check_phone()
#    send_code()
#    user_login()
