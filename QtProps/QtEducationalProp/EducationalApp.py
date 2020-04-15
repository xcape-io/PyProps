#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
EducationalApp.py

EducationalApp application extends SketchApp.

Sainsmart Relay 16: inpu are active LOW (apply 0 to switch ON)

'''

import os

from PropData import PropData
from PyQt5.QtMultimedia import QSound
from QtPropApp import QtPropApp
from constants import *

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO
    ####import MFRC522 # modified for GPIO mode


class EducationalApp(QtPropApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)

        self._sound = QSound("audio/ringtone.wav")

        self._led_p = PropData('led', bool, 0, logger=self._logger)
        self.addData(self._led_p)
        self._blinking_p = PropData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._blinking_p)
        self._sounding_p = PropData('sounding', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._sounding_p)

        self._led_p.update(False)
        self._blinking_p.update(False)
        self._sounding_p.update(True)

        self.addPeriodicAction("blink", self.blink, 1.0)

        self._nfc_module_p = PropData('nfc', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._nfc_module_p)

        if NFC_MODULE is None:
            self._logger.info("No NFC module configured'")
            self._blinking_p.update(False)


    # __________________________________________________________________
    def blink(self):
        try:
            if self._blinking_p.value():
                self._led_p.update(not self._led_p.value())
                if self._sounding_p.value() and self._led_p.value():
                        self._sound.play()
                GPIO.output(GPIO_BLINKING_LED, self._led_p.value())
                self.sendData(str(self._led_p))  # immediate notification
        except Exception as e:
            self._logger.error("Failed to execute periodic 'blink'")
            self._logger.debug(e)

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
