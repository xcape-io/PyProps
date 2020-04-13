#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
EducationalApp.py

EducationalApp application extends SketchApp.

Sainsmart Relay 16: inpu are active LOW (apply 0 to switch ON)

'''

import os

from PropsData import PropsData
from PyQt5.QtCore import pyqtSlot, QTimer
from QtPropsApp import QtPropsApp
from constants import *

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO
    ####import MFRC522 # modified for GPIO mode


class EducationalApp(QtPropsApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)

        self._led_p = PropsData('led', bool, 0, logger=self._logger)
        self.addData(self._led_p)
        self._blinking_p = PropsData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._blinking_p)
        self._sounding_p = PropsData('sounding', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._sounding_p)

        self._led_p.update(False)
        self._blinking_p.update(False)
        self._sounding_p.update(True)

        self.addPeriodicAction("blink", self.blink, 1.0)

        self._mqttDataCount = 0

        self._mqttDataTimer = QTimer()
        self._mqttDataTimer.setInterval(SKETCH_INTERVAL_DATA)
        self._mqttDataTimer.timeout.connect(self.publishDataOnTick)
        self._mqttDataTimer.start()
        self._logger.info("{0} {1} {2}".format(self.tr("Data change will be published every"), SKETCH_INTERVAL_DATA,
                                               self.tr("milliseconds")))
        self._logger.info("{0} {1} {2}".format(self.tr("Data full publishing will occur every"),
                                               SKETCH_INTERVAL_DATA * SKETCH_DATA_COUNT, self.tr("milliseconds")))

    # __________________________________________________________________
    def blink(self):
        while True:
            try:
                if self._blinking_p.value():
                    self._led_p.update(not self._led_p.value())
                    GPIO.output(GPIO_BLINKING_LED, self._led_p.value())
                    self.sendData(str(self._led_p))  # immediate notification
            except Exception as e:
                self._logger.error("Failed to execute periodic 'blink'")
                self._logger.debug(e)

    # __________________________________________________________________
    def onMessage(self, topic, message):
        print(topic, message)
        if message == "app:startup":
            self.sendAllData()
            self.sendDone(message)
        elif message == "app:data":
            self.sendAllData()
            self.sendDone(message)
        elif message.startswith("blink:"):
            if message.endswith(":0"):
                self._blinking_p.update(False)
                self.sendDataChanges()
                self.sendDone(message)
            elif message.endswith(":1"):
                self._blinking_p.update(True)
                self.sendDataChanges()
                self.sendDone(message)
            else:
                self.sendOmit(message)
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

    # __________________________________________________________________
    def publishAllData(self):
        # self._logger.debug("Publish all")

        data = "DATA " + "toto=0" + " tata=0"
        self._publishMessage(self._mqttOutbox, data)

    # __________________________________________________________________
    def publishDataChanges(self):
        # self._logger.debug("Publish changes")
        data = "DATA " + "toto=0"
        self._publishMessage(self._mqttOutbox, data)

    # __________________________________________________________________
    @pyqtSlot()
    def publishDataOnTick(self):

        if self.isConnectedToMqttBroker():
            if self._mqttDataCount:
                self.publishDataChanges()
            else:
                self.publishAllData()
            self._mqttDataCount = self._mqttDataCount + 1
            if self._mqttDataCount > SKETCH_DATA_COUNT:
                self._mqttDataCount = 0
