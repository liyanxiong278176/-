import csv
import os
import xlrd
import xlwt
from xlutils.copy import copy

from common.recordlog import logs
from conf.setting import BASE_DIR


def read_csv_data(file_name):
    try:
        with open(os.path.join(BASE_DIR,'data', file_name), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for e in reader:
                print(e)
    except Exception as e:
        logs.error(e)


class OperateExcel:
    def __init__(self,file_path=None):
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = os.path.join(BASE_DIR,'data','接口消息.xls')

    def xls_obj(self):
        """
        获取excel操作对象
        :return:
        """
        open_workbook = xlrd.open_workbook(self.file_path, formatting_info=True)
        obj = open_workbook.sheets()[0]
        return obj

    def get_cols(self):
        """
        获取列数
        :return:
        """
        return self.xls_obj().ncols

    def get_rows(self):
        """
        获取行数
        :return:
        """
        return self.xls_obj().nrows
    def get_cell_value(self,row,col):
        """
        获取单元格值
        :param row:
        :param col:
        :return:
        """
        return self.xls_obj().cell_value(row,col)

    def get_rows_value(self,row):
        """
        获取行数据
        :param row:
        :return:
        """
        return self.xls_obj().row_values(row)

    def get_cols_value(self,col):
        """
        获取列数据
        :param col:
        :return:
        """
        return self.xls_obj().col_values(col)



if __name__ == '__main__':
   excel = OperateExcel()
   print(excel.get_cols())
   print(excel.get_rows())
   print(excel.get_cell_value(1,1))
   print(excel.get_rows_value(0))
   print(excel.get_cols_value(0))

