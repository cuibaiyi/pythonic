#!/usr/bin/env python
# -*- coding:utf-8-*-
import requests
import json

class Check():
    def __init__(self):
        self.url = 'http://118.89.217.80:9093/api/v1/alerts'
        self.token = '3ee20aba6c55414c77e8a05477b75cacd12808751f5c10924e719c883eba7bad'
        self.ding = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.token
        self.headers = {"Content-Type": "application/json"}

    def Get(self):
        ret = requests.get(self.url)
        data = ret.text
        json_data = json.loads(data)
        li = []
        Sum = 1#len(json_data['data'])
        for n in range(Sum):
            d = json_data['data'][n]
            data = {}
            #d = json_data['data'][0]
            data['check_name'] = d['labels']['alertname']
            data['job_name'] = d['labels']['job']
            data['demo'] = d['annotations']['summary']
            data['url'] = d['generatorURL']
            data['startTime'] = d['startsAt']
            data['stopTime'] = d['endsAt']
            li.append(data)
        return (li,Sum) if Sum else None

    def Post(self):
        for i in range(self.Get()[1]):
            d = self.Get()[0]
            payload = {
                "msgtype": "markdown",
                "markdown": {"title":"{job_name}报警".format(job_name=d[i]['job_name']),
                "text": "#### **报警信息: {check_name}** \n\n 1.报警提示: {demo} \n\n 2.[监控详情链接]({url}) \n\n @18610160109 请查看".format(url=d[i]['url'], demo=d[i]['demo'], check_name=d[i]['check_name'])
                 },
                "at": {
                "atMobiles": ["18610160109"],
                "isAtAll": True #False
                 }
            }
            json_data = json.dumps(payload).encode(encoding='utf-8')
            ret = requests.post(self.ding, data=json_data, headers=self.headers)
            r = ret.text
            data = json.dumps(r)
            print(data)
        return True

if '__main__' == __name__:
    obj = Check()
    if obj.Get():
        print(obj.Post())
    else:
        print('没有报警')