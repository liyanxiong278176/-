import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
#把路径添加到环境变量
sys.path.append(BASE_DIR)

LOG_LEVEL = logging.DEBUG#输出到文件
STREAM_LOG_LEVEL = logging.DEBUG#输出到控制台

#文件路径
FILE_PATH={
    "extract":os.path.join(BASE_DIR,"extract.yaml"),
    "conf":os.path.join(BASE_DIR,"conf","conf.ini"),
    "LOG":os.path.join(BASE_DIR,"log")
}
print(FILE_PATH["conf"])

