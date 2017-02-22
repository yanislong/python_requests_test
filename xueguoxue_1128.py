#!/usr/bin/python
#-*-coding:utf-8 -*-

import requests
import hashlib
import re
import bs4
import sys
import time
import json
import threading
import random

if len(sys.argv) > 2:
    username = sys.argv[1]
    password = sys.argv[2]
else:
    print "请输入参数用户名和密码!"
    sys.exit()

class login_user():

    url_0 = "http://passport.xueguoxuewang.cn/login"
    url_1 = "http://course.lihailong.xueguoxuewang.cn/"
    url_2 = "http://course.lihailong.xueguoxuewang.cn/login"
    xgx = ''
    
    def __init__(self,phone,password):
        self.phone = phone
        m2 = hashlib.md5()
        m2.update(password)
        self.password = m2.hexdigest()
        self.xgx = self.login()
#        self.c_pic = self.course_pic() #课程图
#        self.c_b_pic = self.course_back_pic() #课程背景图
#        self.c_doc = self.course_doc() #课程附件
#        self.jg_wuzheng = self.jigou_wuzheng() #机构五证图
#        self.jg_logo = self.jigou_logo() #机构logo图
#        self.up_view = self.upload_view() #课时视频
#        self.course = self.teacher_course() #课程id
        print "xueguoxuewang_session:\n" + self.xgx

    def get_re_xsrf(self,sss):
        sss = str(sss)
        l1 = re.compile(r'XSRF-TOKEN=(.*?;)')
        return l1.findall(sss)
        
    def get_re_xueguoxue(self,sss):
        sss = str(sss)
        l1 = re.compile(r'xueguoxue_session=(.*?;)')
        return l1.findall(sss)

    def get_re_xueguoxuewang(self,sss):
        sss = str(sss)
        l1 = re.compile(r'xueguoxuewang_session=(.*?;)')
        return l1.findall(sss)

    def get_re_csrf(self,sss):
        #l1 = re.compile(r'content":(.*?")')
        suop = bs4.BeautifulSoup(sss)
        l1 = re.compile(r'csrfToken":"(.*)"')
        l2 = l1.findall(str(soup.script))
        l2 = str(l2)[2:-2]
        return l2

#用户登录
    def login(self):
        s = requests.Session()
        r = s.get("http://course.lihailong.xueguoxuewang.cn/login",allow_redirects=False)
        xgxw = r.headers['set-cookie']
        l1 = re.compile(r'xueguoxuewang_session=(.*?;)')
        l2 = l1.findall(xgxw)
        url = r.headers['Location']
        header = {}
        header['cookie'] = 'xueguoxuewang_session=' + l2[0]

        r1 = s.get(url,headers=header,allow_redirects=True)
        html = bs4.BeautifulSoup(r1.text)
        tok = r1.headers['set-cookie']
        ll1 = re.compile(r'csrfToken":"(.*)"')
        ll2 = ll1.findall(str(html.script))
        csrf = str(ll2)[2:-2]
        n1 = re.compile(r'XSRF-TOKEN=(.*?;)')
        n2 = n1.findall(tok)
        k1 = re.compile(r'xueguoxue_session=(.*?;)')
        k2 = k1.findall(tok)

        data = {}
        header['cookie'] = 'xueguoxuewang_session=' + str(l2[0]) +'XSRF-TOKEN=' + str(n2)[2:-2] + "xueguoxue_session=" + str(k2)[2:-2]
        header['content-type'] = 'application/x-www-form-urlencoded'
        data = {'_token':csrf,'phone':self.phone,'password':self.password}
        header['referer'] = 'http://passport.xueguoxuewang.cn/login'
        r2 = s.post("http://passport.xueguoxuewang.cn/login",data=data,headers=header,allow_redirects=True)
        y1 = re.compile(r'xueguoxuewang_session=(.*?;)')
        y2 = y1.findall(r2.headers['set-cookie'])
        if y2 != "":
            print "user login success !"
        else:
            print "user login false!!"
            sys.exit()
        return str(y2)[2:-2]


