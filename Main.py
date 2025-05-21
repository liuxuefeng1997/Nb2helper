import hashlib
import json
import os
import sys
import threading

from PyQt5.QtWidgets import QApplication

from lib.core import *
from lib.default_def import *
from lib.mainWindow import MainWindow

CONFIG_DATA = None


def init():
    if not os.path.exists(r'.\logs'):
        os.mkdir(r'.\logs')
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s', handlers=[logging.FileHandler(filename=r'.\logs\log.txt', mode='w', encoding='utf-8')])
    upLog(True)
    logging.info("等待游戏运行")
    del_cache()
    checkConfig()
    t = threading.Thread(target=ui)
    t.start()


def ui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def onClose():
    logging.info("程序关闭")
    return 0


def checkConfig():
    if not os.path.exists("./config"):
        os.mkdir("./config")
    write_config(default_config, True)
    if not os.path.exists("./config/config.json"):
        write_config(default_config)


def write_cache(_stadd, _hash_c="", _hash_e=""):
    cx = open(f'./cache', 'wb')
    cx.write(json.dumps(
        {"start_address": _stadd, "config_md5": _hash_c, "exp_md5": _hash_e}, ensure_ascii=False).encode("utf-8"))
    cx.close()


def read_cache():
    cx = None
    if os.path.exists("./cache"):
        with open(f'./cache', 'r') as file:
            cx = json.loads(file.read())
            file.close()
    logging.debug(cx)
    return cx


def del_cache():
    if os.path.exists("./cache"):
        os.remove("./cache")


def write_config(_jsonObj, isTemple=False):
    with open(f'./config/config{".temple" if isTemple else ""}.json', 'w', encoding="UTF-8") as f:
        f.write(json.dumps(_jsonObj, ensure_ascii=False))
        f.close()


def read_config():
    cx = None
    if os.path.exists("./config/config.json"):
        with open(f'./config/config.json', 'r', encoding="UTF-8") as f:
            cx = json.loads(f.read())
            f.close()
    return cx


def upLog(k):
    r = "\n"
    for n in uplogs["lines"]:
        r += f"\n{n}"
    logging.info(f'\n版本 {uplogs["version"]}{r if k else ""}\n')


def has_key(_dict, _key):
    return _key in _dict


def file_hash(file_path: str, hash_method) -> str:
    if not os.path.isfile(file_path):
        print('文件不存在。')
        return ''
    h = hash_method()
    with open(file_path, 'rb') as fss:
        while b := fss.read(8192):
            h.update(b)
    return h.hexdigest()


def checkAndSetData(tag):
    if CONFIG_DATA is not None:
        if has_key(CONFIG_DATA, tag) and CONFIG_DATA[tag]["enable"]:
            writeMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), CONFIG_DATA[tag]["value"], NB2_TYPE[tag])


def has_max(tag, lock_to_max=True):
    if readMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), NB2_TYPE[tag]) < CONFIG_DATA[tag]["value"]:
        if readMemValue(getMemAddressWithOffset(NB2_VALUE[f"MAX_{tag}"]), NB2_TYPE[f"MAX_{tag}"]) < CONFIG_DATA[tag]["value"]:  # 当最大值小于设定值时，修改最大值
            writeMemValue(getMemAddressWithOffset(NB2_VALUE[f"MAX_{tag}"]), CONFIG_DATA[tag]["value"],
                          NB2_TYPE[f"MAX_{tag}"])
    if lock_to_max:
        if readMemValue(getMemAddressWithOffset(NB2_VALUE[f"MAX_{tag}"]), NB2_TYPE[f"MAX_{tag}"]) > readMemValue(
                getMemAddressWithOffset(NB2_VALUE[tag]), NB2_TYPE[tag]):  # 当值不满时，修改值至最大
            writeMemValue(getMemAddressWithOffset(NB2_VALUE[tag]),
                          readMemValue(getMemAddressWithOffset(NB2_VALUE[f"MAX_{tag}"]), NB2_TYPE[f"MAX_{tag}"]),
                          NB2_TYPE[tag])
    else:
        if readMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), NB2_TYPE[tag]) < CONFIG_DATA[tag]["value"]:  # 当值小于设定时修改值
            writeMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), CONFIG_DATA[tag]["value"], NB2_TYPE[tag])


def has_min(tag):
    # 当值小于设定时修改值
    if readMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), NB2_TYPE[tag]) < CONFIG_DATA[tag]["value"]:
        writeMemValue(getMemAddressWithOffset(NB2_VALUE[tag]), CONFIG_DATA[tag]["value"], NB2_TYPE[tag])


def runOnce():
    for key in list(default_config.keys()):
        if not has_key(default_config[key], "lock"):
            # 不允许锁定的项目
            checkAndSetData(key)


def runLoop():
    for key in list(default_config.keys()):
        if has_key(default_config[key], "lock"):  # 允许锁定的项目
            if has_key(NB2_VALUE, f"MAX_{key}"):  # 有最大值的
                if has_key(CONFIG_DATA, key) and CONFIG_DATA[key]["enable"] and CONFIG_DATA[key]["lock"]:
                    has_max(key, CONFIG_DATA[key]["lock_to_max"] if has_key(CONFIG_DATA[key], "lock_to_max") else True)
            else:  # 没有最大值的
                if has_key(CONFIG_DATA, key) and CONFIG_DATA[key]["enable"] and CONFIG_DATA[key]["lock"]:
                    has_min(key)


if __name__ == "__main__":
    init()
    add = fmd5 = None
    tips = ""
    try:
        while True:
            if check_process_running(EXE_NAME):
                checkConfig()

                stadd = getMemAddressWithOffset()
                caches = read_cache()
                if caches is not None:
                    add = caches["start_address"]
                    fmd5 = caches["config_md5"]
                else:
                    add = fmd5 = None

                if fmd5 != file_hash("./config/config.json", hashlib.md5):
                    CONFIG_DATA = read_config()
                    tips = f"配置修改已生效"
                    write_cache(add, file_hash("./config/config.json", hashlib.md5))

                if stadd is not None and stadd != 0x0 and len("0x29B14CCA000") == len(f"0x{stadd:X}"):
                    if add != stadd:
                        write_cache(stadd, file_hash("./config/config.json", hashlib.md5))
                        runOnce()
                        # print("\033c", end="")
                        # upLog(False)
                        logging.info(f"地址段: 0x{getMemAddressWithOffset():X}")
                        logging.info(f"修改器已启动")
                        tips = ""

                    if tips != "":
                        runOnce()
                        # print("\033c", end="")
                        # upLog(False)
                        logging.debug(f"地址段: 0x{getMemAddressWithOffset(): X} {tips}")
                        logging.info(tips)
                        tips = ""

                if add is not None and check_process_running(EXE_NAME):
                    try:
                        runLoop()
                    except Exception as e:
                        a = e
            else:
                if os.path.exists("./cache"):
                    os.remove("./cache")
                    # print("\033c", end="")
                    # upLog(False)
                    logging.info("等待游戏运行...")
    except KeyboardInterrupt:
        onClose()
    except Exception as e:
        logging.debug(e)
