import json
import re

from common.assertions import Assertions
from common.debugtalk import DebugTalk
from common.readyaml import ReadAndWriteYaml, get_yaml
from common.recordlog import logs
from common.send_request import SendRequest
from conf.operateconf import OperateConf


class Api:
    """
    *.yaml文件的${}通过read来读取extract.yaml文件的值，然后写会*.yaml
    1*.yaml文件的数据
    2获取每个${}
    3通过反射来使用read下面的方法
    4替换原来*.yaml里${}
    """
    def __init__(self):
        self.read=ReadAndWriteYaml()
        self.conf=OperateConf()
        self.send=SendRequest()
    def analyse_data(self, data):
        """
        :param data: 键
        :return:
        """
        #转换为字符串操作
        str_data=data
        if not isinstance(data,str):
            str_data=json.dumps(data, ensure_ascii=False)
        #获取每个${}
        for i in range(str_data.count("${")):
            if "${" in str_data and "}" in str_data:
                start_index=str_data.index("${")
                end_index=str_data.index("}", start_index)#	返回指定位置后的第一个 }
                fun_and_params=str_data[start_index:end_index+1]
                #获取${}里的值
                fun_name=fun_and_params[2:fun_and_params.index('(')]
                params=fun_and_params[fun_and_params.index('(')+1:fun_and_params.index(')')]
                #通过反射来使用read下面的方法
                extract_data=getattr(DebugTalk(), fun_name)(*params.split(',') if params else None)
                #替换原来*.yaml里${}
                str_data=str_data.replace(fun_and_params,str(extract_data))

        #转换回字典
        if isinstance(data,str):
            data=str_data
        else:
            data=json.loads(str_data)
        return  data

    def specification_yaml(self,baseInfo,testcase):
        """
        :param baseInfo:
        :param testcase:
        :return:
        """
        #获取接口基本消息
        cookie=None
        params_type=['params','data','json']
        api_name=baseInfo['api_name']
        url = self.conf.get_envi('host')+baseInfo['url']
        method = baseInfo['method']
        headers=baseInfo['headers']
        try:
            cookie=baseInfo['cookies']
            cookie=self.analyse_data(cookie)
        except:
            pass

        #获取yaml文件接口参数
        case_name = testcase.pop('case_name')
        validation = testcase.pop('validation')
        extract = testcase.pop('extract', None)
        extract_list = testcase.pop('extract_list', None)
        for key, value in testcase.items():
            if key in params_type:
                # 解析参数
                testcase[key]=self.analyse_data(value)
        # 处理文件上传接口
        file,files=testcase.pop('file', None),None
        if file is not None:
            for fk,fv in file.items():
                #allure.attach_file(json.dumps(file),"导入文件")
                files={fk:{open(fv, 'rb')}}
        # for tc in case_info['testCase']:
        #     case_name = tc.pop('case_name')
        #     validation = tc.pop('validation')
        #     extract = tc.pop('extract', None)
        #     extract_list = tc.pop('extract_list', None)
        #
        #     for key,value in tc.items():
        #         if key in params_type:
        #             # 解析参数
        #             tc[key]=self.analyse_data(value)
        #
        #     #处理文件上传接口
        #     file,files=tc.pop('file', None),None
        #     if file is not None:
        #         for fk,fv in file.items():
        #             #allure.attach_file(json.dumps(file),"导入文件")
        #             files={fk:{open(fv, 'rb')}}

        res = self.send.run_main(api_name=api_name, url=url, method=method, headers=headers, cookies=cookie,
                                      file=files, **testcase)
        #print("res的数据：",json.dumps(res.json(),indent=2,ensure_ascii=False))
        if extract is not None:
            self.extract_data(extract,res.text)
        elif extract_list is not None:
            self.extract_data_list(extract_list,res.text)


        #接口断言
        assertions = Assertions()
        #print(res.status_code)
        assertions.assert_result(validation,res.json(),res.status_code)


    def extract_data(self,extract,response):
        """
        提取数据,支持json提取器和正则表达式
        :param extract:yaml文件中的extract
        :param response:接口的实际返回值
        :return:
        """
        for key,value in extract.items():
            # 先把 response 当作 JSON 字符串解析成 Python 对象，再用 jsonpath 库根据 value（如 $.token）提取对应字段的值，并取第一个结果
            if '$' in value:
                # 1. 把响应字符串转成Python字典
                response_dict = json.loads(response)
                len_value = value[2:len(value)]
                extract_data={}
                if response_dict[len_value]:
                    extract_data={key:response_dict[len_value]}
                else:
                    extract_data={key:'未提取到数据'}
                self.read.write_yaml_data(extract_data)
                #print("$",extract_data)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if '$' in value:
                    # 1. 把响应字符串转成Python字典
                    response_dict = json.loads(response)
                    value=str(value)
                    #$.goodsList[*].goodsId
                    clean_value = value[2:]
                    first_value = clean_value.split('[*]')[0]
                    second_value = clean_value.split('[*].')[1]
                    if response_dict[first_value]:
                        extract_data = {key: [response_dict[first_value][i][second_value] for i in range(len(response_dict[first_value]))]}
                    else:
                        extract_data = {key: '未提取到数据'}
                    self.read.write_yaml_data(extract_data)
                    #print("$", extract_data)

        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')



if __name__ == '__main__':
    data = get_yaml('../testcase/Login/login.yaml')[0]
    print(data)
    api = Api()
    #data = api.analyse_data(data)
    api.specification_yaml(data)
    # print("解析之前："+json.dumps( data,ensure_ascii= False))
    # data = api.analyse_data(data)
    # print("解析之后："+json.dumps( data,ensure_ascii= False))



