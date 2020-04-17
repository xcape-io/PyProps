#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
SketchApp.py

SketchApp extends MqttConsoleApp to implement automation sketch in a PyQt5 
console application.
'''

from constants import *
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot
from MqttConsoleApp import MqttConsoleApp
import re, sys
import RPi.GPIO as GPIO

class SketchApp(MqttConsoleApp):

	actuatorReceived = pyqtSignal(str)

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False, gpio_bcm=True, no_gpio=False):

		super().__init__(argv, client, debugging_mqtt)
		
		self._noGpio = no_gpio
		
		if not self._noGpio and self.raspberryPiVersion():
			import RPi.GPIO as GPIO
			if gpio_bcm:
				GPIO.setmode(GPIO.BCM)
			else:
				GPIO.setmode(GPIO.BOARD)

		if self._mqttInbox:
			self._mqttClient.message_callback_add(self._mqttInbox, self._mqttOnActuator)

		self.actuatorReceived.connect(self.onActuatorReceived)
		self.messageReceived.connect(self.onMessageReceived)

		self.setupAutomation()

		self._mqttDataCount = 0

		self._mqttDataTimer = QTimer()
		self._mqttDataTimer.setInterval(SKETCH_INTERVAL_DATA)
		self._mqttDataTimer.timeout.connect(self.publishDataOnTick)
		self._mqttDataTimer.start()
		self._logger.info("{0} {1} {2}".format(self.tr("Data change will be published every"), SKETCH_INTERVAL_DATA, self.tr("milliseconds")))
		self._logger.info("{0} {1} {2}".format(self.tr("Data full publishing will occur every"), SKETCH_INTERVAL_DATA * SKETCH_DATA_COUNT, self.tr("milliseconds")))

		self._automationTimer = QTimer()
		self._automationTimer.setInterval(SKETCH_INTERVAL_AUTOMATION)
		self._automationTimer.timeout.connect(self.processAutomationOnTick)
		self._automationTimer.start()
		self._logger.info("{0} {1} {2}".format(self.tr("Automation processing will run every"), SKETCH_INTERVAL_AUTOMATION, self.tr("milliseconds")))
				
	#__________________________________________________________________
	def _mqttOnActuator(self, client, userdata, msg):

		message = None
		try:
			message = msg.payload.decode(encoding="utf-8", errors="strict")
		except:
			pass

		if message:
			self._logger.info(self.tr("Message received : '") + message + self.tr("' in ") + msg.topic)
			self.actuatorReceived.emit(message)
		else:
			self._logger.warning("{0} {1}".format(self.tr("MQTT message decoding failed on"), msg.topic))

	#__________________________________________________________________
	@pyqtSlot(str)
	def onActuatorReceived(self, action):

		if action == "@PING":
			self.publishMessage(self._mqttOutbox, "PONG")
		else:
			self.performAction(action)

	#__________________________________________________________________
	@pyqtSlot(str, str)
	def onMessageReceived(self, topic, message):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' might be implemented in derived sketch (' + self.__class__.__name__ + ')')

	#__________________________________________________________________
	def performAction(self, message):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' must be implemented in derived sketch (' + self.__class__.__name__ + ')')
			
	#__________________________________________________________________
	def processAutomation(self):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' must be implemented in derived sketch (' + self.__class__.__name__ + ')')
	
	#__________________________________________________________________
	@pyqtSlot()
	def processAutomationOnTick(self):
		self.processAutomation()
	
	#__________________________________________________________________
	def publishAllData(self):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' must be implemented in derived sketch (' + self.__class__.__name__ + ')')
		
	#__________________________________________________________________
	def publishDataChanges(self):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' must be implemented in derived sketch (' + self.__class__.__name__ + ')')

	#__________________________________________________________________
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

	#__________________________________________________________________
	@pyqtSlot()
	def quit(self, a=None, b=None):
		
		GPIO.cleanup() 
		MqttConsoleApp.quit(self)
	
	#__________________________________________________________________
	def raspberryPiVersion(self):
		"""Detect the version of the Raspberry Pi.  Returns either 1, 2 or
		None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
		Raspberry Pi 2 (model B+), or not a Raspberry Pi.
		Thanks to https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/Platform.py
		"""
		# Check /proc/cpuinfo for the Hardware field value.
		# 2708 is pi 1
		# 2709 is pi 2
		# 2835 is pi 3 on 4.9.x kernel
		# Anything else is not a pi.
		try:
			with open('/proc/cpuinfo', 'r') as infile:
				cpuinfo = infile.read()
			# Match a line like 'Hardware   : BCM2709'
			match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
							  flags=re.MULTILINE | re.IGNORECASE)
			if not match:
				# Couldn't find the hardware, assume it isn't a pi.
				return None
			if match.group(1) == 'BCM2708':
				# Pi 1
				return 1
			elif match.group(1) == 'BCM2709':
				# Pi 2
				return 2
			elif match.group(1) == 'BCM2835':
				# Pi 3 / Pi on 4.9.x kernel
				return 3
			else:
				# Something else, not a pi.
				return None
		except:
				return None
			
	#__________________________________________________________________
	def setupAutomation(self):
		self._logger.debug('SketchApp.' + sys._getframe(0).f_code.co_name + ' must be implemented in derived sketch (' + self.__class__.__name__ + ')')
		
