import json
import os
import struct
import sys

import psutil

from lib.core import *
from lib.default import *
from lib.nb2data import *

GLOBAL = None


def fileHash(file_path: str, hash_method) -> str:
    if not os.path.isfile(file_path):
        print('文件不存在。')
        return ''
    h = hash_method()
    with open(file_path, 'rb') as fss:
        while b := fss.read(8192):
            h.update(b)
    return h.hexdigest()


def checkConfig():
    if not os.path.exists("./config"):
        os.mkdir("./config")
    writeConfig(default_config, isTemple=True)
    if not os.path.exists("./config/config.json"):
        writeConfig(default_config)
    if not os.path.exists("./config/ui.cfg"):
        writeConfig(default_ui, _type="ui")


def writeConfig(_jsonObj, _type="config", isTemple=False):
    match _type:
        case "ui":
            pfx = "cfg"
        case _:
            pfx = "json"
    with open(f'./config/{_type}{".temple" if isTemple else ""}.{pfx}', 'w', encoding="UTF-8") as f:
        f.write(json.dumps(_jsonObj, ensure_ascii=False))
        f.close()


def readConfig():
    cx = None
    if os.path.exists("./config/config.json"):
        with open(f'./config/config.json', 'r', encoding="UTF-8") as f:
            cx = json.loads(f.read())
            f.close()
    return cx


def readUIConfig():
    cx = None
    if os.path.exists("./config/ui.cfg"):
        with open(f'./config/ui.cfg', 'r', encoding="UTF-8") as f:
            cx = json.loads(f.read())
            f.close()
    return cx


def getPID(process_name):
    pid = None
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            pid = proc.info['pid']
            break
    return pid


def getMemAddress(tag=None):
    if tag is None:
        tag = "_DEFAULT_"
    memInfo = NB2_DATA[tag]
    if "offsets" in memInfo:
        offsets = memInfo["offsets"]
    else:
        return None

    # 目标进程ID
    pid = getPID(EXE_NAME)
    if pid is None:
        logging.error("游戏未运行")
        return None
    try:
        start_address = getBaseOffset(memInfo["dll_name"], memInfo["dll_offset"])  # 计算初始地址
        final_address = read_pointer_chain(pid, start_address, offsets)  # 解析指针链
        return final_address
    except Exception as e:
        logging.debug(e)
        return None


def checkRun(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False


def writeMemValue(tag, value):
    memInfo = NB2_DATA[tag]
    address = getMemAddress(tag)
    logging.debug(memInfo)
    if "valueType" in memInfo:
        _type = memInfo["valueType"]
    else:
        return None
    pid = getPID(EXE_NAME)
    data = struct.pack(f'<{_type}', value)
    return write_memory(pid, address, data)


def readMemValue(tag):
    memInfo = NB2_DATA[tag]
    address = getMemAddress(tag)
    if "valueType" in memInfo:
        _type = memInfo["valueType"]
    else:
        return None
    match _type:
        case "d":
            size = 8
        case "f":
            size = 4
        case "b":
            size = 1
        case "2b":
            size = 2
        case "4b":
            size = 4
        case "8b":
            size = 8
        case _:
            logging.error("Mem type error")
            return None
    pid = getPID(EXE_NAME)
    data = read_memory(pid, address, size)
    return struct.unpack(f'<{_type}', data)[0]


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = "./"
    ret_path = os.path.join(base_path, relative_path)
    return ret_path


def getBaseOffset(dll_name, dll_offset):
    return get_module_base(getPID(EXE_NAME), dll_name) + dll_offset
