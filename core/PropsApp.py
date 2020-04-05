#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PropsApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

Props base class extends MqttApp:
- add automation
- agnostic to asyncio, Qt, Tkinter or Kivy
- add methods to support Room protocol like ArduinoProps
    DATA -> send variables to control
    MESG -> send text to display in control
    DONE -> acknowledge that a command has been performed
    OMIT -> acknowledge that a command has been ignored
    OVER -> notify that a challenge is over
    REQU -> request a command to another props
    PROG -> request a control program
"""

from MqttApp import MqttApp
from constants import *


class PropsApp(MqttApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

    '''
        void addData(PropsData*);
    '''
    # __________________________________________________________________
    def sendAllData(self):
        self.publishAllData()

    # __________________________________________________________________
    def sendDataChanges(self):
        self.publishDataChanges()

    # __________________________________________________________________
    def sendData(self, data):
        self.publishMessage(self._mqttOutbox, "DATA " + message)

    # __________________________________________________________________
    def sendDone(self, action):
        self.publishMessage(self._mqttOutbox, "DONE " + message)

    # __________________________________________________________________
    def sendMesg(self, message):
        self.publishMessage(self._mqttOutbox, "MESG " + message)

    # __________________________________________________________________
    def sendMesg(self, message, topic):
        self.publishMessage(topic, "MESG " + message)

    # __________________________________________________________________
    def sendOmit(self, action):
        self.publishMessage(self._mqttOutbox, "OMIT " + action)

    # __________________________________________________________________
    def sendOver(self, challenge):
        self.publishMessage(self._mqttOutbox, "OVER " + challenge)

    # __________________________________________________________________
    def sendProg(self, program):
        self.publishMessage(self._mqttOutbox, "PROG " + program)

    # __________________________________________________________________
    def sendRequ(self, request):
        self.publishMessage(self._mqttOutbox, "REQU " + request)

    # __________________________________________________________________
    def sendRequ(self, request, topic):
        self.publishMessage(topic, "REQU " + request)
