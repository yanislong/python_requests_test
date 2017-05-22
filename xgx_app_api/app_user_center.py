#!/usr/bin/python
# -*-coding=utf-8 -*-

import requests
import app_user_register
import re
import hashlib


def pw_md5(pw):
    mima = hashlib.md5()
    mima.update(pw)
    return mima.hexdigest()


def user_information(myphone):
    url = "https://cuimingwen.api.xueguoxuewang.cn/v1/user/center"
    header = {}
    data = {}
    data['token'] = app_user_register.user_login(myphone)
    r = requests.get(url, params=data, verify=False)
    print r.url
    print r.content

def send_code(myphone):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/passwd/msg/send"
    data = {'phone':myphone}
    r = requests.post(url, data=data)
    l1 = re.compile('\d{6}')
    l2 = l1.findall(r.content)
    try:
        if l2:
            print "短信发送成功，验证码： " + l2[0]
            return l2[0]
        else:  
            print r.content
    except:
        print 'ifcate error'
        return None

def reset_passwd(myphone):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/passwd/reset"
    data = {}
    data['phone'] = myphone
    data['code'] = "464878"#send_code(myphone)
    data['password'] = pw_md5('123456789')
    r = requests.post(url, data=data)
    print r.content

def user_identity():
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/identity-list"
    data = {'token':app_user_register.user_login('13166666249')}
    r = requests.get(url, params=data)
    print r.content

def user_identity_save(myphone):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/identity"
    data = {}
    data['identity'] = (40,60,30)
    data['interests[]'] = ((103,105),)
    param = {'token':app_user_register.user_login(myphone)}
    r = requests.post(url, data=data, params=param)
    print r.url
    print r.content
    
def user_collect(myphone):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/center/collection"
    header = {}
    param = {}
    param['type'] = "10"
    param['token'] = app_user_register.user_login(myphone)
    r = requests.get(url, params=param)
    print r.content
   
def user_order(myphone):
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/center/order"
    param = {}
    param['order_status'] = 10
    param['page'] = 1
    param['token'] = app_user_register.user_login(myphone)
    r = requests.get(url, params=param)
    print r.content

def order_information(myphone):
    url = ""
    param = {}
    param['token'] = app_user_register.user_login(myphone)
    param['order_code'] = ""
    r = requests.get(url, params=param)
    print r.content

if __name__ == "__main__":
    myphone = "13166666241"
    user_information(myphone)
#    send_code(myphone)
#    reset_passwd(myphone)
#    user_identity()
#    user_identity_save(myphone)
#    user_collect(myphone)
#    user_order(myphone)
#    order_information(myphone)
