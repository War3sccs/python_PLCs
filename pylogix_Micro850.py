# ！python3
# -*- coding: UTF-8 -*-

import logging  # 导入日志模块
import time  # import timer
from logging.handlers import RotatingFileHandler  # 导入日志模块
from pylogix import PLC

# TODO:1.全局变量/公用函数/初始化
# TODO:1.1 开启logging
logger_paddle = logging.getLogger('logging_paddle')

# TODO:1.1.1日志格式
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# TODO:1.1.2 日志纪录的目的地
# 定义日志信息发送的目的地，可以是控制台，也可以是文件，也可以多个
logger_handler = logging.StreamHandler()  # log在控制台显示
logger_handler.setFormatter(log_format)
logger_paddle.addHandler(logger_handler)

file_handler = RotatingFileHandler('operationg_log.txt', maxBytes=30*1024*1024, backupCount=5)  # log写入文件
file_handler.setFormatter(log_format)
logger_paddle.addHandler(file_handler)

# TODO:1.1.3 记录的等级
# logger_paddle.setLevel(logging.DEBUG)
logger_paddle.setLevel(logging.INFO)
# logger_paddle.setLevel(logging.WARNING)

# 读开关量
alarm_value = None
alarm_status = None

with PLC('192.168.9.87', Micro800=True) as comm:
    ret = comm.Read('silo_weight_low_alarm')
    alarm_value = ret.Value
    alarm_status = ret.Status

print(f"标签名: silo_weight_low_alarm")
print(f"数值: {alarm_value}")
print(f"状态: {alarm_status}")

#写开关量

# with 外部：写入的数值和接收的状态
write_value = True
write_status = None

with PLC('192.168.9.87', Micro800=True) as comm:
    ret = comm.Write('equipment_local_actuation[19]', write_value)
    write_status = ret.Status

print(f"写入数值: {write_value}")
print(f"写入状态: {write_status}")

#读浮点量

# with 外部：接收数值和状态
setting_value = None
setting_status = None

with PLC('192.168.9.87', Micro800=True) as comm:
    ret = comm.Read('air_compressor_pressure_low_setting')
    setting_value = ret.Value
    setting_status = ret.Status

print(f"标签名: air_compressor_pressure_low_setting")
print(f"数值: {setting_value}")
print(f"状态: {setting_status}")

#写浮点量
# with 外部：写入的数值和接收的状态
write_value = 0.45
write_status = None

with PLC('192.168.9.87', Micro800=True) as comm:
    ret = comm.Write('air_compressor_pressure_low_setting', write_value)
    write_status = ret.Status

print(f"写入数值: {write_value}")
print(f"写入状态: {write_status}")

#if __name__ == "__main__":

    #读开关量

    #写开关量

    #读浮点量

    #写浮点量

    #读word量

    #写word量
