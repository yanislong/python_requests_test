#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import xgx_login_0217

s = requests.Session()
url = "http://www.xueguoxue.com"
header = {}
header['cookie'] = "course_xueguoxue_session=" + xgx_login_0217.login()
r = s.get(url, headers=header)
print r.status_code
print r.content
