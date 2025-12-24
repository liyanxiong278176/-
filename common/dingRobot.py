import base64
import hashlib
import hmac
import time
import urllib
import requests

def generate_sign():
    timestamp = str(round(time.time() * 1000))
    secret = 'SECd4381d2b6cc37d41aef49ad84e68dde7b0ef44bda35b640c18383b44bba7e1cb'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign

def send_dingding_message(message,at_all):
    """
    向钉钉群推送消息
    :param message: 消息
    :param at_all: 是否@所有人
    :return:
    """
    timestamp_sign = generate_sign()
    url=f"https://oapi.dingtalk.com/robot/send?access_token=8e930ebdcd5bbe691364be04ad3692950d95dbba6769cf5ba11d5eaf72c457ac&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}"
    headers={"Content-Type":"application/json;charset=utf-8"}
    data={
        "msgtype": "text",
        "text": {
            "content": message
        },
        "at": {
            "isAtAll": at_all
        }
    }
    res=requests.post(url=url,json=data,headers=headers)
    return  res
if __name__ == '__main__':
    print(send_dingding_message("""
    自动化测试报告
    总接口数量:800
    正常：780
    异常：20
    接口报告地址：www.baidu.com
    """,True))