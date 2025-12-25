import csv
import os
import random
import time

from common.readyaml import ReadAndWriteYaml
from common.recordlog import logs
from conf.setting import BASE_DIR


class DebugTalk:
    def __init__(self):
        self.read=ReadAndWriteYaml()

    def get_extract_yaml_data_order(self, data,key):
        if key is not [0,-1]:
            return data[key-1]

    # 获取yaml文件value数据
    def get_extract_yaml_data(self, key,randoms=None,second_key=None):
        """
        获取yaml文件的数据
        :param key:yaml文件的key
        :return:
        """
        data = self.read.get_extract_yaml_data(key,second_key)
        if randoms is not None:
            num_random=int(randoms)
            data_dict={
                num_random:self.get_extract_yaml_data_order(data,num_random),
                0:random.choice(data),#随机数
                -1:'.'.join(data),
                -2:'.'.join(data).split('.')
            }
            data=data_dict[num_random]
        return data

    def md5(self, data):
        return "666"+data

    def read_csv_data(file_name):
        try:
            with open(os.path.join(BASE_DIR, 'data', file_name), 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for e in reader:
                    print(e)
                return reader
        except Exception as e:
            logs.error(e)

    def get_now(self):
        """
        获取当前时间
        :return:
        """
        return time.strftime("%Y-%m-%d", time.localtime())

    def get_timestamp(self):
        """
        获取时间戳
        :return:
        """
        return int(time.time())




if __name__ == '__main__':
    # print(DebugTalk().get_extract_yaml_data('id',"-2"))
    print(DebugTalk().get_now())
