from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from lib.exlibrary import *
from lib.language import *
from lib.nb2data import *


class Thread(QThread):
    data_sent = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        core_exec(self)

    def send(self, data):
        self.data_sent.emit(data)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("初始化窗口中")
        self.config = readConfig("ui")
        currSetLang = self.config["language"] if self.config and "language" in self.config else "zh-cn"
        self.lang = language[currSetLang]
        self.Icon = QIcon(resource_path(os.path.join("resources/", "icon.ico")))
        # 设置窗口标题和大小
        self.setWindowTitle(f'{self.lang["title"]}')
        self.setWindowIcon(self.Icon)
        self.resize(288, 223)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height())
        # 初始化托盘图标
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.Icon)
        # 语言菜单
        self.langMenu = QMenu(self)
        self.langMenu.setTitle(self.lang["language"])
        self.langCNAction = QAction(self)
        self.langCNAction.setText("简体中文")
        self.langCNAction.triggered.connect(self.activeLangCN)
        self.langENAction = QAction(self)
        self.langENAction.setText("English")
        self.langENAction.triggered.connect(self.activeLangEN)
        self.langMenu.addAction(self.langCNAction)
        self.langMenu.addAction(self.langENAction)
        match currSetLang:
            case "zh-cn":
                self.langCNAction.setChecked(True)
                self.langENAction.setChecked(False)
            case "en-us":
                self.langCNAction.setChecked(False)
                self.langENAction.setChecked(True)
        # 托盘右键菜单
        self.trayMenu = QMenu(self)

        self.showAction = QAction(self)
        self.showAction.setText(self.lang["hide"])
        self.showAction.triggered.connect(self.showEx)
        self.trayMenu.addAction(self.showAction)

        self.trayMenu.addSeparator()
        self.trayMenu.addMenu(self.langMenu)

        self.aboutAction = QAction(self)
        self.aboutAction.setText(self.lang["about"])
        self.aboutAction.triggered.connect(self.buttonAbout_onClick)
        self.trayMenu.addAction(self.aboutAction)

        self.trayMenu.addSeparator()

        self.quitAction = QAction(self)
        self.quitAction.setText(self.lang["quit"])
        self.quitAction.triggered.connect(self.closeEvent)
        self.trayMenu.addAction(self.quitAction)

        self.tray.setContextMenu(self.trayMenu)
        self.tray.activated.connect(self.tray_isClicked)
        self.tray.show()
        # 初始化配置
        self.curr_cfg = readConfig()
        self.def_cfg = default_config
        # 初始化列表
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, 0, 100, 200)
        self.listWidget.setStyleSheet("QListWidget::item { height: 20px; font-size: 11px; text-overflow: clip; }")
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidget.clicked.connect(self.listWidget_onClicked)
        # 初始化列表数据
        for key in self.def_cfg.keys():
            if "offsets" in NB2_DATA[key]:
                item = QListWidgetItem()
                item.setText(self.lang[key])
                item.setStatusTip(f'{key}')
                self.listWidget.addItem(item)
        # 初始化启用选择框
        self.checkBoxEnable = QCheckBox(self.lang["enable"], self)
        self.checkBoxEnable.setGeometry(130, 10, 85, 20)
        self.checkBoxEnable.setCheckable(True)
        self.checkBoxEnable.setVisible(False)
        self.checkBoxEnable.clicked.connect(self.checkBoxEnable_onClicked)
        # 初始化锁定选择框
        self.checkBoxLock = QCheckBox(self.lang["lock"], self)
        self.checkBoxLock.setGeometry(130, 40, 85, 20)
        self.checkBoxLock.setCheckable(True)
        self.checkBoxLock.setVisible(False)
        self.checkBoxLock.clicked.connect(self.checkBoxLock_onClicked)
        # 初始化标签
        self.label = QLabel(self)
        self.label.setGeometry(130, 170, 40, 20)
        self.label.setText(self.lang["value"])
        self.label.setVisible(False)
        # 初始化整数数值输入框
        self.SpinBox = QSpinBox(self)
        self.SpinBox.setGeometry(170, 169, 70, 22)
        self.SpinBox.setMaximum(999)
        self.SpinBox.setMinimum(0)
        self.SpinBox.setVisible(False)
        self.SpinBox.editingFinished.connect(self.SpinBox_onChange)
        # 初始化浮点数值输入框
        self.doubleSpinBox = QDoubleSpinBox(self)
        self.doubleSpinBox.setGeometry(self.SpinBox.geometry())
        self.doubleSpinBox.setMaximum(1.00)
        self.doubleSpinBox.setMinimum(0.00)
        self.doubleSpinBox.setVisible(False)
        self.doubleSpinBox.editingFinished.connect(self.doubleSpinBox_onChange)
        # 初始化锁定最大选择框
        self.checkBoxLockMax = QCheckBox(self.lang["lockMax"], self)
        self.checkBoxLockMax.setGeometry(130, 70, 85, 20)
        self.checkBoxLockMax.setCheckable(True)
        self.checkBoxLockMax.setVisible(False)
        self.checkBoxLockMax.clicked.connect(self.checkBoxLockMax_onClicked)
        # 初始化开启选择框
        self.checkBoxOpen = QCheckBox(self.lang["open"], self)
        self.checkBoxOpen.setGeometry(130, 170, 85, 20)
        self.checkBoxOpen.setCheckable(True)
        self.checkBoxOpen.setVisible(False)
        self.checkBoxOpen.clicked.connect(self.checkBoxOpen_onClicked)
        # 初始化状态栏
        self.statusBar = QStatusBar(self)
        self.statusBar.setGeometry(0, 201, 288, 22)
        self.statusBar.setSizeGripEnabled(False)

        logging.info("窗口初始化结束")
        # 加载数据
        self.listWidget.setCurrentRow(0)
        self.checkVisit(self.listWidget.currentItem().statusTip())
        self.c_key = self.listWidget.currentItem().statusTip()
        # 启动核心线程
        self.t = Thread()
        self.t.data_sent.connect(self.callback)
        self.t.start()

    def callback(self, data):
        lang_tag = data["lang_tag"]
        ti = f' [{data["now_time"]}]' if "now_time" in data else ""
        self.statusBar.showMessage(f'{self.lang[lang_tag]}{ti}', 5000)

    def tray_isClicked(self, reason):
        logging.debug(f'tray-icon: {reason} {type(reason)}')
        match f'{reason}':
            case "ActivationReason.DoubleClick":
                self.showEx()

    def activeLangCN(self):
        self.config["language"] = "zh-cn"
        writeConfig(self.config, "ui")
        self.langCNAction.setChecked(True)
        self.langENAction.setChecked(False)
        self.statusBar.showMessage(f'{self.lang["next_start_active_lang"]}', 5000)

    def activeLangEN(self):
        self.config["language"] = "en-us"
        writeConfig(self.config, "ui")
        self.langCNAction.setChecked(False)
        self.langENAction.setChecked(True)
        self.statusBar.showMessage(f'{self.lang["next_start_active_lang"]}', 5000)

    def buttonAbout_onClick(self):
        self.statusBar.showMessage(f'{self.lang["version"]}v{versionInfo["version"]}', 5000)

    def showEx(self):
        if self.isHidden():
            self.showAction.setText(self.lang["hide"])
            self.show()
        else:
            self.showAction.setText(self.lang["show"])
            self.hide()

    def closeEvent(self, e):
        logging.info("窗口关闭")
        self.t.exit(0)
        self.tray = None
        self.saveGeometry()
        sys.exit(0)

    def checkVisit(self, current_key=None):
        self.checkBoxEnable.setVisible(False)
        self.checkBoxLock.setVisible(False)
        self.checkBoxLockMax.setVisible(False)
        self.label.setVisible(False)
        self.SpinBox.setVisible(False)
        self.doubleSpinBox.setVisible(False)
        self.checkBoxOpen.setVisible(False)
        if current_key is not None:
            enable = False
            if current_key in self.curr_cfg:
                enable = self.curr_cfg[current_key]["enable"]
            self.checkBoxEnable.setVisible(True)
            self.checkBoxEnable.setChecked(True) if enable else self.checkBoxEnable.setChecked(False)
        if self.checkBoxEnable.isChecked():
            if "lock" in self.def_cfg[current_key]:
                if "lock" not in self.curr_cfg[current_key]:
                    self.curr_cfg[current_key].update({"lock":False})
                    writeConfig(self.curr_cfg)
                self.checkBoxLock.setChecked(self.curr_cfg[current_key]["lock"])
                self.checkBoxLock.setVisible(True)
            if "lock_to_max" in self.def_cfg[current_key] and self.checkBoxLock.isChecked():
                if "lock_to_max" not in self.curr_cfg[current_key]:
                    self.curr_cfg[current_key].update({"lock_to_max":False})
                    writeConfig(self.curr_cfg)
                self.checkBoxLockMax.setChecked(self.curr_cfg[current_key]["lock_to_max"])
                self.checkBoxLockMax.setVisible(True)
            if "valueType" in NB2_DATA[current_key]:
                match NB2_DATA[current_key]["valueType"]:
                    case "d":
                        self.label.setVisible(True)
                        self.SpinBox.setVisible(True)
                        self.SpinBox.setValue(self.curr_cfg[current_key]["value"])
                    case "f":
                        self.label.setVisible(True)
                        self.doubleSpinBox.setVisible(True)
                        self.doubleSpinBox.setValue(self.curr_cfg[current_key]["value"])
                    case "b":
                        value = self.curr_cfg[current_key]["value"]
                        self.checkBoxOpen.setVisible(True)
                        self.checkBoxOpen.setChecked(True) if value == 1 else self.checkBoxOpen.setChecked(False)

    def checkBoxEnable_onClicked(self):
        self.curr_cfg[self.c_key]["enable"] = self.checkBoxEnable.isChecked()
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def checkBoxLock_onClicked(self):
        self.curr_cfg[self.c_key]["lock"] = self.checkBoxLock.isChecked()
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def SpinBox_onChange(self):
        self.curr_cfg[self.c_key]["value"] = self.SpinBox.value()
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def doubleSpinBox_onChange(self):
        self.curr_cfg[self.c_key]["value"] = self.doubleSpinBox.value()
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def checkBoxLockMax_onClicked(self):
        self.curr_cfg[self.c_key]["lock_to_max"] = self.checkBoxLockMax.isChecked()
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def checkBoxOpen_onClicked(self):
        self.curr_cfg[self.c_key]["value"] = 1 if self.checkBoxOpen.isChecked() else 0
        self.checkVisit(self.c_key)
        writeConfig(self.curr_cfg)

    def listWidget_onClicked(self):
        item = self.listWidget.currentItem()
        current_text = f'{item.text()}'
        current_key = f'{item.statusTip()}'
        logging.debug(f'{current_text}：{current_key}')
        if getMemAddress(current_key) is not None:
            self.statusBar.showMessage(f'{current_text}: {readMemValue(current_key)}', 5000)
        self.c_key = current_key
        if current_key not in self.curr_cfg:
            logging.info(f"{current_text} {current_key}: 配置项不存在，写入默认配置")
            l_dict = {f'{current_key}' :self.def_cfg[current_key]}
            self.curr_cfg.update(l_dict)
            writeConfig(self.curr_cfg)
        logging.info(f"{current_text} {current_key}: {self.curr_cfg[current_key]}")
        self.checkVisit(current_key)
