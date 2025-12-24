import configparser

from conf import setting


class OperateConf:
    """
    操作ini配置文件
    """
    def __init__(self, conf_file= None):
        if conf_file is None:
            self.conf_file = setting.FILE_PATH['conf']
        else:
            self.conf_file = conf_file

        #读文件
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.conf_file, encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self, section,option):
        try:
            return self.conf.get(section, option)
        except Exception as e:
            print(e)

    def get_envi(self,option):
        return self.get_section_for_data('api_envi', option)

    def get_mysql(self,option):
        return self.get_section_for_data('MYSQL', option)

    def get_redis(self,option):
        return self.get_section_for_data('REDIS', option)


if __name__ == '__main__':
    operate_conf = OperateConf()
    print(operate_conf.get_envi('host'))
