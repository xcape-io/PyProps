#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlinkEchoApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

BlinkEchoApp extends MqttApp.
"""

from constants import *
from PropsApp import PropsApp
from PropsData import PropsData
from Periodic import Periodic

import os, platform, sys, logging
import RPi.GPIO as GPIO


class BlinkEchoApp(PropsApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)

        self._led_p = PropsData('led', bool, 0, logger=self._logger)
        self.addData(self._led_p)
        self._blinking_p = PropsData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._blinking_p)

        self._led_p.update(False)
        self._blinking_p.update(False)

        self._last_echo_p = PropsData('last_echo', str, BLANK_ECHO, logger=self._logger)
        self.addData(self._last_echo_p)

        self._blinking_periodic = Periodic(self.blink, 1.0, logger=self._logger)

        ##await self._blinking_periodic.start()

    # __________________________________________________________________
    def blink(self):
        self._led_p.update(not self._led_p.value())
        GPIO.output(GPIO_BLINKING_LED, self._led_p.value())
        self.sendData(str(self._led_p))  # immediate notification

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        self.sendMesg("echo on")

    # __________________________________________________________________
    def onDisconnect(self, client, userdata, rc):
        # extend as a virtual method
        self.sendMesg("echo off")

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message == "app:startup":
            self.sendAllData()
            self.sendDone(message)
        elif message.startswith("echo:"):
            text = message[5:]
            self.sendMesg("echo: " + text)
            self._last_echo_p.update(text)
            self.sendDataChanges()
            self.sendDone(message)
        elif message.startswith("blink:"):
            if message.endswith(":0"):
                self._blinking_p.update(False)
                self.sendData(str(self._blinking_p))  # accurate flip/flop
                self.sendDone(message)
            elif message.endswith(":1"):
                self._blinking_p.update(True)
                self.sendData(str(self._blinking_p))  # accurate flip/flop
                self.sendDone(message)
            else:
                self.sendOmit(message)
        else:
            self.sendOmit(message)
