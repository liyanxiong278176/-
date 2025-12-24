import csv
import os

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


if __name__ == '__main__':
    read_csv_data('test.csv')
