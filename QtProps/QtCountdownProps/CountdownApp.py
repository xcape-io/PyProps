#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
CountdownApp.py

CountdownApp application extends SketchApp.

Sainsmart Relay 16: inpu are active LOW (apply 0 to switch ON)

'''

import os, sys

from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from PropsData import PropsData
from QtPropsApp import QtPropsApp
from CountdownWidget import CountdownWidget

from constants import *

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO


class CountdownApp(QtPropsApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        self._sounding_p = PropsData('sounding', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._sounding_p)

        self._sounding_p.update(True)

        style = ""
        qss = open("Countdown.css",'r')
        with qss:
            style = style + qss.read()

        self._mainWidget = CountdownWidget(self._logger)
        self._mainWidget.setStyleSheet(style)
        self._mainWidget.aboutToClose.connect(self.exitOnClose)
        self._mainWidget.show()

        self._mainWidget.showFullScreen()
        self._mainWidget.setCursor(Qt.BlankCursor)

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        self.sendAllData()

    # __________________________________________________________________
    def onMessage(self, topic, message):
        print(topic, message)
        if message == "app:startup":
            self.sendAllData()
            self.sendDone(message)
        elif message == "app:data":
            self.sendAllData()
            self.sendDone(message)
        elif message.startswith("sound:"):
            if message.endswith(":0"):
                self._sounding_p.update(False)
                self.sendDataChanges()
                self.sendDone(message)
            elif message.endswith(":1"):
                self._sounding_p.update(True)
                self.sendDataChanges()
                self.sendDone(message)

            else:
                self.sendOmit(message)
        else:
            self.sendOmit(message)
