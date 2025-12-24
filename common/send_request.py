import logging

import requests


from common.readyaml import ReadAndWriteYaml
from common.recordlog import logs
from common.request_demo import cookie


class SendRequest(object):
    def __init__(self):
        self.read=ReadAndWriteYaml()


    def send_request(self,**kwargs):
        try:
            cookie={}
            session = requests.session()
            response = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(response.cookies)
            if set_cookie:
                cookie["Cookie"] = set_cookie
                #cookie写入到extract.yaml文件中
                self.read.write_yaml_data(set_cookie)
                logs.info("请求的cookies：{}".format(set_cookie))
            # data = response.json()
            # print("token:",data['token'])
            #token写入extract.yaml文件
            #self.read.write_yaml_data({'token':data['token']})
        except requests.exceptions.ConnectionError:
            logs.error("请求服务器异常")
            pytest.fail("请求服务器异常")
        except requests.exceptions.HTTPError:
            logs.error("请求的接口异常")
            pytest.fail("请求的接口异常")
        except requests.exceptions.RequestException as e:
            logs.error("请求异常：{}".format(e))
            pytest.fail("请求异常：{}".format(e))
        return response

    def run_main(self, api_name,url,method,headers,cookies=None,file=None,**kwargs):
        try:
            logs.info("请求的接口名称：{}".format(api_name))
            logs.info("请求的url：{}".format(url))
            logs.info("请求的method：{}".format(method))
            logs.info("请求的headers：{}".format(headers))
            logs.info("请求的cookies：{}".format(cookies))
            logs.info("请求的file：{}".format(file))
            logs.info("请求的参数：{}".format(kwargs))
        except Exception as e:
            logs.error("请求日志异常：{}".format(e))

        response = self.send_request(method=method, url=url, headers=headers, cookies=cookies, files=file, verify=False, **kwargs)
        logs.info("响应的接口消息：{}".format(response.json()))
        return response

if __name__ == '__main__':
    url = 'http://127.0.0.1:8787/dar/user/login'
    headers = None
    data = {
        "user_name": "test01",
        "passwd": "admin123"
    }
    method="post"
    res = SendRequest().run_main(method=method,url=url, data=data, header=headers)
    print(res)
