#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
BlinkApp.py

Pygame BlinkApp extends ThreadingProps.
'''

from constants import *

from ThreadingProps import ThreadingProps
from PropsData import PropsData

import RPi.GPIO as GPIO
import threading, time
		
class BlinkApp(ThreadingProps):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)
		
		GPIO.setmode(GPIO.BCM)
		#GPIO.setwarnings(False)

		GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)

		self._led_p = PropsData('led', bool, 0, logger=self._logger)
		self.addData(self._led_p)
		self._blinking_p = PropsData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
		self.addData(self._blinking_p)

		self._led_p.update(False)
		self._blinking_p.update(False)

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
		else:
			self.sendOmit(message)

	#__________________________________________________________________
	def blinkThread(self):
		# run in its own thread
		while True:
			try:
				if self._blinking_p.value():
					self._led_p.update(not self._led_p.value())
					GPIO.output(GPIO_BLINKING_LED, self._led_p.value())
					self.sendData(str(self._led_p))  # immediate notification
			except:
				pass
			finally:
				time.sleep(1.0)

