#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'carlos.cui'
from bs4 import BeautifulSoup
import requests
import json
import logging
import os
import re

try:
    from sh import sed
except Exception as e:
    if os.system('pip install sh') == 0:
        from sh import sed

log_file = '/data/logs/check_html.log'
if not os.path.exists(re.findall('/.*/', log_file)[0]):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=log_file,
                    filemode='ab+')

def Get(url):
    r = requests.get(url)
    html = r.text
    return html

def filter(url):
    soup = BeautifulSoup(Get(url), 'html.parser', from_encoding='utf-8')
    # soup = BeautifulSoup(open('/Downloads/test.html'), 'html.parser', from_encoding='utf-8')
    a = soup.find_all('tr')
    l = list()
    for i in a:
        s = i.get_text().split()
        if s[3] == 'down':
            err_log_record = s[1] + ' ' + s[2] + ' ' + s[3]
            cmd = ''.join(list(['grep -q', ' ', '"', err_log_record, '"', ' ', log_file]))
            if os.system(cmd) != 0:
                l.append(s[1] + ' ' + s[2] + ' ' + s[3])
                logging.warning(s[1] + ' ' + s[2] + ' ' + s[3])
        elif s[3] == 'up':
            log_record = s[1] + ' ' + s[2] + ' ' + s[3]
            cmd = ''.join(list(['grep -q', ' ', '"', log_record, '"', ' ', log_file]))
            if os.system(cmd) == 0:
                sed('-i', '/{log_record}/d', log_file).format(log_record=log_record)

    return l if l else None

def Alert(url, token):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + token

    sum = filter(url)
    if not sum:
        return None
    for i in range(len(sum)):
        payload = {
                "msgtype": "markdown",
                "markdown": {"title":"app报警测试",
                "text": "#### **报警信息: {check_app}** \n\n @186xxxxxxxx 请查看".format(check_app=sum[i])
                 },
                "at": {
                "atMobiles": ["186xxxxxxxx"],
                "isAtAll": True
                 }
        }
        json_data = json.dumps(payload).encode(encoding='utf-8')
        ret = requests.post(api_url, data=json_data, headers=headers)
        r = ret.text
        data = json.dumps(r)
        print(data)

    return True

if __name__ == '__main__':
    token = '3ee20aba6c55414c77e8a05477b75cacd12808751f5c10924e719c883ebaxxxx'
    url = 'http://10.8.12.1:8000/kstat'
    Alert(url, token)