#老师认证
    def teacher_authentication(self):
        submit_addr = "http://course.lihailong.xueguoxuewang.cn/u/tauth"
        s = requests.Session()
        time.sleep(2)
        header = {}
        data = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r_authentication = s.get(submit_addr,headers=header)
        html = bs4.BeautifulSoup(r_authentication.text)
        token_name = html.find(id="hiddenInput")['name']
        token_value = html.find(id="hiddenInput")['value']
        return token_name,token_value

    def teacher(self):
        s = requests.Session()
        test = self.teacher_authentication()
        submit_addr = "http://course.lihailong.xueguoxuewang.cn/u/tauth"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        header['X-Requested-With'] = 'XMLHttpRequest'
        data = {}
        data['xname'] = "".join(random.sample(u'不是诚心诚意的祈祷我就能回到生命中最美好的时光一直以为那就天堂那时候最爱的女人陪在身旁abc',random.randint(2,4)))
        data['xid_card'] = "34240119880701001X"
        data['xeducation_id'] = str(random.randrange(10,70,10))
        youshi = ['行尸走肉','金蝉脱壳','百里挑一','金玉满堂','背水一战','霸王别姬','9999','<br>','"[]"','堕落天使']
        you = random.sample(youshi,random.randint(1,10))
        ss = ""
        for i in range(len(you)):
            ss = ss + you[i] + ','
        data['xsuperiority'] = ss
        data['xbio'] = "很多时候，一个人的性格，会影响他的职业。做这一行最大的好处就是不用做决定。谁该死，时间，地点，别人早就决定好了。我是个很懒的人，我喜欢别人替我安排一切。所以我需要一个拍档。"
        img_0 = self.upload_acaimg()
        img_1 = self.upload_cerimg()
        data['xacademic_certificate'] = json.dumps({"state":"true","result":{"originalName":img_0,"fileSrc":img_0}})
        data['xteacher_certification'] = json.dumps({"state":"true","result":{"originalName":"img_1","fileSrc":img_1,"keyWord":"","size":""}})
        data['address'] = "ss-ss"
        data['addresscode'] = str(random.randint(1,20)) + "-100" + str(random.randint(1,5))
        data[test[0]] = test[1]
        #data['xacademic_certificate']['result']['fileSrc'] = "http://testgxres.ufile.ucloud.com.cn/5Yfdwx7g4sDerR3bqbIKWgBcCtD1UWTc.jpg"
        #data['xacademic_certificate']['result']['originalName'] = "http://testgxres.ufile.ucloud.com.cn/5Yfdwx7g4sDerR3bqbIKWgBcCtD1UWTc.jpg"
        #data['xteacher_certification']['result']['fileSrc'] = "http://testgxres.ufile.ucloud.com.cn/5Yfdwx7g4sDerR3bqbIKWgBcCtD1UWTc.jpg"
        #data['xteacher_certification']['result']['originalName'] = "http://testgxres.ufile.ucloud.com.cn/5Yfdwx7g4sDerR3bqbIKWgBcCtD1UWTc.jpg"
        print "请求主体:\n" + str(data)
        r = s.post(submit_addr, data=data, headers=header)
        if r.status_code == 200:
            print "服务端返回状态码:\n" + str(r.status_code)
            print "服务端返回:\n" + r.content
        else: 
            print "服务端返回错误，程序退出"
            sys.exit()
        self.logout()
        print "用户退出"

