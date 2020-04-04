#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
MinimalApp.py

MinimalApp application extends MqttKivyApp.

'''

from kivy.uix.button import Button

from constants import *
from MqttKivyApp import MqttKivyApp

#from MqttKivyApp import _is_rpi
#if _is_rpi: import RPi.GPIO as GPIO

class MinimalApp(MqttKivyApp):

	#__________________________________________________________________
	def __init__(self, client, debugging_mqtt=False):

		super().__init__(client, debugging_mqtt)

	#__________________________________________________________________
	def build(self):
		# return a Button() as a root widget
		return Button(text=_('hello') )

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		print(topic, message)
		self.publishMessage(self._mqttOutbox, "OMIT " + message)
