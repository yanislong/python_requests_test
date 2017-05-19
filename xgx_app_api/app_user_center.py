#!/usr/bin/python
# -*-coding=utf-8 -*-

import requests

def user_information():
    url = "http://cuimingwen.api.xueguoxuewang.cn/v1/user/center"
    header = {}
    data = {}
    r = requests.get(url)
    print r.content

if __name__ == "__main__":
    user_information()
