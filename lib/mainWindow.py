# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from lib.exlibrary import *
from lib.language import *
from lib.nb2data import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("初始化窗口中")
        self.config = readUIConfig()
        self.lang = language[self.config["language"]] if "language" in self.config and self.config else language["zh-cn"]
        # 设置窗口标题和大小
        self.setWindowTitle(f'{self.lang["title"]} v{versionInfo["version"]}')
        self.setWindowIcon(QIcon(resource_path(os.path.join("resources/", "icon.ico"))))
        self.resize(358, 223)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height())

        self.curr_cfg = readConfig()
        self.def_cfg = default_config

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, 0, 171, 200)
        self.listWidget.setStyleSheet("QListWidget::item { height: 20px; font-size: 11px; text-overflow: clip; }")
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for key in self.def_cfg.keys():
            if "offsets" in NB2_DATA[key]:
                item = QListWidgetItem()
                item.setText(self.lang[key])
                item.setStatusTip(f'{key}')
                self.listWidget.addItem(item)

        self.listWidget.clicked.connect(self.listWidget_onClicked)

        self.checkBoxEnable = QCheckBox(self.lang["enable"], self)
        self.checkBoxEnable.setGeometry(200, 10, 85, 20)
        self.checkBoxEnable.setCheckable(True)
        self.checkBoxEnable.setVisible(False)
        self.checkBoxEnable.clicked.connect(self.checkBoxEnable_onClicked)

        self.checkBoxLock = QCheckBox(self.lang["lock"], self)
        self.checkBoxLock.setGeometry(200, 40, 85, 20)
        self.checkBoxLock.setCheckable(True)
        self.checkBoxLock.setVisible(False)
        self.checkBoxLock.clicked.connect(self.checkBoxLock_onClicked)

        self.label = QLabel(self)
        self.label.setGeometry(200, 170, 40, 20)
        self.label.setText(self.lang["value"])
        self.label.setVisible(False)

        self.SpinBox = QSpinBox(self)
        self.SpinBox.setGeometry(240, 169, 62, 22)
        self.SpinBox.setMaximum(999)
        self.SpinBox.setMinimum(0)
        self.SpinBox.setVisible(False)
        self.SpinBox.editingFinished.connect(self.SpinBox_onChange)

        self.doubleSpinBox = QDoubleSpinBox(self)
        self.doubleSpinBox.setGeometry(240, 169, 62, 22)
        self.doubleSpinBox.setMaximum(1.00)
        self.doubleSpinBox.setMinimum(0.00)
        self.doubleSpinBox.setVisible(False)
        self.doubleSpinBox.editingFinished.connect(self.doubleSpinBox_onChange)

        self.checkBoxLockMax = QCheckBox(self.lang["lockMax"], self)
        self.checkBoxLockMax.setGeometry(200, 70, 85, 20)
        self.checkBoxLockMax.setCheckable(True)
        self.checkBoxLockMax.setVisible(False)
        self.checkBoxLockMax.clicked.connect(self.checkBoxLockMax_onClicked)

        self.checkBoxOpen = QCheckBox(self.lang["open"], self)
        self.checkBoxOpen.setGeometry(200, 170, 85, 20)
        self.checkBoxOpen.setCheckable(True)
        self.checkBoxOpen.setVisible(False)
        self.checkBoxOpen.clicked.connect(self.checkBoxOpen_onClicked)

        self.statusBar = QStatusBar(self)
        self.statusBar.setGeometry(0, 201, 358, 22)

        logging.info("窗口初始化结束")

        self.statusBar.showMessage(f'{self.lang["wait_game"]}', 5000)
        self.listWidget.setCurrentRow(0)
        self.checkVisit(self.listWidget.currentItem().statusTip())
        self.c_key = self.listWidget.currentItem().statusTip()

    def closeEvent(self, e):
        logging.info("窗口关闭")
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
            enable = self.curr_cfg[current_key]["enable"]
            self.checkBoxEnable.setVisible(True)
            self.checkBoxEnable.setChecked(True) if enable else self.checkBoxEnable.setChecked(False)
        if self.checkBoxEnable.isChecked():
            if "lock" in self.def_cfg[current_key]:
                self.checkBoxLock.setChecked(self.curr_cfg[current_key]["lock"])
                self.checkBoxLock.setVisible(True)
            if "lock_to_max" in self.def_cfg[current_key] and self.checkBoxLock.isChecked():
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
        else:
            self.statusBar.showMessage(f'{self.lang["wait_game"]}', 5000)
        self.c_key = current_key
        logging.info(f"{current_text} {current_key}: {self.curr_cfg[current_key]}")
        self.checkVisit(current_key)
