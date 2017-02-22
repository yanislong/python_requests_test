#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import xgx_login_0217
import xgx_config

s = requests.Session()
url = xgx_config.url_test
header = {}
header['cookie'] = "course_xueguoxue_session=" + xgx_login_0217.login()
r = s.get(url, headers=header)
print r.content
print r.status_code
