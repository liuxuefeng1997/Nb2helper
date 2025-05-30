from PyQt6.QtWidgets import QApplication

from lib.exlibrary import *
from lib.mainWindow import MainWindow


def init():
    NOW_TIME_WITH_NO_SPACE = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    if getattr(sys, 'frozen', False):
        if not os.path.exists(r'.\logs'):
            os.mkdir(r'.\logs')
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s', handlers=[logging.FileHandler(filename=rf'.\logs\log_{NOW_TIME_WITH_NO_SPACE}.txt', mode='w', encoding='utf-8')])
    else:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')
    upLog(True)
    checkConfig()
    delCache()


def ui():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    init()
    ui()
