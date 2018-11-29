# -*- coding:utf-8-*-
import requests
import json

class Zabbix():
    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
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


    def Create_host(self, file_path, groupid='', proxyid=None):
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
                                    "groupid": groupid
                                }
                            ],
                            "templates": [
                                {
                                    "templateid": "10001" #linux模板id
                                }   #可以添加多个模板，复制dict
                            ],
                            "inventory_mode": 0,
                            #proxy代理id,没有代理注释掉
                            #"proxy_hostid": proxyid
                        },
                        "auth": self.Login(),
                        "id": 1
                }
                json_data = json.dumps(data)
                r = requests.post(self.url, data=json_data, headers=self.headers, verify=False)
                print(r.json())
        return True


if '__main__' == __name__:
    obj = Zabbix('https://ip/api_jsonrpc.php','Admin', 'passwd')
    print(obj.Create_host(file_path='填写添加的主机ip文件的路径', groupid='填写组id'))
