import hashlib
import json
import os
import struct
import sys
import time

import psutil

from lib.core import *
from lib.default import *
from lib.nb2data import *

GLOBAL = None
CONFIG_DATA: dict


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
    if not os.path.exists("./config/config.json"):
        writeConfig(default_config)
    if not os.path.exists("./config/ui.cfg"):
        writeConfig(default_ui, _type="ui")


def writeConfig(_jsonObj, _type="config"):
    match _type:
        case "ui":
            pfx = "cfg"
        case _:
            pfx = "json"
    with open(f'./config/{_type}.{pfx}', 'w', encoding="UTF-8") as f:
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


def core_exec(s):
    tips = ""
    try:
        while True:
            if checkRun(EXE_NAME):
                checkConfig()
                stadd = getMemAddress()
                caches = readCache()
                if caches is not None:
                    add = caches["start_address"]
                    fmd5 = caches["config_md5"]
                else:
                    add = fmd5 = None

                if fmd5 != fileHash("./config/config.json", hashlib.md5):
                    global CONFIG_DATA
                    CONFIG_DATA = readConfig()
                    tips = f"配置修改已生效"
                    writeCache(add, fileHash("./config/config.json", hashlib.md5))

                if stadd is not None and stadd != 0x0:
                    if add != stadd:
                        writeCache(stadd, fileHash("./config/config.json", hashlib.md5))
                        runOnce()
                        logging.info(f"地址段: 0x{getMemAddress():X}")
                        logging.info(f"修改器已启动")
                        s.send({"lang_tag":"helper_started"})
                        tips = ""

                    if tips != "":
                        runOnce()
                        logging.debug(f"地址段: 0x{getMemAddress():X} {tips}")
                        logging.info(tips)
                        s.send({"lang_tag":"config_updated", "now_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))})
                        tips = ""

                if add is not None and checkRun(EXE_NAME):
                    try:
                        runLoop()
                    except Exception as e:
                        logging.debug(e)
            else:
                if os.path.exists("./cache"):
                    os.remove("./cache")
                    logging.info("等待游戏运行...")
                    s.send({"lang_tag":"wait_game"})
    except KeyboardInterrupt:
        onClose()
    except Exception as e:
        logging.debug(e)


def onClose():
    logging.info("程序关闭")
    return 0


def writeCache(_stadd, _hash_c=""):
    cx = open(f'./cache', 'wb')
    cx.write(json.dumps(
        {"start_address": _stadd, "config_md5": _hash_c}, ensure_ascii=False).encode("utf-8"))
    cx.close()


def readCache():
    cx = None
    if os.path.exists("./cache"):
        with open(f'./cache', 'r') as file:
            cx = json.loads(file.read())
            file.close()
    return cx


def delCache():
    if os.path.exists("./cache"):
        os.remove("./cache")


def upLog(k):
    r = "\n"
    for n in versionInfo["lines"]:
        r += f"\n{n}"
    logging.info(f'\n版本 {versionInfo["version"]}{r if k else ""}\n')


def checkAndSetData(tag):
    if tag in CONFIG_DATA and CONFIG_DATA[tag]["enable"]:
        writeMemValue(tag, CONFIG_DATA[tag]["value"])


def has_max(tag, lock_to_max=True):
    if readMemValue(tag) < CONFIG_DATA[tag]["value"]:
        if readMemValue(f"MAX_{tag}") < CONFIG_DATA[tag]["value"]:  # 当最大值小于设定值时，修改最大值
            writeMemValue(f"MAX_{tag}", CONFIG_DATA[tag]["value"])
    if lock_to_max:
        if readMemValue(f"MAX_{tag}") > readMemValue(tag):  # 当值不满时，修改值至最大
            writeMemValue(tag, readMemValue(f"MAX_{tag}"))
    else:
        if readMemValue(tag) < CONFIG_DATA[tag]["value"]:  # 当值小于设定时修改值
            writeMemValue(tag, CONFIG_DATA[tag]["value"])


def has_min(tag):
    # 当值小于设定时修改值
    if readMemValue(tag) < CONFIG_DATA[tag]["value"]:
        writeMemValue(tag, CONFIG_DATA[tag]["value"])


def runOnce():
    for key in list(default_config.keys()):
        if "lock" not in default_config[key]:
            # 不允许锁定的项目
            checkAndSetData(key)


def runLoop():
    for key in list(default_config.keys()):
        if "lock" in default_config[key]:  # 允许锁定的项目
            if f"MAX_{key}" in NB2_DATA:  # 有最大值的
                if key in CONFIG_DATA and CONFIG_DATA[key]["enable"] and CONFIG_DATA[key]["lock"]:
                    has_max(key, CONFIG_DATA[key]["lock_to_max"] if "lock_to_max" in CONFIG_DATA[key] else True)
            else:  # 没有最大值的
                if key in CONFIG_DATA and CONFIG_DATA[key]["enable"] and CONFIG_DATA[key]["lock"]:
                    has_min(key)
