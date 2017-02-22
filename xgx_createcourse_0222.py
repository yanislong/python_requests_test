#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import requests
import hashlib
import re
import sys
import bs4
import time
import json
import threading
import random
import xgx_config

class course():

    def __init__(self):
        self.xgx = xgx_config.session
        self.n = 2
        self.course = self.teacher_course()

#老师发课
    def teacher_course(self):
        s = requests.Session()
        header = {}
        data = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        header['X-Requested-With'] = "XMLHttpRequest"
        header['X-CSRF-TOKEN'] = tt
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/course"
        mm = random.randrange(10,11,10)
        if mm == 10:
            data['sales_method'] = "10"
            data['original_cost'] = str(random.randint(2,9999))
            data['selling_price'] = str(random.randint(2,9999))
            data['cost_price'] = "1"
            data['title'] = "[正常销售]路曼曼其修远兮，吾将上下而求索%?"
        elif mm == 40:
            data['sales_method'] = "40"
            data['original_cost'] = str(random.randint(2,9999))
            data['selling_price'] = str(random.randint(2,9999))
            data['cost_price'] = "1"
            data['total_period'] = str(random.randint(2,99))
            data['update_the_deadline'] = str(random.randrange(1,3,1))
            data['title'] = "[预售课]终于知道为什么一读书就困了，因为读书，是梦>开始的地方？%"
        elif mm == 50:
            data['sales_method'] = "50"
            data['original_cost'] = str(random.randint(2,9999))
            data['selling_price'] = "9999"# str(random.randint(2,9999))
            data['cost_price'] = "1"
            data['apply_start_at'] = "2017-03-10"# + str(random.randint(23,25))
            data['apply_end_at'] = "2017-03-31"# + str(random.randint(25,30))
            data['places_upper_limit'] = str(random.randint(9,99))
            data['places_lower_limit'] = str(random.randint(1,9))
            data['course_start_at'] = "2017-04-24"
            data['consulting_tel'] = "010-8888999"
            data['total_period'] = "3"
            data['video_times'] = "10"
            data['course_end_at'] = "2017-05-31"
            data['title'] = "[线下实体授课]革命总是悄悄地不期而至，每次一小步"
        data['course_synopsis'] = "[ course_synopsis ] 你以为躲起来就找不到你了>吗？没有用的！像你这么出色的男人，无论在什么地方，都像漆黑中的萤火虫一样，那样的"
        data['course_pic'] = self.course_pic()
        data['course_bg_pic'] = self.course_back_pic()
        a = []
        for i in range(2):
            a.append(self.course_doc())
        b = tuple(a)
        data['course_docs[]'] = b
#        data['speaker_teacher'] = "".join(random.sample("abcdefghijklmnopqrstuvwxyz",4))
        data['speaker_teacher'] = "".join(random.sample(u'爱过所以慈悲因为懂得宽k',3))
#        f = open('/root/test1','rb')
#        print f.read()
        data['course_presentation'] = "[this is course_presentation]<h3>小时候，"
        data['category_ids[]'] = "3"
        data['category_ids[1][]'] = "1"
        data['tag_ids[]'] = "15"
        data['shopping_guide'] = "this is shopping_guide,你爱怎么卖就怎么卖"
        data['check_status'] = "10"
        course = s.post(url, data=data, headers=header)
        print course.content
        l1 = re.compile(r'cid":"(.*?)"')
        l2 = l1.findall(course.text)
        return str(l2)[3:-2],mm

#上传课程图
    def course_pic(self):
        s = requests.Session()
        header = {}
        header['cookie'] = 'course_xueguoxuewang_session=' + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/cpics"
        data = {'__token':tt}
        while True:
            dir = str(random.randint(500,1030))
            if os.path.exists('/root/Desktop/picc/' + dir + '.jpeg'):
                file = {'file':open(r'/root/Desktop/picc/' + dir + '.jpeg','rb')}
                break
#        file = {'file':open(r'/root/Desktop/banner/banner10.png','rb')}
        course_pic = s.post(url,headers=header,files=file, data=data)
        if course_pic.status_code == 200:
            l1 = re.compile(r'key":"(.*?)"')
            l2 = l1.findall(course_pic.content)
            l2 = str(l2).replace(r'\\','')
            l2 = l2[2:-2]
            print "上传课程图片成功: %s" % l2
        else:
            print "上传课程图片失败"
            return None
        return l2

#上传背景图
    def course_back_pic(self):
        s = requests.Session()
        header = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
