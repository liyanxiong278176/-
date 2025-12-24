import requests
from requests import utils
url='http://127.0.0.1:8787/dar/user/login'
headers={
    "Content-Type":"application/x-www-formurlencoded;charset=UTF-8 "
}
data={
    "user_name":"test01",
    "passwd":"admin123"
}
#--------------------post------------------------------
#res是状态码
#表单用data，json用json
# res=requests.post(url=url,data=data)
# #文本
# print(res.text)
# #json
# print(res.json())

#------------------get--------------------------------
url_2='http://127.0.0.1:8787/coupApply/cms/goodsList'
headers_2={
    "Content-Type":"application/x-www-formurlencoded;charset=UTF-8"
}
json_data={
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 20
}
# res_2=requests.get(url=url_2,params=json_data,headers=headers_2)
# print(res_2.text)
# print(res_2.json())
#-----------------------session-------------------------
#通过session管理会话
# session=requests.session()
# res_3=session.request(method="get",url=url_2,params=json_data,headers=headers_2)
# print(res_3.text)


#------------------------cookie--------------------------

session=requests.session()
result=session.request(method="post",url=url,data=data)
cookie=requests.utils.dict_from_cookiejar(result.cookies)
print(cookie)