#老师认证上传图片
    def upload_acaimg(self):
        header ={}
        header['cookie'] = "xueguoxuewang_session=" + str(self.xgx)
        #header['content-type'] = "multipart/from-data"
        s = requests.Session()
        file = {'file':open('/root/Desktop/tx/'+ str(random.randint(1,24)) +'.jpeg','rb')}
        url = "http://course.lihailong.xueguoxuewang.cn/u/tauth/uploadTeacherAcademicPic"

        up_img_0 = s.post(url, files=file, headers=header)
        if up_img_0.status_code == 200:
            print up_img_0.text
            print "img is success"
        else:
            print "img is error"
        tt = "".join(up_img_0.text)
        l1 = re.compile(r'fileSrc":"(.*?)",')
        l2 = l1.findall(str(tt))
        l2 = str(l2)[2:-2]
        l3 = l2.replace('\\','')
        print up_img_0.content
        return l3

    def upload_cerimg(self):
        s = requests.Session()
        file = {'file':open('/root/Desktop/ziliao/' + str(random.randint(1,24)) + '.jpeg','rb')}
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + str(self.xgx)
        url_1 = "http://course.lihailong.xueguoxuewang.cn/u/tauth/uploadTeacherCertificatePic"
        up_img_1 = s.post(url_1, files=file, headers=header)
        tt1 = "".join(up_img_1.text)
        ll1 = re.compile(r'fileSrc":"(.*?)",')
        #yy1 = re.compile(r'originalName":"(.*?)",')
        ll2 = ll1.findall(str(tt1))
        #yy2 = yy1.findall(str(tt1))
        ll2 = str(ll2)[2:-2]
        #yy2 = str(yy2)[2:-2]
        ll3 = ll2.replace('\\','')
        #yy3 = yy2.replace('\\','')
        print up_img_1.content
        return  ll3

