#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
BlinkApp.py

Pygame BlinkApp extends ThreadingProp.
'''

from constants import *

from ThreadingProp import ThreadingProp
from PropData import PropData

import os, threading, time
if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
	import RPi.GPIO as GPIO

import pygame

		
class BlinkApp(ThreadingProp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)

		GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)

		self._dingChannel = pygame.mixer.Channel(0)
		self._dingSound = pygame.mixer.Sound("audio/ringtone.wav")
		self._dingSound.set_volume(0.5)

		self._led_p = PropData('led', bool, 0, logger=self._logger)
		self.addData(self._led_p)
		self._blinking_p = PropData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
		self.addData(self._blinking_p)
		self._sounding_p = PropData('sounding', bool, 0, alias=("yes", "no"), logger=self._logger)
		self.addData(self._sounding_p)

		self._led_p.update(False)
		self._blinking_p.update(False)
		self._sounding_p.update(True)

		self._blinkTimerThread = threading.Thread()
		self._blinkTimerThread = threading.Thread(target=self.blinkThread())
		self._blinkTimerThread.daemon = True

		self._blinkTimerThread.start()

	#__________________________________________________________________
	def onConnect(self, client, userdata, flags, rc):
		# extend as a virtual method
		self.sendAllData()

	#__________________________________________________________________
	def onDisconnect(self, client, userdata, rc):
		# extend as a virtual method
		pass

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		#print(topic, message)
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

	#__________________________________________________________________
	def blinkThread(self):
		# run in its own thread
		while True:
			try:
				if self._blinking_p.value():
					self._led_p.update(not self._led_p.value())
					if self._sounding_p.value() and self._led_p.value():
						self._dingChannel.play(self._dingSound)
					GPIO.output(GPIO_BLINKING_LED, self._led_p.value())
					self.sendData(str(self._led_p))  # immediate notification
			except:
				pass
			finally:
				time.sleep(1.0)

