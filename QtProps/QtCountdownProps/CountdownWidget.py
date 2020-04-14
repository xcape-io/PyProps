#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CountdownFrame.py
MIT License (c) Marie Faure <dev at faure dot systems>

Countdown main widget.
"""

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel


class CountdownWidget(QWidget):
    aboutToClose = pyqtSignal()

    # __________________________________________________________________
    def __init__(self, logger):
        super().__init__()

        self._logger = logger

        # always on top sometimes doesn't work
        #self.setAttribute(Qt.WA_AlwaysStackOnTop)
        #self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self._buildUi()

    # __________________________________________________________________
    def _buildUi(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        self._chronoLabel = QLabel("00:00")
        self._chronoLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        main_layout.addWidget(self._chronoLabel)

        self.setLayout(main_layout)

    # __________________________________________________________________
    @pyqtSlot(str)
    def onTeletextDisplayMessage(self, message):
        if message == "-":
            message = ""
        message = message.replace('\n', '<br>')

    # __________________________________________________________________
    @pyqtSlot(str)
    def onPropsMessage(self, message):
        pass

    # __________________________________________________________________
    def closeEvent(self, e):
        self.aboutToClose.emit()
