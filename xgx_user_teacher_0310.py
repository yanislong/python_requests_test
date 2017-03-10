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

data_teacher = {}
data_teacher['true_name'] = "name"
data_teacher['certificate'] = "10"
data_teacher['subject_id'] = "1"
data_teacher["school_id"] = "1"
data_teacher["grade_id"] = "6"
data_teacher['email'] = "1@q.con"
data_teacher['advantage'] = "df"
data_teacher["area_id"] = "1001"
data_teacher["gender"] = "10"

def user_identify(url, data_identify,xgx):
    global phone
    conn = pymysql.connect(host="172.16.9.238",user="root",passwd="xueguoxue",db="xgx_course",charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    effect_row = cursor.execute("UPDATE `xgx_users` SET role_id=0  WHERE phone=%s",phone)
    if  effect_row == 1:
        print "用户身份重置成功"
    else:
        print "用户手机号不存在或用户未选择身份，进行身份选择..."
    conn.commit()
    r_data = data_identify
    header = {}
    s = requests.Session()
    header['cookie'] = "course_xueguoxuewang_session=" + xgx
    r0 = s.get(url, headers=header)
    html = bs4.BeautifulSoup(r0.content)
    csrf = html.find(id="x-csrf-token")['value']
    header['X-Requested-With'] = "XMLHttpRequest" 
    header["X-CSRF-TOKEN"] = csrf
    r = s.post(url, headers=header, data=r_data)
    if r.content[8] != "0":
        print "用户已选择身份"
    else:
        print "接口传递参数:"
        print r_data
        m0 = cursor.execute("select nick_name,user_id from xgx_users where phone=%s",phone)
        result0 = cursor.fetchall()
        print result0[0]['user_id']
        print u"当前用户:\t" + result0[0]['nick_name'] + u"||\t选择[老师]身份成功,数据库实际数据:"
        m1 = cursor.execute("select sname from `xgx_schools` where school_id=%s",r_data['school_id'])
        result1 = cursor.fetchall()
        print u"所在学校:\t" + result1[0]['sname']
        m2 = cursor.execute("select area_name from xgx_areas where area_id=%s",r_data['area_id']) 
        result2 = cursor.fetchall()
        print u"所在地区:\t" + result2[0]['area_name']
        m3 = cursor.execute("select job, subject_id, certificate, advantage from xgx_user_info where user_id=%s",result0[0]['user_id'])
        result3 = cursor.fetchall()
        print u"职业:\t" + result3[0]['job']
        m4 = cursor.execute("select grade_name from xgx_grade where grade_id=%s",r_data['grade_id'])
        result4 = cursor.fetchall()
        print u"年纪:\t" + result4[0]['grade_name']
        m5 = cursor.execute("select gender from xgx_users where user_id=%s",result0[0]["user_id"])
        result5 = cursor.fetchall()
        print u"性别:\t" + result5[0]['gender']
        m6 = cursor.execute("select email from xgx_users where user_id=%s",result0[0]['user_id'])
        result6 = cursor.fetchall()
        print u"学科:\t" + str(result3[0]['subject_id'])
        print "学历:\t" + str(result3[0]['certificate'])
        print u"优势:\t" + result3[0]['advantage']
        print "邮箱:\t" + str(result6[0]['email'])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    user_identify(url_teacher,data_teacher,xgx_config.session)