#机构认证
    def organization(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/u/oauth" 
        header = {}
        data = {}
        header['cookie'] = "xueguoxuewang_session=" + str(self.xgx)
        r = s.get(url, headers=header)
        html = bs4.BeautifulSoup(r.text)
        if (html.find(id="hiddenInput")):
            token_name = html.find(id="hiddenInput")['name']
            token_value = html.find(id="hiddenInput")['value']
        else:
            print r.content
            sys.exit()
        header['X-Requested-With'] = 'XMLHttpRequest'
        #img_wuzheng = 'http:\\/\\/testgxres.ufile.ucloud.com.cn\\/aWg7KaQLDCYDVrnAD85cI3vmFpJFBcCE.jpg'
        #img_logo = 'http:\\/\\/testgxres.ufile.ucloud.com.cn\\/Mji2gGnMOyl2RmykwFI5SRuzK26SHdFF.jpg'
        data[token_name] = token_value
        data['oaddresscode'] = "1-1008"
        data['oaddress'] = "dizh<"
        data['organization_name'] = "org_nam<"
        data['osuperiority'] = "ority<"
        data['organizing_institution_bar_code'] = "12345678-0"
        data['obusiness_license_code'] = "123123123112312"
        data['odetailed_address'] = "obeta_address<"
        data['olegal_person'] = "abcd"
        data['otelephone'] = "13141032576"
        data['ophone'] = "13141032577"
        data['oemail'] = "1@q.com"
        data['obio'] = "abcdefghijk<"
        data['organization_logo'] = self.jg_logo
        data['organization_card'] = self.jg_wuzheng
        print data
        organization = s.post(url,data=data,headers=header)
        print organization.text

#上传机构logo
    def jigou_logo(self):
        url = "http://course.lihailong.xueguoxuewang.cn/u/oauth/uploadOrganCertificatePic"
        header = {}
        file = {"file":open('/root/Desktop/aa.jpg','rb')}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        logo = requests.post(url,files=file,headers=header)
        tt = str(logo.text)
        l1 = re.compile(r'fileSrc":"(.*?)",')
        l2 = l1.findall(tt)
        l2 = str(l2)[2:-2]
        return l2
        
    def jigou_wuzheng(self):
        url = "http://course.lihailong.xueguoxuewang.cn/u/oauth/uploadOrganAcademicPic"
        header = {}
        file = {"file":open('/root/Desktop/bb.jpg','rb')}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        wuzheng = requests.post(url,files=file,headers=header)
        tt = wuzheng.content
        l1 = re.compile(r'fileSrc":"(.*?)",')
        l2 = l1.findall(tt)
        l2 = str(l2)[2:-2]
        return l2

    def ww(self):
        for i in range(400):
            t = threading.Thread(target=self.upload_cerimg,args=())
            t.start()
            print i

#基本资料
    def user_info(self):
        header = {}
        data = {}
        url = "http://course.lihailong.xueguoxuewang.cn/u/info/save"
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r = requests.get("http://course.lihailong.xueguoxuewang.cn/u/info",headers=header)
        html = bs4.BeautifulSoup(r.text)
        token_name = html.find(id="hiddenInput")['name']
        token_value =  html.find(id="hiddenInput")['token']
#        print r.status_code
        data['email'] = "12@q.com"
        data['gender'] = "10"
        data['industry'] = "12345678901234567890"
        data['idiograph'] = "\u003cimg data-osrc=1 onerror=alert(/xss/)\u003e"
        data['birthday'] = "1930-12-04"
        data['user_id'] = "29"
        data['nick_name'] = "testster"
        data[token_name] = token_value
        header['X-Requested-With'] = "XMLHttpRequest"
        info = requests.post(url, headers=header, data=data)
        print info.text
        print info.status_code

#添加收货地址
    def add_address(self):
        url = "http://course.lihailong.xueguoxuewang.cn/u/address/save"
        url_1 = "http://course.lihailong.xueguoxuewang.cn/u/address"
        header = {}
        data = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r = requests.get(url_1, headers=header)
        rr = bs4.BeautifulSoup(r.text)
        if (rr.find(id="hiddenInput")):
            token_name = rr.find(id="hiddenInput")['name']
            token_value = rr.find(id="hiddenInput")['token']
        else:
            print r.content
            sys.exit()
        data['recipients'] = "用来接收订"
        data['area_code'] = "1-1007"
        data['detailed_address'] = "用来接收订单提醒邮件用来接收订单提醒邮件用来接收订单提醒邮件用来接收订单订单提醒邮件<a"
        data['phone'] = "13141032576"
        data['telephone'] = "010-88899900"
        data['email'] = '1@qq.com'
        data['alias_name'] = "<br>"
        data[token_name] = token_value
        add = requests.post(url, data=data, headers=header)
        print add.status_code
        #print add.headers
        print add.text

#删除收货地址
    def del_address(self):
        s = requests.Session()
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r = s.get("http://course.lihailong.xueguoxuewang.cn/u/address",headers=header)
        html = bs4.BeautifulSoup(r.text)
        if (html.find("p",class_='clearfix')):
            id = html.find("p",class_='clearfix')['addid']
            pass
        else:
            print "not have address"
            sys.exit()
        print "delete address_id: %s" % id
        url = "http://course.lihailong.xueguoxuewang.cn/u/address/delete"
        data = {"address_id":85}
        addr = s.delete(url, params=data,headers=header)
        print addr.status_code
        #print addr.headers
        print addr.url
        print addr.text
        
#老师发课
    def teacher_course(self):
        s = requests.Session()
        header = {}
        data = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/course"
        #header['content-type'] = "application/x-www-form-urlencoded"
        global num
        num = num + 1
        mm = random.randrange(30,31,10)
        if mm == 20:
            data['sales_method'] = str(mm)
            data['original_cost'] = str(random.randint(2,9999))
            data['average_price'] = str(random.randint(2,9999))
            data['cost_price'] = "1"
            print data['average_price']
            data['title'] = "[单课时均价]不管怎样，我终相信这个世界是美好的。" + str(num)
        elif mm == 30:
            data['sales_method'] = str(mm)
            data['title'] = "[单课时单价]要是我的生命只剩一天，那么我选择和你在一起" + str(num)
        elif mm == 10:
            data['sales_method'] = "10"
            data['original_cost'] = str(random.randint(2,9999))
            data['selling_price'] = str(random.randint(2,9999))
            data['cost_price'] = "1"
            data['title'] = "[正常销售]做人如果没梦想，那跟咸鱼有什么分别？" + str(num)
        data['course_synopsis'] = "[course_synopsis] 风往哪个方向吹，草就要往哪个方向倒。年轻的时候，我也曾经以为自己是风，可是最后遍体鳞伤，我才知道，我们原来都只是草" + str(num)
        data['course_pic'] = self.c_pic
        data['course_bg_pic'] = self.c_b_pic
        a = []
        for i in range(10):
            a.append(self.course_doc())
        b = tuple(a)
        data['course_docs[]'] = b
#        data['speaker_teacher'] = "".join(random.sample("abcdefghijklmnopqrstuvwxyz",4))
#        data['speaker_teacher'] = "".join(random.sample(u'赵钱孙李周吴郑王',1)) + "".join(random.sample(u'爱过所以慈悲因为懂得宽容',2))
        f = open('/root/test1','rb')
#        print f.read()
        data['course_presentation'] = "this is<script>alert(document.cookie)</script> course_presentation<input type='password'>,我们一路奋战，不是为了改变世界，而是为了不让世界改变我们,<I alt='s' SRC='https://a-ssl.duitang.com/uploads/item/201503/07/20150307220811_BxBzr.thumb.224_0.jpeg'>" + f.read()
        data['category_ids[]'] = (random.randint(4,15),random.randint(16,18))
        data['tag_ids[]'] = (random.randint(1,26),random.randint(1,26),random.randint(1,26))
        data['shopping_guide'] = "this is shopping_guide,你爱怎么卖就怎么卖" 
        #data['check_status'] = "1"
        f.close()
#        data['original_cost'] = str(random.randint(2,9999))
#        data['selling_price'] = str(random.randint(2,9999))
#        data['cost_price'] = "1"
        course = s.post(url, data=data, headers=header)
        print course.content
        l1 = re.compile(r'cid":"(.*?)"')
        l2 = l1.findall(course.text)
        return str(l2)[3:-2],mm

#上传课程图
    def course_pic(self):
        s = requests.Session()
        header = {}
        header['cookie'] = 'xueguoxuewang_session=' + self.xgx
        #header['content-type'] = "multipart/form-data"
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/cpics"
        file = {'file':open(r'/root/Desktop/ziliao/'+ str(random.randint(412,436)) + '.jpeg','rb')}
        course_pic = s.post(url,headers=header,files=file)
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
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        file = {'file':open('/root/Desktop/tu/' + str(random.randint(1,9)) + '.jpeg','rb')}
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/cbgpics"
        back_pic = s.post(url, files=file, headers=header)
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
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        file = {'file':open('/root/Desktop/bbb.pdf','rb')}
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/docs"
        doc = s.post(url, files=file, headers=header)
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
    def course_keshi(self,n):
        s = requests.Session()
        header = {}
        data = {}
        self.n = n
        global num
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/period"
        data = {}
        #print self.up_view
        data['video_src'] = self.upload_view()
        data['videoTitle'] = "this is title,特立独行，哗众取宠" + str(self.n)
        data['period_bio'] = "{this is bio}你以为躲起来就找不到你了吗？没有用的！象你这样出色的男人，无论在什么地方，都像漆黑中的萤火虫一样，那样的鲜明，那样的出众。你那忧郁的眼神，稀嘘的胡喳子，神乎其神的刀法，和那杯Dry Martine，都深深地迷住了我。不过，虽然这是这样的出色，但是行有行规，无论怎样你要付清昨晚的过夜费呀，叫女人不用给钱吗?"

        if self.course[1] == 10:
            if self.n % 2 == 0:
                data['sales_method'] = "20"
                data['try_play'] = "10"
                data['videoType'] = "free"
                data['period_title'] = "[免费]每个曾经想改变中国的人，都被中国所改变" + str(self.n)
            else:
                data['period_title'] = "[收费]每个曾经特立独行的人，都抛弃了曾经的自己" + str(self.n)
                data['sales_method'] = "20"
                data['videoType'] = "charge"

        elif self.course[1] == 20:
            if self.n % 2 == 0:
                data['sales_method'] = "20"
                data['try_play'] = "10"
                data['videoType'] = "free" 
	        data['period_title'] = "[免费]每个曾经特立独行的人，都抛弃了曾经的自己" + str(self.n)
            else:
                data['period_title'] = "[收费]每个曾经想改变中国的人，都被中国所改变" + str(self.n)
                data['sales_method'] = "20"
                data['videoType'] = "charge"

        elif self.course[1] == 30:
            if self.n % 2 == 0:
                data['sales_method'] = "30"
                data['try_play'] = "10"
                data['videoType'] = "free"
                data['period_title'] = "[免费]每个曾经特立独行的人，都抛弃了曾经的自己" + str(self.n)
            else:
                data['period_title'] = "[收费]每个曾经想改变中国的人，都被中国所改变" + str(self.n)
                data['original_price'] = str(random.randint(9998,9999))
                data['price'] = str(random.randint(9998,9999))
                data['cost_price'] = "1"
                data['sales_method'] = "30"
                data['videoType'] = "charge"

        #data['price'] = "10"
        #data['cost_price'] = "1"
        data['cid'] = self.course[0]
#        print data
        r = s.post(url, headers=header, data=data)
        print r.content

#上传课时视频
    def upload_view(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/u/resource/upload/videos?cid=" + self.course[0]
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        file = {'file':open('/root/Desktop/2017.mp4','rb')}
        r = s.post(url, files=file, headers=header)
        print r.content
        l1 = re.compile(r'src":"(.*?)"')
        l2 = l1.findall(r.content)
        print "上传课时视频成功: %s" % str(l2)[2:-2] 
        return str(l2)[2:-2]
  
#提交审核
    def submit_course(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/u/issue/submitAudit"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        data = {'cid':self.course[0]}
        r = s.post(url, headers=header, data=data)
        print r.content
        print r.url

#课程讨论组发起讨论
    def content(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/c/u/discussion/save"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        data = {}
        data['content'] = "天空灰的像哭过\n离开你以后并没有更自由\n酸酸的空气嗅出我们的距离\n一幕锥心的结局像呼吸般无法停息"
        data['course_id'] = "7831"
        r = s.post(url,headers=header,data=data)
        print r.text
    
#课程讨论组发起回复        
    def huifu(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/c/u/discussion/save"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        data = {}
        data['content'] = "天空灰的像哭过\r离开你以后并没有更自由\r酸酸的空气嗅出我们的距离\r一幕锥心的结局像呼吸般无法停息"
        data['course_id'] = "7831"
        data['at_who_id'] = "28"
        data['parent_id'] = "442"
        r = s.post(url,headers=header,data=data)
        print r.text

#课程咨询
    def course_question(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/consult/ask"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        data = {}
        data['id'] = random.randint(9310,9312)
        data['type'] = "1"
        data['question'] = "辩方律师请回到：你到底爱不爱我"
        r = s.post(url, headers=header, data=data)
        print r.text

#课程收藏
    def collection(self):
        s = requests.Session()
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        url = "http://course.lihailong.xueguoxuewang.cn/u/pickupfavorites/"
        data = ""
        for i in xrange(100):
            r = s.get(url+str(random.randint(9000,9600)),headers=header)
            print r.content
        
#关注
    def focus(self):
        s = requests.Session()
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        url = "http://course.lihailong.xueguoxuewang.cn/u/hurteachother/"
        numm = str(random.randint(1,60))
        url1 = url + "73"
        data = ""
        for i in range(1):
            r = s.get(url1, headers=header)
            print r.content

#添加购物车
    def add_cart(self,gou_num):
        self.gou_num = gou_num
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/shopping/cart/addToCart2"
        header = {}
        data = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        header['X-Requested-With'] = "XMLHttpRequest"
#        cc = (self.gou_num,)
        data['course_id'] = ("10750","10754")
#        data['period_id[]'] = "29849" #("28298","28299")
#        for i in range(10594,10640):
#            data['course_id'] = i
#        pp = ('28266',) 
#        kk = []
#        for i in range(28200,28207):
#            kk.append(i)
#            ss = tuple(kk)
#            data['period_id[]'] = ss #self.gou_num
#            print i - 28158
#        print data
        r = s.post(url, headers=header, data=data)
        print r.content

#从购物车中移除
    def remove_cart(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/shopping/cart/removeSkuFromCart"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        data = {}
        dd = ('351')
        data['cart_id'] = dd
        r = s.post(url, headers=header, data=data)
        print r.content

#查看购物车
    def show_cart(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/shopping/getCartList"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r = s.get(url, headers=header)
        print r.content

#生成预订单
    def edit_order(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/shopping/order/getPreOrderId"
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        header['X-Requested-With'] = "XMLHttpRequest"
        data = {}
        r = s.get(url, headers=header)
        print "生成预订单 -->>" + r.content
        l1 = re.compile(r'OrderId":"(.*?)"')
        l2 = l1.findall(r.content)
        l3 = str(l2)[2:-2]
        return l3

#生成订单
    def order(self):
        s = requests.Session()
        url = "http://course.lihailong.xueguoxuewang.cn/shopping/order/getOrderData/" + self.edit_order()
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + self.xgx
        r = s.get(url, headers=header)
#        print r.content
        l1 = re.compile(r'preOrderId":"(.*?)"')
        l2 = l1.findall(r.content)
        print l2
        url1 = "http://course.lihailong.xueguoxuewang.cn/shopping/order/submitOrder"     
#        header['X-Requested-With'] = "XMLHttpRequest"
        data = {}
        data['preOrderId'] = str(l2)[2:-2]
        data['addressId'] = "134"
        data['billTitleId'] = "0"
        data['billTitleType'] = ""
        r1 = s.post(url1, headers=header, data=data)
        print r1.content
    

#用户退出
    def logout(self):
        wang_session = requests.Session()
        header = {}
        header['cookie'] = "xueguoxuewang_session=" + str(self.xgx)
        r0 = wang_session.get("http://course.lihailong.xueguoxuewang.cn/u/issue/course",headers=header)
        html = bs4.BeautifulSoup(r0.content)
        tt = html.find(id="x-csrf-token")['value']
        print tt
        data = {}
        data = {'__token':tt}
        r_logout = wang_session.post("http://course.lihailong.xueguoxuewang.cn/logout",headers=header, data=data)
        print r_logout.status_code
        print  "user logout success"
        return True

num = 1
f = open('/root/register_user.txt','r')
#f = open('/root/teacher_acc.txt','r')
'''
for i in xrange(1):
    user = (f.readline()).strip()
    print user
    a = login_user("","")
    for j in range(1):
        print "start %d" % j
        t = threading.Thread(target=a.focus,args=())
        t.start()
        t.join()
#    a.submit_course()
f.close()
'''
a = login_user(username,password)
#a.teacher_authentication()
#a.teacher()
#a.organization()
#a.jigou_logo()
#a.jigou_wuzheng()
#a.upload_acaimg()
#a.upload_cerimg()
#a.del_address()
#for i in range(5):
#a.add_address()
#a.user_info()
#a.course_pic()
#a.course_back_pic()
#a.course_doc()
#a.teacher_course()
#a.upload_view()
#a.course_keshi()
#a.submit_course()
'''
for i in xrange(52):
    print 'this is %d' %i
    a.content()
for i in xrange(10):
    print "this is %s" %i
    a.huifu()
for i in range(103):
    print "this is %s" %i
    a.course_question()
'''
#a.collection()
#a.focus()
#for i in  range(28158,28258):
#a.add_cart(1)
#a.remove_cart()
#a.show_cart()
#a.order()
#a.logout()
