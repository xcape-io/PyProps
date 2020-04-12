#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
EducationalApp.py

EducationalApp application extends SketchApp.

Sainsmart Relay 16: inpu are active LOW (apply 0 to switch ON)

'''

import platform
from constants import *
from QtPropsApp import QtPropsApp
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
import threading, time
import RPi.GPIO as GPIO
####import MFRC522 # modified for GPIO mode

class EducationalApp(QtPropsApp):
	actuatorReceived = pyqtSignal(str)

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):

		super().__init__(argv, client, debugging_mqtt)
		# let's initialize automation stuff in setupAutomation()
		GPIO.setmode(GPIO.BCM)

		if self._mqttInbox:
			self._mqttClient.message_callback_add(self._mqttInbox, self.mqttOnActuator)

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
	@pyqtSlot()
	def doSequence(self):

		if self._sequence:
			on, x, interval = self._sequence.pop(0)
			if on:
				if self.setLetterOn(x):
					self._display = x
				else:
					self._logger.warning("{} '{}'".format(self.tr("Ignore set ON letter"), x))
			else:
				if self.setLetterOff(x):
					self._display = None
				else:
					self._logger.warning("{} '{}'F".format(self.tr("Ignore set OFF letter"), x))
			self.publishAllData()
			QTimer.singleShot(interval, self.doSequence)
		else:
			self.setAllLettersOff()		
			self._display = None
			self.publishMessage(PIRELAY_INBOX, "lumières-salon:allumer")
			self.publishAllData()					

	#__________________________________________________________________
	def mqttOnActuator(self, client, userdata, msg):

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
		#self._logger.debug("Action " + message)

		if message == "app:startup":
			self._mqttDataCount = 0
			self.publishAllData()
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			
		elif message.startswith("éclairer:"):
			text = message[8:]
			# fire async sequence
			self._sequence = []

			for x in text:
				self._sequence.append((ON, x, DISPLAY_ON_TIME))
				self._sequence.append((OFF, x, DISPLAY_OFF_TIME))
			
			self.setAllLettersOff()		
			self._display = None
			self.publishAllData()			
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			
			self.publishMessage(PIRELAY_INBOX, "lumières-salon:éteindre")
			QTimer.singleShot(1000, self.doSequence)
			
		elif message == "effet:guirlande":
			# fire async effect
			self._sequence = []

			for x in list(map(chr, range(65, 91))) + list(map(chr, range(0x30, 0x3A))):
				self._sequence.append((ON, x, GARLAND_ON_TIME))
				self._sequence.append((OFF, x, GARLAND_OFF_TIME))
			
			self.setAllLettersOff()		
			self._display = None
			self.publishAllData()			
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			
			QTimer.singleShot(0, self.doSequence)

		elif message == "effet:spinning":
			# fire async effect
			self.setAllLettersOff()		
			self._display = "spinning"
			self.publishAllData()			
			time.sleep(2.0)
			threading.Thread(target=self.processSpinning, ).start()
			self.publishMessage(self._mqttOutbox, "DONE " + message)

		elif message == "stop":

			self._sequence = []
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			
		else:
			if False:
				pass
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				print(message)
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
			
	#__________________________________________________________________
	def processAutomation(self):
		'''read sensors and fire related sound'''
		#self._logger.debug("Automation processing")
		if self._criticalMessage: return


		''' strange behavior, when a card is present: 
				it loops detected/not detected
			so we read twice...!
		'''
		
		detected = 0
		''' read RFID '''
		if self._MIFAREReader:
			# Scan for cards    
			####(status,TagType) = self._MIFAREReader.MFRC522_Request(self._MIFAREReader.PICC_REQIDL)
			# If a card is found
			####if status == self._MIFAREReader.MI_OK:
			####	detected = detected + 1
				
			# Get the UID of the card
			####(status,uid) = self._MIFAREReader.MFRC522_Anticoll()
			# If we have the UID
			####if status == self._MIFAREReader.MI_OK:
			####	detected = detected + 1
				
			''' read a second time '''
			# Scan for cards    
			####(status,TagType) = self._MIFAREReader.MFRC522_Request(self._MIFAREReader.PICC_REQIDL)
			# If a card is found
			####if status == self._MIFAREReader.MI_OK:
			####	detected = detected + 1
				
			# Get the UID of the card
			####(status,uid) = self._MIFAREReader.MFRC522_Anticoll()
			# If we have the UID
			####if status == self._MIFAREReader.MI_OK:
			####	detected = detected + 1
						
			if detected == 2:
				# card present
				if not self._cardPresent:
					data = "DATA carte=oui"
					self.publishMessage(self._mqttOutbox, data)
				self._cardPresent = True				
			else:
				if self._cardPresent:
					data = "DATA carte=non"
					self.publishMessage(self._mqttOutbox, data)					
				self._cardPresent = False

	# __________________________________________________________________
	@pyqtSlot()
	def processAutomationOnTick(self):
		self.processAutomation()

	#__________________________________________________________________
	def processSpinning(self):

		alphabet = []
		for x in list(map(chr, range(65, 91))):
			alphabet.append(x)
		
		try:
			sleep_on = 0.250
			sleep_on_min = 0.030
			sleep_on_substract = 0.010
			sleep_off = 0.150
			sleep_off_min = 0.010
			sleep_off_substract = 0.005
			ref = 0
			round = 0
			while round < 26 * 5:
				self.setLetterOn(alphabet[ref], nolog=True)
				time.sleep(sleep_on)
				self.setLetterOff(alphabet[ref], nolog=True)
				time.sleep(sleep_off)
				if sleep_on > sleep_on_min + sleep_on_substract:
					sleep_on = sleep_on - sleep_on_substract
				else:
					sleep_on = sleep_on_min
				if sleep_off > sleep_off_min + sleep_off_substract:
					sleep_off = sleep_off - sleep_off_substract
				else:
					sleep_off = sleep_off_min
				ref = (ref + 1) % len(alphabet)
				round = round + 1
				print(ref, round, alphabet[ref], sleep_on, sleep_off)
		except Exception as e:
			self._logger.error(self.tr("Error in spinning process"))
			self._logger.debug(e)

		self._display = None
		self.publishAllData()			

	#__________________________________________________________________
	def publishAllData(self):
		#self._logger.debug("Publish all")
		if self._criticalMessage:
			self.publishMessage(self._mqttOutbox, "MESG " + self._criticalMessage)
			return

		display = self._display
		if not display: display = '-'
		if self._cardPresent:
			card = 'oui'
		else:
			card = 'non'

		data = "DATA " + "éclairage=" + display + " carte=" + card
		self.publishMessage(self._mqttOutbox, data)

	#__________________________________________________________________
	def publishDataChanges(self):
		#self._logger.debug("Publish changes")

		##data = self._sequence_p.change()
		##data = data.strip()
		##if data:
			##self.publishMessage(self._mqttOutbox, "DATA " + data + " phonemes=" + self.sequenceToPhonemes(self._sequence_p.value()))
		pass

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

	# __________________________________________________________________
	@pyqtSlot()
	def quit(self, a=None, b=None):

		GPIO.cleanup()
		MqttConsoleApp.quit(self)

	#__________________________________________________________________
	def setAllLettersOff(self):

		for rl in RELAYS_ALPHA:
			GPIO.output(RELAYS_ALPHA[rl], GPIO.LOW)
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rl, self.tr("on output"), RELAYS_ALPHA[rl], self.tr("is set to 1 (OFF)")))
		for rn in RELAYS_NUMER:
			GPIO.output(RELAYS_NUMER[rn], GPIO.LOW)
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rn, self.tr("on output"), RELAYS_NUMER[rn], self.tr("is set to 1 (OFF)")))

	#__________________________________________________________________
	def setLetterOff(self, letter, nolog=False):
	
		if letter not in RELAYS: return False
		
		rl, rn = RELAYS[letter]
		GPIO.output(RELAYS_ALPHA[rl], GPIO.LOW)
		if not nolog:
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rl, self.tr("on output"), RELAYS_ALPHA[rl], self.tr("is set to 1 (OFF)")))
		GPIO.output(RELAYS_NUMER[rn], GPIO.LOW)
		if not nolog:
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rn, self.tr("on output"), RELAYS_NUMER[rn], self.tr("is set to 1 (OFF)")))
		return True
		
	#__________________________________________________________________
	def setLetterOn(self, letter, nolog=False):
		
		if letter not in RELAYS: return False
		
		rl, rn = RELAYS[letter]
		GPIO.output(RELAYS_ALPHA[rl], GPIO.HIGH)
		if not nolog:
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rl, self.tr("on output"), RELAYS_ALPHA[rl], self.tr("is set to 0 (ON)")))
		GPIO.output(RELAYS_NUMER[rn], GPIO.HIGH)
		if not nolog:
			self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rn, self.tr("on output"), RELAYS_NUMER[rn], self.tr("is set to 0 (ON)")))
		return True
	
	#__________________________________________________________________
	def setupAutomation(self):
		'''Done even before session started and before thios class constructor'''
		#self._logger.debug("Automation setup")
		
		self._criticalMessage  = None
		self._sequence = []
		self._display = None # one letter at a time, or none
			
		if platform.system() == 'Windows':
			##no GPIO
			self._criticalMessage = "running on Windows (no GPIO)"
		else:
			for rl in RELAYS_ALPHA:
				GPIO.setup(RELAYS_ALPHA[rl], GPIO.OUT, initial=GPIO.LOW)
				self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rl, self.tr("on output"), RELAYS_ALPHA[rl], self.tr("is set to 0")))
			for rn in RELAYS_NUMER:
				GPIO.setup(RELAYS_NUMER[rn], GPIO.OUT, initial=GPIO.LOW)
				self._logger.info("{} {} {} {} {}".format(self.tr("Relay"), rn, self.tr("on output"), RELAYS_NUMER[rn], self.tr("is set to 0")))

		''' setup RFID '''
		self._cardPresent = False
		self._MIFAREReader = None
		try:
			self._MIFAREReader = MFRC522.MFRC522()
			self._logger.info(self.tr("RFID ready"))
		except Exception as e:
			self._MIFAREReader = None
			self._logger.error(self.tr("Error in RFID setup"))
			self._logger.debug(e)
