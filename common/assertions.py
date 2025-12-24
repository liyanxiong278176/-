import operator

from common.connectdb import ConnectMysql
from common.readyaml import get_yaml
from common.recordlog import logs
from conf.operateconf import OperateConf
from conf.setting import FILE_PATH


class Assertions:
    def find_values_by_key(self,data, target_key):
        """
        递归查找 JSON 中所有指定 key 的 value
        :param data: dict / list / 其他类型
        :param target_key: 要查找的键名（如 'name'）
        :return: 包含所有匹配值的列表
        """
        results = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    results.append(value)
                # 递归子元素
                results.extend(self.find_values_by_key(value, target_key))
        elif isinstance(data, list):
            for item in data:
                results.extend(self.find_values_by_key(item, target_key))


        return results
    def contains_assert(self,value,response,status_code):
        """
        :param value: yaml文件的validation关键字下的结果
        :param response: 实际返回到结果json
        :param status_code: 状态码
        :return:
        """
        flag=0
        #遍历断言字典 value 中的所有键值对
        for assert_key,assert_value in value.items():
            #print(assert_key,assert_value)
            if assert_key=='status_code':
                if assert_value !=status_code:
                    flag+=1
                    logs.error('containing断言失败：接口返回码【%s】不等于【%s】' % (status_code, assert_value))
                else:
                    logs.info('containing断言成功：接口返回码【%s】等于【%s】' % (status_code, assert_value))
            else:
                #从 response 这个 JSON 数据中，递归查找所有名为 assert_key 的字段，并把它们的值组成一个列表返回。
                res_list = self.find_values_by_key(response, assert_key)
                if isinstance(res_list[0],str):
                    res_list=''.join(res_list)
                if res_list:
                    if assert_value in res_list:
                        logs.info(f"包含断言成功,实际结果为{res_list}，预期结果为{assert_value}")
                    else:
                        logs.error(f"包含断言失败,实际结果为{res_list}，预期结果为{assert_value}")
                        flag+=1
                else:
                    print("没有找到字段")
                    flag+=1
        return flag

    def equal_assert(self,value,response):
        """
        :param value: yaml文件的validation关键字下的结果,dict
        :param response: 响应结果dict
        :return:
        """
        flag=0
        res_list=[]

        if isinstance(value,dict) and isinstance(response,dict):
            for res in response:
                if list(value.keys())[0] != res:
                    res_list.append(res)
            for res in res_list:
                del response[res]
            eq = operator.eq(value, response)
            if eq:
                print("断言成功")
                logs.info(f"equal断言成功,接口实际结果为{response},预期结果{value}")
            else:
                print("断言失败")
                logs.error(f"equal断言失败,接口实际结果为{response},预期结果{value}")
                flag+=1
        else:
            raise TypeError("value和response类型不一致,必须为dict类型")
        return flag

    def mysql_assert(self,sql):
        """
        断言新增之后，查询数据库是否有，有说明新增成功，断言成功
        :param sql: mysql查询语句
        :return:
        """
        flag=0
        conn = ConnectMysql()
        query = conn.query(sql)
        if query is not None:
            #print(query)
            logs.info(f"mysql断言成功,数据库查询结果为{query}")
        else:
            flag+=1
            #print("数据库查询结果为空")
            logs.error("mysql断言失败,数据库查询结果为空")
        return  flag

    def assert_result(self,expect,response,status_code):
        """
        选取不同的断言方式
        :param expect: yaml文件的validation关键字下的结果
        :param response: 响应结果
        :param status_code: 状态码
        :return:
        """
        all_flag=0
        flag=0
        try:
            for i in expect:
                for key, value in i.items():
                    if key=='contains':
                        flag = self.contains_assert(value, response, status_code)
                    elif key=='eq':
                        flag = self.equal_assert(value, response)
                    elif key=='mysql':
                        flag = self.mysql_assert(value)
                    all_flag += flag
        except Exception as e:
            logs.error("测试失败")
            logs.error("测试失败原因：%s" % e)
            raise e

        if all_flag==0:
            logs.info("测试通过")
            assert True
        else:
            logs.error("测试失败")
            assert False


if __name__ == '__main__':
    value = get_yaml('../testcase/Login/login.yaml')[0]

    validation = value['testCase'][0]['validation']

    response={
        "error_code":None,
        "msg":"登录成功",
        "msg_code":200,
        "token":"4f426FED3F1aEEF10FFbff7bbC926"
    }
    assertions = Assertions()
    for i in validation:
        for key,value in i.items():
            assertions.equal_assert(value,response)
