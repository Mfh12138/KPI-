import json
import requests

WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=a86dfb27606676d63560637891d0e6443bbbe9f2858d065c2489747959539a7d'
TITLE = '群发消息'
def send_text_msg(message):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
            'msgtype': 'text',
            'text': {
                'title': TITLE,
                "content": message,
                'messageUrl': 'http://请求IP+端口号'
            },
            'at': {
                    'atMobiles': [
                        '群消息@的用户1',
                        '群消息@的用户2'
                    ],
                    'isAtAll': False
            }
    }
    post_data = json.dumps(data)
    response = requests.post(WEBHOOK, headers=headers, data=post_data)
    return response.text

def send_pic(name):
    ddurl='https://oapi.dingtalk.com/robot/send?access_token=ae06afc1139180419e341e67022015c09cd7533c44a24bb4a480491aa9593754'   #钉钉机器人api地址
    picurl = 'http://139.217.2.199/pic/{}'.format(name)   #图片地址,公网可访问到的地址
    print(type(picurl), picurl)
    phone = ['15988817534']

    postData = {
        "msgtype": "markdown",
         "markdown": {
             "title": "图片标题",
             "text":
                     "> ![screenshot]({})\n".format(picurl)
             },
         "at": {
            "atMobiles": phone,
            "isAtAll": 0           # 0是@部分人，1是@所有人。
         }
    }
