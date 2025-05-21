# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lib.default_def import default_config
from lib.nb2data import *


def writeConfig(_jsonObj):
    with open(f'./config/config.json', 'w', encoding="UTF-8") as f:
        f.write(json.dumps(_jsonObj, ensure_ascii=False))
        f.close()


def readConfig():
    cx = None
    if os.path.exists("./config/config.json"):
        with open(f'./config/config.json', 'r', encoding="UTF-8") as f:
            cx = json.loads(f.read())
            f.close()
    return cx


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("初始化窗口中")
        self.c_key = None
        # 设置窗口标题和大小
        self.setWindowTitle("霓虹深渊2修改器")
        self.setWindowIcon(QIcon(self.resource_path(os.path.join("resources/", "icon.ico"))))
        self.resize(358, 201)
        self.setFixedSize(self.width(), self.height())

        self.curr_cfg = readConfig()
        self.def_cfg = default_config

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, 0, 171, 200)
        self.listWidget.setStyleSheet("QListWidget::item { height: 20px; font-size: 11px; text-overflow: clip; }")
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for key in self.def_cfg.keys():
            item = QListWidgetItem()
            item.setText(f'{self.def_cfg[key]["_self"]}')
            item.setStatusTip(f'{key}')
            self.listWidget.addItem(item)

        self.listWidget.clicked.connect(self.listWidget_onClicked)

        self.checkBoxEnable = QCheckBox("启用", self)
        self.checkBoxEnable.setGeometry(200, 10, 85, 20)
        self.checkBoxEnable.setCheckable(True)
        self.checkBoxEnable.setVisible(False)
        self.checkBoxEnable.clicked.connect(self.checkBoxEnable_onClicked)

        self.checkBoxLock = QCheckBox("锁定", self)
        self.checkBoxLock.setGeometry(200, 40, 85, 20)
        self.checkBoxLock.setCheckable(True)
        self.checkBoxLock.setVisible(False)
        self.checkBoxLock.clicked.connect(self.checkBoxLock_onClicked)

        self.label = QLabel("数值：", self)
        self.label.setGeometry(200, 170, 40, 20)
        self.label.setVisible(False)

        self.SpinBox = QSpinBox(self)
        self.SpinBox.setGeometry(240, 169, 62, 22)
        self.SpinBox.setMaximum(999)
        self.SpinBox.setMinimum(0)
        self.SpinBox.setVisible(False)
        self.SpinBox.valueChanged.connect(self.SpinBox_onChange)

        self.doubleSpinBox = QDoubleSpinBox(self)
        self.doubleSpinBox.setGeometry(240, 169, 62, 22)
        self.doubleSpinBox.setMaximum(1.00)
        self.doubleSpinBox.setMinimum(0.00)
        self.doubleSpinBox.setVisible(False)
        self.doubleSpinBox.valueChanged.connect(self.doubleSpinBox_onChange)

        self.checkBoxLockMax = QCheckBox("锁定至最大", self)
        self.checkBoxLockMax.setGeometry(200, 70, 85, 20)
        self.checkBoxLockMax.setCheckable(True)
        self.checkBoxLockMax.setVisible(False)
        self.checkBoxLockMax.clicked.connect(self.checkBoxLockMax_onClicked)

        self.checkBoxOpen = QCheckBox("开启", self)
        self.checkBoxOpen.setGeometry(200, 170, 85, 20)
        self.checkBoxOpen.setCheckable(True)
        self.checkBoxOpen.setVisible(False)
        self.checkBoxOpen.clicked.connect(self.checkBoxOpen_onClicked)

        logging.info("窗口初始化结束")

    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = "./"
        ret_path = os.path.join(base_path, relative_path)
        return ret_path

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
            self.checkBoxEnable.setVisible(True)
            self.checkBoxEnable.setChecked(True) if self.curr_cfg[current_key]["enable"] else self.checkBoxEnable.setChecked(False)
        if self.checkBoxEnable.isChecked():
            if "lock" in self.def_cfg[current_key]:
                self.checkBoxLock.setChecked(self.curr_cfg[current_key]["lock"])
                self.checkBoxLock.setVisible(True)
            if "lock_to_max" in self.def_cfg[current_key]:
                self.checkBoxLockMax.setChecked(self.curr_cfg[current_key]["lock_to_max"])
                self.checkBoxLockMax.setVisible(True)
            match NB2_TYPE[current_key]:
                case "d":
                    self.label.setVisible(True)
                    self.SpinBox.setVisible(True)
                    self.SpinBox.setValue(self.curr_cfg[current_key]["value"])
                case "f":
                    self.label.setVisible(True)
                    self.doubleSpinBox.setVisible(True)
                    self.doubleSpinBox.setValue(self.curr_cfg[current_key]["value"])
                case "b":
                    self.checkBoxOpen.setVisible(True)
                    self.checkBoxOpen.setChecked(True) if self.curr_cfg[current_key]["value"] == 1 else self.checkBoxOpen.setChecked(False)

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
        current_key = self.listWidget.currentItem()
        select_item_text = f'{current_key.text()}'
        select_item_key = f'{current_key.statusTip()}'
        self.c_key = select_item_key
        logging.info(f"{select_item_text} {select_item_key}: {self.curr_cfg[select_item_key]}")
        self.checkVisit(select_item_key)
