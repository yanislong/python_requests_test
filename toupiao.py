#!/usr/bin/python
# -*-coding:utf-8 -*-

import requests
import random
import time

url = "http://wcb.cccinst.org/vote.php"
header = {}
header['X-forwarded-for'] = "114.238.238.239"
header['X-Requestsed-With'] = "XMLHttprequest"
header['cookie'] = "PHPSESSID=vruo7706ojuiqjtrmqjk38v247;"
proxie = {'http':'http://14.211.144.113:9797'}
data = {'action':'add','code':'tkzw','data':' ,c132,c150'}
for i in range(1,100):
    for j in range(1,5):
        time.sleep(random.randint(1,10))
        header['X-forwarded-for'] = random.choice(['203','61','211','124']) + "." + random.choice(['13','235','36','241','92','166']) + "." + str(random.randint(100,220)) + "." + str(random.randint(10,210))
        print header['X-forwarded-for']
        r = requests.post(url, headers=header,data=data, proxies=proxie)
        print r.content
