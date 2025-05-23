import hashlib
import logging
from threading import Thread

from PyQt5.QtWidgets import QApplication

from lib.exlibrary import *
from lib.mainWindow import MainWindow

CONFIG_DATA = None


def init():
    if getattr(sys, 'frozen', False):
        if not os.path.exists(r'.\logs'):
            os.mkdir(r'.\logs')
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s', handlers=[logging.FileHandler(filename=r'.\logs\log.txt', mode='w', encoding='utf-8')])
    else:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')
    upLog(True)
    checkConfig()
    logging.info("等待游戏运行")
    delCache()
    t = Thread(target=ui)
    t.start()


def ui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


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
    for n in uplogs["lines"]:
        r += f"\n{n}"
    logging.info(f'\n版本 {uplogs["version"]}{r if k else ""}\n')


def checkAndSetData(tag):
    if CONFIG_DATA is not None:
        if tag in CONFIG_DATA and CONFIG_DATA[tag]["enable"]:
            writeMemValue(getMemAddress(tag), CONFIG_DATA[tag]["value"], tag)


def has_max(tag, lock_to_max=True):
    if readMemValue(getMemAddress(tag), tag) < CONFIG_DATA[tag]["value"]:
        if readMemValue(getMemAddress(f"MAX_{tag}"), f"MAX_{tag}") < CONFIG_DATA[tag]["value"]:  # 当最大值小于设定值时，修改最大值
            writeMemValue(getMemAddress(f"MAX_{tag}"), CONFIG_DATA[tag]["value"],
                          f"MAX_{tag}")
    if lock_to_max:
        if readMemValue(getMemAddress(f"MAX_{tag}"), f"MAX_{tag}") > readMemValue(
                getMemAddress(tag), tag):  # 当值不满时，修改值至最大
            writeMemValue(getMemAddress(tag),
                          readMemValue(getMemAddress(f"MAX_{tag}"), f"MAX_{tag}"),
                          tag)
    else:
        if readMemValue(getMemAddress(tag), tag) < CONFIG_DATA[tag]["value"]:  # 当值小于设定时修改值
            writeMemValue(getMemAddress(tag), CONFIG_DATA[tag]["value"], tag)


def has_min(tag):
    # 当值小于设定时修改值
    if readMemValue(getMemAddress(tag), tag) < CONFIG_DATA[tag]["value"]:
        writeMemValue(getMemAddress(tag), CONFIG_DATA[tag]["value"], tag)


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


if __name__ == "__main__":
    init()
    add = fmd5 = None
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
                    CONFIG_DATA = readConfig()
                    tips = f"配置修改已生效"
                    writeCache(add, fileHash("./config/config.json", hashlib.md5))

                if stadd is not None and stadd != 0x0:
                    if add != stadd:
                        writeCache(stadd, fileHash("./config/config.json", hashlib.md5))
                        runOnce()
                        logging.info(f"地址段: 0x{getMemAddress():X}")
                        logging.info(f"修改器已启动")
                        tips = ""

                    if tips != "":
                        runOnce()
                        logging.debug(f"地址段: 0x{getMemAddress():X} {tips}")
                        logging.info(tips)
                        tips = ""

                if add is not None and checkRun(EXE_NAME):
                    try:
                        runLoop()
                    except Exception as e:
                        a = e
            else:
                if os.path.exists("./cache"):
                    os.remove("./cache")
                    logging.info("等待游戏运行...")
    except KeyboardInterrupt:
        onClose()
    except Exception as e:
        logging.debug(f"Main.py：{e}")
        a = e
