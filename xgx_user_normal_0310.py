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

data_normal = {}
data_normal["birthday"] = "2013-12-12"
data_normal["email"] = "6@q.cn"
data_normal["job"] = "test"
data_normal['gender'] = "20"
data_normal["like[]"] = "1"
data_normal["like_name[]"] = "s"

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
        print "用户选择[普通]身份成功:"
        m0 = cursor.execute("select nick_name,user_id from xgx_users where phone=%s",phone)
        result0 = cursor.fetchall()
        print result0[0]['user_id']
        print u"当前用户:\t" + result0[0]['nick_name']
#        m1 = cursor.execute("select sname from `xgx_schools` where school_id=%s",data['school_id'])
#        result1 = cursor.fetchall()
#        print u"所在学校:\t" + result1[0]['sname']
#        m2 = cursor.execute("select area_name from xgx_areas where area_id=%s",data['area_id']) 
#        result2 = cursor.fetchall()
#        print u"所在地区:\t" + result2[0]['area_name']
        m3 = cursor.execute("select job from xgx_user_info where user_id=%s",result0[0]['user_id'])
        result3 = cursor.fetchall()
        print u"职业:\t" + result3[0]['job']
#        m4 = cursor.execute("select grade_name from xgx_grade where grade_id=%s",data['grade_id'])
#        result4 = cursor.fetchall()
#        print u"年纪:\t" + result4[0]['grade_name']
        m5 = cursor.execute("select gender, email, birthday from xgx_users where user_id=%s",result0[0]["user_id"])
        result5 = cursor.fetchall()
        print u"性别:\t" + result5[0]['gender']
        print u"邮箱:\t" + result5[0]['email']
        print u"生日:\t" + result5[0]['birthday']
        m6 = cursor.execute("select like_name from xgx_user_like where like_name=%s",data['like_name[]'])
        result6 = cursor.fetchall()
        print u"关注喜好:\t" + result6[0]['like_name']
        m7 = cursor.execute("select like_id from xgx_user_like where like_id=%s",(data["like[]"]))
        result7 = cursor.fetchall()
        print "关注喜好[系统默认]:\t" + str(result7[0]['like_id'])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    user_identify(url_normal,data_normal,xgx_config.session)
