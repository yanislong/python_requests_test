#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import requests, urllib
import bs4
import re
import sys

url = "http://upload.polyv.net:1080/files/"
s = requests.Session()
r = s.post(url)
print r.status_code
n = 1000
urllib.urlretrieve(url,'/root/Desktop/doc/' + str(n) + '.mp4')