#        file = {'file':open('/root/Desktop/tu/' + str(random.randint(1,9)) + '.jpeg','rb')}
        file = {'file':open('/root/Desktop/banner/banner11.png','rb')}
        data = {'__token':tt}
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/cbgpics"
        back_pic = s.post(url, files=file, headers=header,data=data)
        if back_pic.status_code == 200:
            l1 = re.compile(r'key":"(.*?)"')
            l2 = l1.findall(back_pic.content)
            l2 = str(l2).replace(r'\\','')
            l2 = l2[2:-2]
            print "上传课程背景图片成功: %s" % l2
        else:
            print "上传课程背景图片失败"
            return None
        return l2

#上传课程附件
    def course_doc(self):
        s = requests.Session()
        header = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        file = {'file':open('/root/Desktop/bbb.pdf','rb')}
        data = {'__token':tt}
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/docs"
        doc = s.post(url, files=file, headers=header, data=data)
        if doc.status_code == 200:
            l1 = re.compile(r'key":"(.*?)"')
            l2 = l1.findall(doc.content)
            l2 = str(l2).replace(r'\\','')
            l2 = l2[2:-2]
            print "上传课程附件成功: %s" % l2
        else:
            print "上传课程附件失败"
            return None
        return l2

#上传课时
    def course_keshi(self):
        s = requests.Session()
        header = {}
        data = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        header['X-CSRF-TOKEN'] = tt
        header['X-Requested-With'] = "XMLHttpRequest"
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/period"
        data = {}
        data['video_src'] = self.upload_view()
        data['videoTitle'] = "[videl title]v字仇杀队 --" + str(self.n)
        data['period_bio'] = "this is bio --->> 我们被教导要记住思想，而不是人"
        if self.course[1] == 10:
            if self.n % 2 == 0:
                data['sales_method'] = "20"
                data['try_play'] = "10"
                data['videoType'] = "free"
                data['period_title'] = "[免费]日日行，不怕千万里；常常做，不怕千"
            else:
                data['period_title'] = "[收费]人非圣贤，孰能无过" + str(self.n)
                data['sales_method'] = "20"
                data['videoType'] = "charge"
        elif self.course[1] == 40:
            if self.n % 2 == 0:
                data['sales_method'] = "40"
                data['try_play'] = "10"
                data['videoType'] = "free"
                data['period_title'] = "[免费]世界上的脑残这么多，可是你却成了其"
                print self.n
            else:
                data['period_title'] = "[收费]世界上的脑残这么多，可是你却成了其"
                print self.n
                data['sales_method'] = "40"
                data['videoType'] = "charge"

        elif self.course[1] == 50:
            if self.n % 2 == 0:
                data['sales_method'] = "50"
                data['try_play'] = "10"
                data['videoType'] = "free"
                data['period_title'] = "[免费] period_title,v字仇杀队" + str(self.n)
            else:
                data['period_title'] = "[收费] period_title,v字仇杀队" + str(self.n)
                data['sales_method'] = "50"
                data['videoType'] = "charge"
        #data['price'] = "10"
        #data['cost_price'] = "1"
        data['cid'] = self.course[0]
        r = s.post(url, headers=header, data=data)
        print r.content
        data['period_title'] = "[收费]人非圣贤，孰能无过" + str(self.n)
        data['sales_method'] = "20"
        data['videoType'] = "charge"
        data['try_play'] = ""
        r = s.post(url ,headers=header, data=data)
        print r.content

#上传课时视频
    def upload_view(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/videos?cid=" + self.course[0]
        header = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        file = {'file':open('/root/Desktop/2017.mp4','rb')}
        data = {}
        data['cid'] = self.course[0]
        data['__token'] = tt
        r = s.post(url, files=file, headers=header ,data=data)
        print r.content
        l1 = re.compile(r'src":"(.*?)"')
        l2 = l1.findall(r.content)
        if l2:
            print "上传课时视频成功: %s" % str(l2)[2:-2]
            return str(l2)[2:-2]
        else:
            print "上传课时失败"
            sys.exit()

#提交审核
    def submit_course(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/submitAudit"
        header = {}
        header['cookie'] = "course_xueguoxuewang_session=" + self.xgx
        r0 = s.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        header['X-CSRF-TOKEN'] = tt
        header['X-Requested-With'] = "XMLHttpRequest"
        data = {'cid':self.course[0]}
        r = s.post(url, headers=header, data=data)
        print r.content


if __name__ == "__main__":
    a = course()
    a.course_keshi()
    a.submit_course()
