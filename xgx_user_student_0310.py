#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import pymysql
from collections import Iterator
import bs4
import xgx_config

#print isinstance("",Iterator)

phone = "13166666213"
url_parent = "http://course.lihailong.xueguoxuewang.cn/u/identify/parent"
url_teacher = "http://course.lihailong.xueguoxuewang.cn/u/identify/teacher"
url_student = "http://course.lihailong.xueguoxuewang.cn/u/identify/student"
url_normal = "http://course.lihailong.xueguoxuewang.cn/u/identify/normal"

data_student = {}
data_student['true_name'] = "haizi"
data_student["school_id"] = "1"
data_student["grade_id"] = "6"
data_student["gender"] = "10"
data_student['email'] = "xuesheng@q.com"
data_student['birthday'] = "2017-01-01"

def user_identify(url, data_identify,xgx):
    global phone
    conn = pymysql.connect(host="172.16.9.238",user="root",passwd="xueguoxue",db="xgx_course",charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    effect_row = cursor.execute("UPDATE `xgx_users` SET role_id=0  WHERE phone=%s",phone)
    print effect_row
    conn.commit()
    data = data_identify
    header = {}
    s = requests.Session()
    header['cookie'] = "course_xueguoxuewang_session=" + xgx
    r0 = s.get(url, headers=header)
    html = bs4.BeautifulSoup(r0.content)
    csrf = html.find(id="x-csrf-token")['value']
    header['X-Requested-With'] = "XMLHttpRequest" 
    header["X-CSRF-TOKEN"] = csrf
    r = s.post(url, headers=header, data=data)
    if r.content[8] != "0":
        print "用户已选择身份"
    else:
        print data
        print "用户选择[学生]身份成功:"
        m0 = cursor.execute("select nick_name,user_id from xgx_users where phone=%s",phone)
        result0 = cursor.fetchall()
        print result0[0]['user_id']
        print u"当前用户:\t" + result0[0]['nick_name']
        m1 = cursor.execute("select sname from `xgx_schools` where school_id=%s",data['school_id'])
        result1 = cursor.fetchall()
        print u"所在学校:\t" + result1[0]['sname']
#        m2 = cursor.execute("select area_name from xgx_areas where area_id=%s",data['area_id']) 
#        result2 = cursor.fetchall()
#        print u"所在地区:\t" + result2[0]['area_name']
#        m3 = cursor.execute("select job from xgx_user_info where user_id=%s",result0[0]['user_id'])
#        result3 = cursor.fetchall()
#        print u"职业:\t" + result3[0]['job']
        m4 = cursor.execute("select grade_name from xgx_grade where grade_id=%s",data['grade_id'])
        result4 = cursor.fetchall()
        print u"年级:\t" + result4[0]['grade_name']
        m5 = cursor.execute("select gender from xgx_users where user_id=%s",result0[0]["user_id"])
        result5 = cursor.fetchall()
        print u"性别:\t" + result5[0]['gender']
        m6 = cursor.execute("select email, birthday from xgx_users where user_id=%s",result0[0]['user_id'])
        result6 = cursor.fetchall()
        print u"邮箱:\t" + result6[0]['email']
        m7 = cursor.execute("select true_name from xgx_user_info where user_id=%s",result0[0]['user_id'])
        result7 = cursor.fetchall()
        print u"真实姓名:\t" + result7[0]['true_name']
        print u"生日:\t" + str(result6[0]['birthday'])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    user_identify(url_student,data_student,xgx_config.session)
