#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PodiumApp.py (version 0.2 fix MQTT connection issue)

PodiumApp extends PropApp.

'''

from constants import *

from PropApp import PropApp
from PropData import PropData

import os, re, threading, time, yaml
if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
	import RPi.GPIO as GPIO

import pygame
		
class PodiumApp(PropApp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)

		self._setupRegex = re.compile(r'([^\s]+):([0-9]+)')

		self._keynote_list = []
		self._keynotesDown = []
		self._keynotesReversed = {}
		self._keynotesSampler = {}
		self._keynoteFolder = AUDIO
		self._symboleAudioChannel = {}
		self._keynoteSound = {}
		self._soluce_list = SOLUCE.split()
				
		self._publishAllTimerThread = threading.Thread()
		self._publishAllTimerThread = threading.Thread(target=self.publishAllData)
		self._publishAllTimerThread.daemon = True
		
		self._publishChangesTimerThread = threading.Thread()
		self._publishChangesTimerThread = threading.Thread(target=self.publishDataChanges)
		self._publishChangesTimerThread.daemon = True
		
		self._samplingTimerThread = threading.Thread()
		self._samplingTimerThread = threading.Thread(target=self.samplingKeynotes)
		self._samplingTimerThread.daemon = True
		
		pygame.mixer.set_num_channels(len(KEY_SYMBOLS) + 4)
		pygame.mixer.set_reserved(len(KEY_SYMBOLS) + 4)
		i = 0
		for k in KEY_SYMBOLS:
			self._symboleAudioChannel [k] = pygame.mixer.Channel(i)
			i = i + 1
		self._wrongSymbolAudioChannel= pygame.mixer.Channel(i)
		i = i + 1
		self._palanAudioChannel= pygame.mixer.Channel(i)

		self.loadSound()
					
		''' Interrupt bouncetime is correct at 200ms (but inputs too noisy)
		   so we go for sampling at high rate'''
		   
		for k in KEY_SYMBOLS:
			gpio = KEY_SYMBOLS[k]
			self._keynotesReversed [gpio] = k
			self._keynotesSampler[gpio] = [1] * SAMPLING_SIZE # pulled-up
			# GPIO ports set up as inputs, pulled up to avoid false detection. 
			# Keynote ports are wired to connect to GND on action  
			GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
			self._logger.info("{} {} {}{}".format("GPIO: setup",  k, "input pulled-up.", gpio))

		GPIO.setup(RELAY_JEU_DES_BILLES, GPIO.OUT, initial=GPIO.LOW)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_JEU_DES_BILLES output.", RELAY_JEU_DES_BILLES, GPIO.LOW))

		GPIO.setup(RELAY_LIGHT, GPIO.OUT, initial=GPIO.LOW)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_LIGHT output.", RELAY_LIGHT, GPIO.HIGH))

		GPIO.setup(RELAY_VR_PLUS, GPIO.OUT, initial=GPIO.HIGH)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_VR_PLUS output.", RELAY_VR_PLUS, GPIO.HIGH))
		GPIO.setup(RELAY_VR_MINUS, GPIO.OUT, initial=GPIO.LOW)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_VR_MINUS output.", RELAY_VR_MINUS, GPIO.HIGH))
		self._nextSymbolExpected = self._soluce_list[0]
	
		if 'jack_course_door_forward' in self._config: 
			self._jack_course_door_forward = self._config['jack_course_door_forward'] 
		else:
			self._jack_course_door_forward = JACK_COURSE_DOOR_FORWARD
			
		if 'jack_course_door_backward' in self._config: 
			self._jack_course_door_backward = self._config['jack_course_door_backward'] 
		else:
			self._jack_course_door_backward = JACK_COURSE_DOOR_BACKWARD

		if 'jack_course_stick_forward' in self._config: 
			self._jack_course_stick_forward = self._config['jack_course_stick_forward'] 
		else:
			self._jack_course_stick_forward = JACK_COURSE_STICK_FORWARD

		if 'jack_course_stick_backward' in self._config: 
			self._jack_course_stick_backward = self._config['jack_course_stick_backward'] 
		else:
			self._jack_course_stick_backward = JACK_COURSE_STICK_BACKWARD
			
		self._activated_p  = PropData('activé' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._activated_p )
		self._gagne_p  = PropData('gagné' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._gagne_p )
		self._sequence_p  = PropData('séquence' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._sequence_p )
		self._previous_p  = PropData('précédente' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._previous_p )
		self._solution_p  = PropData('solution' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._solution_p )
		self._jackReset_p  = PropData('magic' ,  str,  self.displayKeys(JACK_RESET.split(" ")),  logger = self._logger)
		self._publishable.append(self._jackReset_p )
		self._jack_p  = PropData('vérin' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_p )
		self._light_p  = PropData('lumière' ,  bool,  "",  logger = self._logger)
		self._publishable.append(self._light_p )

		self._billes_p  = PropData('billes' ,  bool,  "",  logger = self._logger)
		self._publishable.append(self._billes_p )
		
		self._activated_p.update("non")
		self._gagne_p.update("non")
		self._solution_p.update(self.displayKeys(self._soluce_list))
		self._jack_p.update("pause")
		self._light_p.update(GPIO.input(RELAY_LIGHT))
		
		self._jack_course_door_forward_p  = PropData('porte_avant' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_course_door_forward_p )
		self._jack_course_door_backward_p  = PropData('porte_arrière' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_course_door_backward_p )
			
		self._jack_course_stick_forward_p  = PropData('bâton_avant' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_course_stick_forward_p )
		self._jack_course_stick_backward_p  = PropData('bâton_arrière' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_course_stick_backward_p )
		
		self._jack_course_door_forward_p.update(str(self._jack_course_door_forward))
		self._jack_course_door_backward_p.update(str(self._jack_course_door_backward))
		self._jack_course_stick_forward_p.update(str(self._jack_course_stick_forward))
		self._jack_course_stick_backward_p.update(str(self._jack_course_stick_backward))
		
		os.system("amixer cset numid=3 1") # audio jack
		os.system("amixer set 'PCM' -- 400")  # volume maxi

		self.jackBase()
		
		self._publishAllTimerThread.start()
		self._publishChangesTimerThread.start()
		self._samplingTimerThread.start()

	#__________________________________________________________________
	def displayKeys(self, keys):

		p = ""
		i = 0
		for k in keys:
			if i and i % 4 == 0: p = p + "-"	
			p = p + k 
			i = i + 1
		return p

	#__________________________________________________________________
	def playClochette(self):

		try:
			self._wrongSymbolAudioChannel.stop()
			self._wrongSymbolAudioChannel.play(self._wrongSymbolSound)
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to play small bell", str(e)))
		
	#__________________________________________________________________
	def playVerinBaton(self):

		try:
			self._palanAudioChannel.stop()
			self._palanAudioChannel.play(self._palanSound)
			return
			wav = "{}/palan.wav".format(self._keynoteFolder)
			if os.path.isfile(wav):
				pygame.mixer.music.load(wav)
				pygame.mixer.music.set_volume(2.0)
				pygame.mixer.music.play()
			else:
				self._logger.warning("{} : {}".format("Jack door audio file not found", wav))
				self.publishMessage(self._mqttOutbox, "MESG Fichier non trouvé {}".format(wav))	
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to play jack door audio", str(e)))
			
	#__________________________________________________________________
	def playVerinPorte(self):

		try:
			self._palanAudioChannel.stop()
			self._palanAudioChannel.play(self._palanSound)
			return
			wav = "{}/palan.wav".format(self._keynoteFolder)
			if os.path.isfile(wav):
				pygame.mixer.music.load(wav)
				pygame.mixer.music.set_volume(2.0)
				pygame.mixer.music.play()
			else:
				self._logger.warning("{} : {}".format("Jack stick audio file not found", wav))
				self.publishMessage(self._mqttOutbox, "MESG Fichier non trouvé {}".format(wav))	
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to play jack stick audio", str(e)))
			
	#__________________________________________________________________
	def jackBase(self):

		GPIO.output(RELAY_VR_PLUS, GPIO.HIGH)
		GPIO.output(RELAY_VR_MINUS, GPIO.HIGH)		
		self._jack_p.update("en rentrée")
		self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
		if self._jack_p.value() == "porte":
			threading.Timer(self._jack_course_door_backward / 1000.0, self.jackPause).start()
		elif self._jack_p.value() == "bâton":
			threading.Timer(self._jack_course_stick_backward/ 1000.0, self.jackPause).start()
		else:
			threading.Timer(max(self._jack_course_door_backward, self._jack_course_stick_backward) / 1000.0, self.jackPause, ["rentré"]).start()
		
	#__________________________________________________________________
	def jackDoor(self):
		
		if self._jack_course_door_forward > 0 and self._jack_p.value() == "rentré":
			GPIO.output(RELAY_VR_PLUS, GPIO.LOW)
			GPIO.output(RELAY_VR_MINUS, GPIO.LOW)
			self._jack_p.update("en sortie")
			self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
			threading.Timer(self._jack_course_door_forward / 1000.0, self.jackPause, ["porte"]).start()
			threading.Timer((self._jack_course_door_forward + self._jack_course_door_backward) / 1000.0, self.stopAudioVerin).start()
			self._activated_p.update("oui")
			
	#__________________________________________________________________
	def jackManualBackward(self, tempo):
		
		if tempo > 0 and self._jack_p.value() != "en rentrée" and self._jack_p.value() != "en sortie":
			GPIO.output(RELAY_VR_PLUS, GPIO.HIGH)
			GPIO.output(RELAY_VR_MINUS, GPIO.HIGH)		
			self._jack_p.update("en rentrée")
			self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
			threading.Timer(tempo / 1000.0, self.jackPause, ["pause"]).start()

	#__________________________________________________________________
	def jackManualForward(self, tempo):
		
		if tempo > 0 and self._jack_p.value() != "en rentrée" and self._jack_p.value() != "en sortie":
			GPIO.output(RELAY_VR_PLUS, GPIO.LOW)
			GPIO.output(RELAY_VR_MINUS, GPIO.LOW)
			self._jack_p.update("en sortie")
			self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
			threading.Timer(tempo / 1000.0, self.jackPause, ["pause"]).start()
			
	#__________________________________________________________________
	def jackPause(self, state):

		GPIO.output(RELAY_VR_PLUS, GPIO.HIGH)
		GPIO.output(RELAY_VR_MINUS, GPIO.LOW)
		self._jack_p.update(state)
		self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
		if self._jack_p.value() == "porte":
			threading.Timer(0.100, self.jackBase).start()
		#elif self._jack_p.value() == "bâton":
		#	threading.Timer(10.0, self.jackBase).start()
		
	#__________________________________________________________________
	def jackStick(self):

		if self._jack_course_stick_forward > 0 and self._jack_p.value() == "rentré":
			self.playVerinBaton()
			GPIO.output(RELAY_VR_PLUS, GPIO.LOW)
			GPIO.output(RELAY_VR_MINUS, GPIO.LOW)	
			self._jack_p.update("en sortie")
			self.publishMessage(self._mqttOutbox, "OVER Podium" )
			self.publishMessage(self._mqttOutbox, "DATA " + str(self._jack_p) )# accurate jack state
			threading.Timer(self._jack_course_stick_forward / 1000.0, self.jackPause, ["bâton"]).start()
			threading.Timer((self._jack_course_stick_forward) / 1000.0, self.stopAudioVerin).start()

	#__________________________________________________________________ 
	def keyStroke(self, keynote):
		try:
			if len(self._keynote_list) == len(self._soluce_list):
				self._keynote_list.clear()
			if 	self._activated_p.value() == "oui":
				if  self._nextSymbolExpected and self._nextSymbolExpected == keynote:
					self._symboleAudioChannel [keynote] .stop()
					self._symboleAudioChannel [keynote] .play(self._keynoteSound[keynote])
				else:
					self.playClochette()
		except BaseException as e:
			self._logger.error("{} {} : {}".format("Failed to play key stroke", keynote, str(e)))
		try:
			if self._nextSymbolExpected and self._nextSymbolExpected != keynote:
				self._keynote_list.append(keynote)
				self._previous_p.update(self.displayKeys(self._keynote_list) )
				self._keynote_list.clear()
				self._nextSymbolExpected = self._soluce_list[0]
			else:
				self._keynote_list.append(keynote)
				if len(self._keynote_list) == len(self._soluce_list):
					self._previous_p.update(self.displayKeys(self._keynote_list) )				
					self._nextSymbolExpected = self._soluce_list[0]
				else:
					self._nextSymbolExpected = self._soluce_list[len(self._keynote_list) ]
			self._sequence_p.update(self.displayKeys(self._keynote_list) )
			if self._gagne_p.value() ==  "non" and SOLUCE == " ".join(self._keynote_list):
				self._gagne_p.update("oui")
				self._activated_p.update("non")
				self.jackStick()
			elif self._gagne_p.value() ==  "oui" and JACK_RESET == " ".join(self._keynote_list):
				self.jackBase()
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to process key stroke", str(e)))
	
	#__________________________________________________________________
	def loadSound(self):
		
		self._keynoteFolder = AUDIO
			
		for k in KEY_SYMBOLS:
			self._keynoteSound[k] = pygame.mixer.Sound("{}/bol_thibetain.wav".format(self._keynoteFolder))
			self._keynoteSound[k] .set_volume(0.4)
			
		self._wrongSymbolSound = pygame.mixer.Sound("{}/clochette.wav".format(self._keynoteFolder))
		self._wrongSymbolSound.set_volume(1.0)

		self._palanSound = pygame.mixer.Sound("{}/palan.wav".format(self._keynoteFolder))
		self._palanSound.set_volume(1.0)
		
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
		#print(topic, message)
		if message == "app:startup":
			pass
		elif message == "app:data":
			super.publishAllData()
			self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("setup:1"):
			try:
				m = re.findall(self._setupRegex, message)
				if m:
					for d in m:
						var, s = d
						print(var, s)
						if var == "porte_avant":
							self._jack_course_door_forward = int(s)
							self._config['jack_course_door_forward'] = self._jack_course_door_forward	
							self._jack_course_door_forward_p.update(str(self._jack_course_door_forward))
						if var == "porte_arrière":
							self._jack_course_door_backward = int(s)
							self._config['jack_course_door_backward'] = self._jack_course_door_backward	
							self._jack_course_door_backward_p.update(str(self._jack_course_door_backward))
						if var == "bâton_avant":
							self._jack_course_stick_forward = int(s)
							self._config['jack_course_stick_forward'] = self._jack_course_stick_forward	
							self._jack_course_stick_forward_p.update(str(self._jack_course_stick_forward))
						if var == "bâton_arrière":
							self._jack_course_stick_backward = int(s)
							self._config['jack_course_stick_backward'] = self._jack_course_stick_backward	
							self._jack_course_stick_backward_p.update(str(self._jack_course_stick_backward))
			except Exception as e:
				self._logger.debug(e)
				self.publishMessage(self._mqttOutbox, "MESG " + message +"-->" + e)
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			#super()._publishDataChanges()
			with open(CONFIG_FILE, 'w') as conffile:
				yaml.dump(self._config, conffile, default_flow_style = False)
			#print(self._config)
		elif message.startswith("gagner:"):
			if message.endswith(":0"):
				self._gagne_p.update("non")
				self._activated_p.update("non")
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._gagne_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":1"):
				self._gagne_p.update("oui")	
				self._activated_p.update("non")
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._gagne_p) )# accurate flip/flop
				self.jackStick()
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("billes-lumière:"):
			if message.endswith(":0"):
				GPIO.output(RELAY_JEU_DES_BILLES, GPIO.HIGH)
				self._billes_p.update(GPIO.input(RELAY_JEU_DES_BILLES))
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._billes_p) )
				time.sleep(0.5)
			else:
				time.sleep(0.5)
				GPIO.output(RELAY_JEU_DES_BILLES, GPIO.LOW)
				self._billes_p.update(GPIO.input(RELAY_JEU_DES_BILLES))
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._billes_p) )
			self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("lumière:"):
			if message.endswith(":0"):
				GPIO.output(RELAY_LIGHT, GPIO.LOW)
			else:
				GPIO.output(RELAY_LIGHT, GPIO.HIGH)
			self._light_p.update(GPIO.input(RELAY_LIGHT))
			self.publishMessage(self._mqttOutbox, "DATA " + str(self._light_p) )
			self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("vérin:"):
			if message.endswith(":retour"):
				self.jackBase()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif self._jack_p.value() != "rentré":
				self.publishMessage(self._mqttOutbox, "OMIT " + message+ " vérin non rentré")				
			elif self._jack_p.value() == "en rentrée" or  self._jack_p.value() == "en sortie":
				self.publishMessage(self._mqttOutbox, "OMIT " + message+ " vérin en mouvement")				
			elif message.endswith(":porte"):
				self.playVerinPorte()
				threading.Timer(JACK_COURSE_DOOR_PREAUDIO / 1000.0, self.jackDoor).start()
				GPIO.output(RELAY_LIGHT, GPIO.HIGH)
				self._light_p.update(GPIO.input(RELAY_LIGHT))
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._light_p) )
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":bâton"):
				self.jackStick()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("jouer:bol"):
				self._symboleAudioChannel ["A"] .stop()
				self._symboleAudioChannel ["A"] .play(self._keynoteSound["A"])
				self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("jouer:clochette"):
				self.playClochette()
				self.publishMessage(self._mqttOutbox, "DONE " + message)
		elif message.startswith("rentrer:"):
			m = re.match(r'rentrer:(\d+)', message)
			if m:
				tempo = int(m.group(1).strip())
				self.jackManualBackward(tempo)
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)				
		elif message.startswith("sortir:"):
			m = re.match(r'sortir:(\d+)', message)
			if m:
				tempo = int(m.group(1).strip())
				self.jackManualForward(tempo)
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)	
		else:
			m = re.match(r'jouer:(.+)', message)
			if m:
				keynote= m.group(1).strip()
				self.keyStroke(keynote)
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)

	#__________________________________________________________________
	def publishAllData(self):
		
		while True:
			try:
				super()._publishAllData()
			except:
				pass
			finally:
				time.sleep(3)

	#__________________________________________________________________
	def publishDataChanges(self):

		while True:
			try:
				super()._publishDataChanges()
			except:
				pass
			finally:
				time.sleep(30)		
	
	#__________________________________________________________________
	def samplingKeynotes(self):

		while True:
			try:
				
				for gpio in self._keynotesSampler:
					
					self._keynotesSampler[gpio].insert(0, GPIO.input(gpio))
					self._keynotesSampler[gpio].pop()
					
					lev = sum(self._keynotesSampler[gpio])
					
					if lev  <= SAMPLING_TOLERANCE:
						# pin LOW
						if gpio not in self._keynotesDown:
							# fire key pressed !
							#self._logger.info("{} {}".format("KEY FIRED", self._keynotesReversed[gpio]))
							self.keyStroke(self._keynotesReversed[gpio])
							self._keynotesDown.append(gpio)
					elif lev >= (SAMPLING_SIZE - SAMPLING_TOLERANCE):
						# pin HIGH
						if gpio in self._keynotesDown:
							# fire key released !
							self._keynotesDown.remove(gpio)
										
			except:
				pass
			
			finally:
				time.sleep(SAMPLING_INTERVAL)

	#__________________________________________________________________
	def stopAudioVerin(self):
		
		try:
			self._palanAudioChannel.stop()
			return
			#pygame.mixer.music.fadeout(100)  # blocks until the music has faded out
			pygame.mixer.music.stop() 
		except:
			pass
				
