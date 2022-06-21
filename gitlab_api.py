#!/usr/bin/env python3.6
# encoding: utf-8
# gitlab api官网: https://docs.gitlab.com/ee/api/members.html

import requests
import json

user = [
    "x1@qq.com@name1",
    "x2@qq.com@name2",
]

url = "http://www.gitlab.com/api/v4/users"
para = {"Content-Type": "application/json", 'PRIVATE-TOKEN': 'LPi3mxxx_BER_'}

def post_rul(url, json_data):
    r = requests.post(url, data=json_data, headers=para)
    return r.json()

for s in user:
    t = s.split("@")
    t1 = t[0]+'@'+t[1]
    data = {
        "email": t1,
        "name": t[2],
        "username": t[0],
        "force_random_password": True,
        "reset_password": True,
    }
    json_data = json.dumps(data).encode(encoding='utf-8')
    d = post_rul(url, json_data)
    print(d)
