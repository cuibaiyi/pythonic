# -*- coding:utf-8-*-
import requests
import json

class Zabbix():
    def __init__(self):
        self.url = 'https://149.129.84.9/api_jsonrpc.php'
        self.user = 'Admin'
        self.passwd = 'x4JWhsA#CK^jRnai'
        self.headers = {"Content-Type": "application/json-rpc"}


    def Login(self):
        data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.user,
                    "password": self.passwd
                },
                "id": 1,
                "auth": None
        }
        json_data = json.dumps(data)
        r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
        token = r.json()['result']
        return token


    def Create_host(self, file_path, groupid=''):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                ip = line.strip()
                data = {
                        "jsonrpc": "2.0",
                        "method": "host.create",
                        "params": {
                            "host": ip,
                            "name": ip,
                            "interfaces": [
                                {
                                    "type": 1,
                                    "main": 1,
                                    "useip": 1,
                                    "ip": ip,
                                    "dns": "",
                                    "port": "10050"
                                }
                            ],
                            "groups": [
                                {
                                    "groupid": groupid #dp-nginx
                                }
                            ],
                            "templates": [
                                {
                                    "templateid": "10001" #linux模板id
                                }   #可以添加多个模板，复制dict
                            ],
                            "inventory_mode": 0,
                            "proxy_hostid": "10293" #proxy代理id,没有代理注释掉
                        },
                        "auth": self.Login(),
                        "id": 1
                }
                json_data = json.dumps(data)
                r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
                print(r.json())
        return True


    #获取指定主机组的所有hostid
    def Get_host(self, groupid=''):
        data = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": "[hostid]",
                    "groupids": groupid  #组id
                },
                "auth": self.Login(),
                "id": 1
        }
        json_data = json.dumps(data)
        r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
        d = json.loads(r.text)
        data = list()
        sum = len(d['result'])
        for i in range(sum):
            data.append(d['result'][i]['hostid'])
        return data


    #删除一个指定组的所有主机
    # def Delete_host(self, groupid=''):
    #     for hostid in self.Get_host(groupid):
    #         data = {
    #                 "jsonrpc": "2.0",
    #                 "method": "host.delete",
    #                 "params": [
    #                      hostid  #主机id号
    #                 ],
    #                 "auth": self.Login(),
    #                 "id": 1
    #         }
    #         json_data = json.dumps(data)
    #         r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
    #         print(r.text)
    #     return True


    #更新主机宏变量
    def Update_host(self, groupid=''):
        for hostid in self.Get_host(groupid):
            data = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {
                        "hostid": hostid,
                        "macros": [
                            {
                                "macro": "{$REGION}",
                                "value": "eu"
                            }
                        ]
                    },
                    "auth": self.Login(),
                    "id": 1
            }
            json_data = json.dumps(data)
            r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
            print(r.text)
        return True


if '__main__' == __name__:
    obj = Zabbix()
    print(obj.Get_host())
    # print(obj.Create_host(file_path='/Users/cby/Desktop/zabbix_host.log', groupid=16 ))
    # print(obj.Update_host())