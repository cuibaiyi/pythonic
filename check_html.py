#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'carlos.cui'
"""
#__metaclass__ = type
soup.select('div')                  获取所有div标签内的元素
soup.select('#author')              获取id属性为author的
soup.select('p #author')            获取所有id属性为author的元素，只要在p标签内
soup.select('div span')             获取所有在div元素之内的span元素
soup.select('div > span')           获取所有在div元素之内的span元素，中间没有其他元素
soup.select('input[name]')          获取所有名为input，并有一个name属性
soup.select('input[type="button"]') 获取所有名为input，并有一个type属性，其值为button的元素
getText()                           返回元素的文本数据
soup.find_all('a', limit=2)         输出所有的a标签，以列表形式显示,limit可以限制结果个数
soup.find(id="cby_link")            输出第一个id属性等于cby_link的a标签
soup.find_all(text=['down', '23'])  通过文本进行查找
soup.tr.attrs                       获取属性tr标签的所有属性
for i in soup.find_all('tr'):       获取所有tr标签id属性的内容,没有返回None,可以设置第二个参数
    print(i.get('id', 'ok'))
"""
import requests
import json
import logging
import os
import sys
import re

try:
    from bs4 import BeautifulSoup
    from sh import sed
except Exception as e:
    if os.system('pip install beautifulsoup4') == 0:
        from bs4 import BeautifulSoup
    if os.system('pip install sh') == 0:
        from sh import sed

#导入模块        
#cmd_py = ['from bs4 import BeautifulSoup', 'from sh import sed']
#cmd = ['pip install beautifulsoup4', 'pip install sh']
#l = zip(cmd_py, cmd)
#for i in l:
#    try:
#        exec(i[0])
#    except Exception as e:
#        if os.system(i[1]) == 0:
#            exec(i[0])
#        else:
#            sys.exit(1)

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
            err_log_record = ''.join([s[1], ' ', s[2], ' ', s[3]])
            cmd = ''.join(['grep -q', ' ', '"', err_log_record, '"', ' ', log_file])
            if os.system(cmd) != 0:
                l.append(''.join([s[1], ' ', s[2], ' ', s[3]]))
                logging.warning(''.join([s[1], ' ', s[2], ' ', s[3]]))
        elif s[3] == 'up':
            log_record = s[1] + ' ' + s[2] + ' ' + s[3]
            cmd = ''.join(['grep -q', ' ', '"', log_record, '"', ' ', log_file])
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
    token = 'xxxxxx'
    url = 'http://10.0.0.1:8000/kstat'
    Alert(url, token)
