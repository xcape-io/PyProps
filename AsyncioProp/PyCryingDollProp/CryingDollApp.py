#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryingDollApp.py
MIT License (c) Faure Systems <dev at faure dot systems>

CryingDollApp extends AsyncioProp.
"""

from constants import *

from AsyncioProp import AsyncioProp
from PropData import PropData
from Sound import Sound

import random, os
if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
	import RPi.GPIO as GPIO

class CryingDollApp(AsyncioProp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		super().__init__(argv, client, debugging_mqtt)
		
		self._light_p = PropData('light' , bool, 0, logger = self._logger)
		self.addData(self._light_p )
		self._crying_p = PropData('crying' , bool, 0, logger = self._logger)
		self.addData(self._crying_p )
		self._active_p = PropData('activated' , bool, 0, alias=("yes","no"), logger = self._logger)
		self.addData(self._active_p )

		GPIO.setup(GPIO_RELAY_LIGHT, GPIO.OUT,  initial=GPIO.LOW)

		for pin in GPIO_VIBRATION_SENSORS:
			GPIO.setup(pin, GPIO.IN)
			GPIO.add_event_detect(pin, GPIO.RISING, callback=self.vibrate, bouncetime=200)
			self._logger.info("{} {}".format("Setup vibration sensor input pin on", str(pin)))
		
		self._sound = Sound(self._logger)
		
		self._light_p.update(False)
		self._crying_p.update(False)
		self._active_p.update(False)
		
		os.system("amixer cset numid=3 1") # jack audio
		os.system("amixer set 'PCM' -- 400") # loud volume

	#__________________________________________________________________
	def cry(self):
		self._sound.play(AUDIO_CRYING[random.randint(1, len(AUDIO_CRYING)) - 1])
		self.sendDataChanges()

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
		print(topic, message)
		if message == "app:startup":
			self.sendAllData()
			self.sendDone(message)
		elif message.startswith("activate:"):
			if message.endswith(":0"):
				self._active_p.update(False)
				self.sendDataChanges()
				self.sendDone(message)
			elif message.endswith(":1"):
				self._active_p.update(True)	
				self.sendDataChanges()
				self.sendDone(message)
			else:
				self.sendOmit(message)
		elif message.startswith("cry:_"):
			self.cry()
			self.sendDone(message)
		elif message.startswith("light:"):
			if message.endswith(":off"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.LOW)
				self._light_p.update(False)
				self.sendDataChanges()
				self.sendDone(message)
			elif message.endswith(":on"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.HIGH)
				self._light_p.update(True)
				self.sendDataChanges()
				self.sendDone(message)
			else:
				self.sendOmit(message)
		else:
			self.sendOmit(message)

	#__________________________________________________________________
	def sendAllData(self):
		self._crying_p.update(self._sound.isPlaying() )
		super().sendAllData()
		
	#__________________________________________________________________
	def sendDataChanges(self):
		self._crying_p.update(self._sound.isPlaying() )
		super().sendDataChanges()
		
	#__________________________________________________________________
	def vibrate(self, pin):
		if not self._active_p.value() or self._sound.isPlaying():
			return
		self.cry()
