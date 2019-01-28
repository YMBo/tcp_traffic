# -*- coding:utf8 -*-

import logging

# 创建logger实例
logger = logging.getLogger('traffic_log')
# 输出文件
fh = logging.FileHandler('./traffic_log.log')

# 格式化日志输出
formatter = logging.Formatter(
    "%(levelname)s: %(name)s %(asctime)s processid: %(process)d  funcname: %(funcName)s  lineno:%(lineno)d %(message)s"
)
fh.setFormatter(formatter)
logger.addHandler(fh)
# 设置日志级别
logger.setLevel(logging.DEBUG)