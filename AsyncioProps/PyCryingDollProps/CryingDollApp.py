#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
CryingDollApp.py (version 0.1 initial)

CryingDollApp extends MqttApp.

'''

from constants import *

import sys
sys.path.append("../../core")

from MqttApp import MqttApp
from MqttVar import MqttVar
from Sound import Sound

import RPi.GPIO as GPIO
import random, os
		
class CryingDollApp(MqttApp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)
		
		self._lumiere_p = MqttVar('lumière' , bool, 0, logger = self._logger)
		self._publishable.append(self._lumiere_p )
		self._pleurs_p = MqttVar('pleurs' , bool, 0, logger = self._logger)
		self._publishable.append(self._pleurs_p )
		self._active_p = MqttVar('activé' , bool, 0, alias=("oui","non"), logger = self._logger)
		self._publishable.append(self._active_p )

		GPIO.setup(GPIO_RELAY_LIGHT, GPIO.OUT,  initial=GPIO.LOW)

		for pin in GPIO_VIBRATION_SENSORS:
			GPIO.setup(pin, GPIO.IN)
			GPIO.add_event_detect(pin, GPIO.RISING, callback=self.vibrate, bouncetime=200)
			self._logger.info("{} {}".format("Setup vibration sensor input pin on", str(pin)))
		
		self._sound = Sound(self._logger)
		
		self._lumiere_p.update(False)
		self._pleurs_p.update(False)
		self._active_p.update(False)
		
		os.system("amixer cset numid=3 1") # audio jack
		os.system("amixer set 'PCM' -- 400") # volume fort

	#__________________________________________________________________
	def onConnect(self, client, userdata, flags, rc):
		# extend as a virtual method
		pass
		
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
		elif message.startswith("activer:"):
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
		elif message.startswith("lumière:"):
			if message.endswith(":éteindre"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.LOW)
				self._lumiere_p.update(False)
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._lumiere_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":allumer"):
				GPIO.output(GPIO_RELAY_LIGHT,  GPIO.HIGH)
				self._lumiere_p.update(True)	
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._lumiere_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)

		else:
			self.publishMessage(self._mqttOutbox, "OMIT " + message)

	#__________________________________________________________________
	def publishAllData(self):
		
		self._pleurs_p.update(self._sound.isPlaying() )
		super().publishAllData()
		
	#__________________________________________________________________
	def publishDataChanges(self):
		
		self._pleurs_p.update(self._sound.isPlaying() )
		super().publishDataChanges()
		
	#__________________________________________________________________
	def vibrate(self, pin):
		#print("VIBRATE", pin)
		
		if not self._active_p.value() or self._sound.isPlaying():
			return			

		self._sound.play(AUDIO_CRYING[random.randint(1, len(AUDIO_CRYING)) - 1])
		self.publishDataChanges()
