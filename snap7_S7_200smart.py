# ！python3
# -*- coding: UTF-8 -*-

import logging  # 导入日志模块
import time  # import timer
from logging.handlers import RotatingFileHandler  # 导入日志模块
import snap7  
from snap7 import util

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

# TODO：2.建立连接
def PLC_connect(IP_address):
    plc = snap7.client.Client()
    plc.set_connection_type(3)  # S7-200 SMART 必须设置此项 [citation:4][citation:10]
    plc.connect(IP_address, 0, 1)  # IP, 机架0, 槽1
    return plc

# TODO：3.读开关量
def read_bit(IP_address,offset,bytes_read,byte_index,bit_index):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 读取 V0.0（DB1, 偏移0, 1个字节byte）
    data = plc.db_read(1, offset, bytes_read)  # 读1字节就够，因为开关量只占1位

# 3. 解析出位状态（byte_index=0, bit_index=0）
    value = util.get_bool(data, byte_index, bit_index)
    #print(f"V0.0 状态: {value}")  # 输出 True 或 False

    logger_paddle.info(value)
    plc.disconnect()
    return value

# TODO：4.写开关量
def write_bit(IP_address,offset,bytes_write,byte_index,bit_index,write_value):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 读取 V0.0（DB1, 偏移0, 1个字节byte）
    data = plc.db_read(1, offset, bytes_write)  # 读1字节就够，因为开关量只占1位

# 3. 解析出位状态（byte_index=0, bit_index=0）
    util.set_bool(data, byte_index, bit_index, write_value)
    #util.set_bool(data, byte_index, bit_index, True)
    #print(f"V0.0 状态: {value}")  # 输出 True 或 False

# 4. 把修改后的整个字节写回去
    plc.db_write(bytes_write, offset, data)

    logger_paddle.info(data)
    plc.disconnect()
    return data

# TODO：5.读浮点量
def read_real(IP_address,offset,bytes_read,byte_index):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 读取 V0.0（DB1, 偏移0, 4个字节byte）
    data = plc.db_read(1, offset, bytes_read)  # 读4字节，浮点量4个字节

# 3. 解析出位状态（byte_index=0, bit_index=0）
    value = util.get_real(data, byte_index)
    #print(f"V0.0 状态: {value}")  # 输出 True 或 False

    logger_paddle.info(value)
    plc.disconnect()
    return value

# TODO：6.写浮点量
def write_real(IP_address,offset,byte_index,write_value):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 创建一个 4 字节的缓冲区
    data = bytearray(4)
# 3. 把浮点数写入缓冲区（byte_index=0）
    util.set_real(data, byte_index, write_value)

# 4. 把修改后的整个字节写回去
    plc.db_write(1, offset, data)

    logger_paddle.info(data)
    plc.disconnect()
    return data


# TODO：7.读word量
def read_word(IP_address,offset,bytes_read,byte_index):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 读取 V0.0（DB1, 偏移0, 1个字节byte）
    data = plc.db_read(1, offset, bytes_read)  # 读2字节，word变量2字节

# 3. 解析出位状态（byte_index=0, bit_index=0）
    value = util.get_word(data, byte_index)
    #print(f"V0.0 状态: {value}")  # 输出 True 或 False

    logger_paddle.info(value)
    plc.disconnect()
    return value

# TODO：8.写word量
def write_word(IP_address,offset,byte_index,write_value):
# 1. 建立连接
    plc=PLC_connect(IP_address)

# 2. 创建一个 2 字节的缓冲区
    data = bytearray(2)
# 3. 把word数写入缓冲区（byte_index=0）
    util.set_word(data, byte_index, write_value)

# 4. 把修改后的整个字节写回去
    plc.db_write(1, offset, data)

    logger_paddle.info(data)
    plc.disconnect()
    return data


if __name__ == "__main__":
    IP_address = '192.168.1.150'
    #读开关量
    offset = 0
    bytes_read = 1
    byte_index = 0
    bit_index = 0
    boo_read = read_bit(IP_address,offset,bytes_read, byte_index, bit_index)
    #写开关量
    write_value = True
    #write_value = False
    offset = 6
    byte_index = 0
    bit_index = 2
    bool_write = write_bit(IP_address,offset,bytes_read, byte_index, bit_index,write_value)
    #读浮点量
    offset = 416
    bytes_read = 4 #浮点量要4bytes
    byte_index = 0
    real_read = read_real(IP_address,offset,bytes_read, byte_index)
    #写浮点量
    offset = 416
    byte_index = 0
    write_value = 4.58
    real_write = write_real(IP_address, offset, byte_index, write_value)
    #读word量
    offset = 500
    bytes_read = 2 #word量要2bytes
    byte_index = 0
    word_read = read_word(IP_address,offset,bytes_read, byte_index)
    #写word量
    offset = 500
    byte_index = 0
    write_value = 458
    word_write = write_word(IP_address, offset, byte_index, write_value)
