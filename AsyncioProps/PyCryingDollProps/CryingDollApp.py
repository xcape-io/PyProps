#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryingDollApp.py (version 0.1 initial)

CryingDollApp extends MqttApp.
"""

from constants import *

from PropsApp import PropsApp
from PropsData import PropsData
from Sound import Sound

import RPi.GPIO as GPIO
import random, os
		
class CryingDollApp(PropsApp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		super().__init__(argv, client, debugging_mqtt)
		
		self._light_p = PropsData('light' , bool, 0, logger = self._logger)
		self._publishable.append(self._light_p )
		self._crying_p = PropsData('crying' , bool, 0, logger = self._logger)
		self._publishable.append(self._crying_p )
		self._active_p = PropsData('activated' , bool, 0, alias=("yes","no"), logger = self._logger)
		self._publishable.append(self._active_p )

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
		self.publishDataChanges()

	#__________________________________________________________________
	def onConnect(self, client, userdata, flags, rc):
		# extend as a virtual method
		self.publishAllData()

	#__________________________________________________________________
	def onDisconnect(self, client, userdata, rc):
		# extend as a virtual method
		pass

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		print(topic, message)
		if message == "app:startup":
			self.publishAllData()
			self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("activate:"):
			if message.endswith(":0"):
				self._active_p.update(False)
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._active_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":1"):
				self._active_p.update(True)	
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._active_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("cry:_"):
			self.cry()
			self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("light:"):
			if message.endswith(":off"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.LOW)
				self._light_p.update(False)
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._light_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":on"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.HIGH)
				self._light_p.update(True)
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._light_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)

		else:
			self.publishMessage(self._mqttOutbox, "OMIT " + message)

	#__________________________________________________________________
	def publishAllData(self):
		self._crying_p.update(self._sound.isPlaying() )
		super().publishAllData()
		
	#__________________________________________________________________
	def publishDataChanges(self):
		self._crying_p.update(self._sound.isPlaying() )
		super().publishDataChanges()
		
	#__________________________________________________________________
	def vibrate(self, pin):
		if not self._active_p.value() or self._sound.isPlaying():
			return
		self.cry()
