import json
import os

import yaml

from conf import setting
from conf.operateconf import OperateConf
from conf.setting import FILE_PATH


def get_yaml(file):
    #把yaml文件的baseInfo和testcase的数据拆分组合
    #方便allure测试报告展示一个yaml文件对应多个用例
    testcase_list=[]
    try:
        with open(file,'r',encoding='utf-8') as f:
            load = yaml.safe_load(f)
            if len(load)<=1:
                yaml_data= load[0]
                base_info = yaml_data['baseInfo']
                for testCase in yaml_data['testCase']:
                    params=[base_info,testCase]
                    testcase_list.append(params)
                return testcase_list
            else:
                return load

    except Exception as e:
        print(e)


class ReadAndWriteYaml:
    def __init__(self,yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../testcase/Login/login.yaml'

    def write_yaml_data(self,value):
        """
        :param data:将要写入的数据（dict）
        :return:
        """
        file= setting.FILE_PATH['extract']
        if not os.path.exists(file):
            pass

        try:
            with open(file,'a',encoding='utf-8') as f:
                if isinstance(value,dict):
                    #把data转为yaml格式并可以写中文，保持字典data中键的原始顺序，不进行自动的字母排序
                    write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                    #print("write_data:"+write_data)
                    f.write(write_data)
                    #yaml文件要有下面的格式才能写入
                    # extract:
                    # token: $.token
        except Exception as e:
            print(e)

    # 获取yaml文件所有value数据
    def get_extract_yaml_data(self, key,second_key=None):
        """
        :param key: 键
        :return:
        """
        file_path=FILE_PATH['extract']
        if os.path.exists(file_path):
            pass
        else:
            print("文件不存在")
            with open(file_path, 'w', encoding='utf-8') as f:
               pass
            print("文件创建成功")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if second_key is not None:
                return data[key][second_key]
            return data[key]

    def clear_extract_yaml_data(self):
        """
        清空extract.yaml文件
        :return:
        """
        with open(FILE_PATH['extract'], 'w', encoding='utf-8') as f:
            f.truncate()

if __name__ == '__main__':
    # 获取yaml文件数组的第一个元素
    get_yaml('../testcase/Login/login.yaml')
    #<class 'dict'>获得之后的数据类型是字典
    # print(res)
    # #获取yaml文件数组的元素
    # info = res['baseInfo']
    # url = info['url']
    # operate_conf = OperateConf()
    # new_url=operate_conf.get_envi('host')+url
    # print(new_url)
    # method = info['method']
    # data = res['testCase'][0]['data']
    # # 发送请求
    # from send_request import SendRequest
    # send_request = SendRequest()
    # passage = send_request.run_main(method=method, url=new_url, data=data, header=None)
    # print(passage['token'])
    # #写入yaml文件
    # write_data={'token':passage['token']}
    # ReadAndWriteYaml().write_yaml_data(write_data)
    #
    #
    #
    # #json序列化：把python对象（字典）转换成json对象
    # json_dumps= json.dumps(res)
    # print(type(json_dumps))
    # #json反序列化：把json对象转换成python对象（字典）
    # json_loads= json.loads(json_dumps)
    # print(type(json_loads))
    #
    # print(ReadAndWriteYaml().get_extract_yaml_data('token'))



