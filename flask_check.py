import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        post_data = request.get_data()
        send_alert(bytes_json(post_data))
        return 'success'
    else:
        return 'no!'

def bytes_json(data_bytes):
    data = json.loads(data_bytes.decode('utf8').replace("'", '"'))
    return data

def send_alert(data):
    token = os.getenv('ROBOT_TOKEN')
    if not token:
        print('请设置ROBOT_TOKEN变量指定钉钉token')
        return None
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token
    send_data = {
        "msgtype": "text",
        "text": {
            "content": bytes_json()
        }
    }
    r = requests.post(url, json=send_data)
    result = r.json()
    if result['errcode'] != 0:
        print('钉钉报错: %s' % result['errcode'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
