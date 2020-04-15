#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PianoApp.py (version 0.1 initial)

PianoApp extends PropsApp.

'''

from constants import *

from PropsApp import PropsApp
from PropsData import PropsData

import os, re, threading, time
if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
	import RPi.GPIO as GPIO

import pygame
		
class PianoApp(PropsApp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)

		
		self._config_p  = PropsData('configuration' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._config_p )
		self._gagne_p  = PropsData('gagné' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._gagne_p )
		self._sequence_p  = PropsData('séquence' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._sequence_p )
		self._solution_p  = PropsData('solution' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._solution_p )
		self._jackReset_p  = PropsData('magic' ,  str,  self.frenchKeys(JACK_RESET.split(" ")),  logger = self._logger)
		self._publishable.append(self._jackReset_p )
		self._jack_p  = PropsData('vérin' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._jack_p )
		self._latch_p  = PropsData('piano' ,  str,  "",  logger = self._logger)
		self._publishable.append(self._latch_p )

		self._keynote_list = []
		self._keynotesDown = []
		self._keynotesReversed = {}
		self._keynotesSampler = {}
		self._keynoteFolder = AUDIO_FRENCH
		self._keynoteAudioChannel = {}
		self._keynoteSound = {}
				
		self._publishAllTimerThread = threading.Thread()
		self._publishAllTimerThread = threading.Thread(target=self.publishAllData)
		self._publishAllTimerThread.daemon = True
		
		self._publishChangesTimerThread = threading.Thread()
		self._publishChangesTimerThread = threading.Thread(target=self.publishDataChanges)
		self._publishChangesTimerThread.daemon = True
		
		self._samplingTimerThread = threading.Thread()
		self._samplingTimerThread = threading.Thread(target=self.samplingKeynotes)
		self._samplingTimerThread.daemon = True
		
		pygame.mixer.set_num_channels(len(KEY_NOTES))
		pygame.mixer.set_reserved(len(KEY_NOTES) + 4)
		i = 0
		for k in KEY_NOTES:
			self._keynoteAudioChannel [k] = pygame.mixer.Channel(i)
			i = i + 1

		self.loadSound(self._config_p.value())
					
		''' Interrupt bouncetime is correct at 200ms (but inputs too noisy)
		   so we go for sampling at high rate'''
		   
		for k in KEY_NOTES:
			gpio = KEY_NOTES[k]
			self._keynotesReversed [gpio] = k
			self._keynotesSampler[gpio] = [1] * SAMPLING_SIZE # pulled-up
			# GPIO ports set up as inputs, pulled up to avoid false detection. 
			# Keynote ports are wired to connect to GND on action  
			GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
			self._logger.info("{} {} {}{}".format("GPIO: setup",  k, "input pulled-up.", gpio))
					
		GPIO.setup(RELAY_VR_PLUS, GPIO.OUT, initial=GPIO.HIGH)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_VR_PLUS output.", RELAY_VR_PLUS, GPIO.HIGH))
		GPIO.setup(RELAY_VR_MINUS, GPIO.OUT, initial=GPIO.LOW)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_VR_MINUS output.", RELAY_VR_PLUS, GPIO.HIGH))
		GPIO.setup(RELAY_LATCH, GPIO.OUT, initial=GPIO.HIGH)
		self._logger.info("{}{} = {}".format("GPIO: setup RELAY_LATCH output.", RELAY_VR_PLUS, GPIO.HIGH))
		
		self._config_p.update("Français")
		self._gagne_p.update("non")
		self._solution_p.update(self.frenchKeys(SOLUCE.split()))
		self._jack_p.update("pause")
		self._latch_p.update("fermé")
		
		os.system("amixer cset numid=3 1") # audio jack
		os.system("amixer set 'PCM' -- -100") # volume -3dB

		self._publishAllTimerThread.start()
		self._publishChangesTimerThread.start()
		self._samplingTimerThread.start()

	#__________________________________________________________________
	def playFinalAudio(self):

		try:
			keynote_folder = AUDIO_FRENCH
			if self._config_p.value() == "Anglais":
				keynote_folder = AUDIO_ENGLISH
			elif self._config_p.value() == "Français":
				keynote_folder = AUDIO_FRENCH			
			elif self._config_p.value() == "Enfants":
				keynote_folder = AUDIO_KIDS
			wav = "{}/final.wav".format(keynote_folder)
			if os.path.isfile(wav):
				pygame.mixer.music.load(wav)
				pygame.mixer.music.set_volume(0.85)
				pygame.mixer.music.play()
			else:
				self._logger.warning("{} : {}".format("Final file not found", wav))
				self.publishMessage(self._mqttOutbox, "MESG Fichier non trouvé {}".format(wav))	
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to play final", str(e)))
		finally:
			self.publishMessage(self._mqttOutbox, "OVER {}".format(CHALLENGE))	

	#__________________________________________________________________
	def playSolutionAudio(self):

		try:
			keynote_folder = AUDIO_FRENCH
			if self._config_p.value() == "Anglais":
				keynote_folder = AUDIO_ENGLISH
			elif self._config_p.value() == "Français":
				keynote_folder = AUDIO_FRENCH			
			elif self._config_p.value() == "Enfants":
				keynote_folder = AUDIO_KIDS
			wav = "{}/solution.wav".format(keynote_folder)
			if os.path.isfile(wav):
				pygame.mixer.music.load(wav)
				pygame.mixer.music.play()
			else:
				self._logger.warning("{} : {}".format("Final file not found", wav))
				self.publishMessage(self._mqttOutbox, "MESG Fichier non trouvé {}".format(wav))	
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to play final", str(e)))

	#__________________________________________________________________
	def frenchKeys(self, keys):

		p = ""
		for k in keys:
			try:
				if p: p = p + " "
				p = p + KEY_FRENCH[k]
			except:
				p = p + "\u2669\u266f"
		return p
		
	#__________________________________________________________________
	def jackDown(self):

		self.latchOff()
		GPIO.output(RELAY_VR_PLUS, GPIO.HIGH)
		GPIO.output(RELAY_VR_MINUS, GPIO.HIGH)		
		threading.Timer(JACK_COURSE, self.jackPause).start()
		threading.Timer(JACK_COURSE, self.latchOn).start()
		self._jack_p.update("descente")
		self._logger.info("Jack: DOWN")
	
	#__________________________________________________________________
	def jackPause(self):

		GPIO.output(RELAY_VR_PLUS, GPIO.HIGH)
		GPIO.output(RELAY_VR_MINUS, GPIO.LOW)
		self._jack_p.update("pause")
		self._logger.info("Jack: PAUSE")
	
	#__________________________________________________________________
	def jackUp(self):
		
		self.latchOff()
		GPIO.output(RELAY_VR_PLUS, GPIO.LOW)
		GPIO.output(RELAY_VR_MINUS, GPIO.LOW)	
		threading.Timer(JACK_COURSE, self.jackPause).start()
		self._jack_p.update("montée")
		self._logger.info("Jack: UP")

	#__________________________________________________________________ 
	def keyStroke(self, keynote):
		try:
			self._keynoteAudioChannel [keynote] .stop()
			self._keynoteAudioChannel [keynote] .play(self._keynoteSound[keynote])
		except BaseException as e:
			self._logger.error("{} {} : {}".format("Failed to play key stroke", keynote, str(e)))
		try:
			if '#' in keynote:
				self._keynote_list.append(keynote)
				#self._keynote_list.append('#') # patch2
			else:
				self._keynote_list.append(keynote)
			#patch (better anyway)
			#if len(self._keynote_list) > (len(SOLUCE) / 2 + 1):
			if len(self._keynote_list) > (SOLUCE.count(' ') + 1):
				self._keynote_list.pop(0)
			self._sequence_p.update(self.frenchKeys(self._keynote_list) )
			if self._gagne_p.value() ==  "non" and SOLUCE == " ".join(self._keynote_list):
				self._gagne_p.update("oui")
				threading.Timer(1.200, self.playFinalAudio).start()
				threading.Timer(3, self.jackUp).start()
			elif self._gagne_p.value() ==  "oui" and JACK_RESET == " ".join(self._keynote_list):
				self.jackDown()
		except BaseException as e:
			self._logger.error("{} : {}".format("Failed to process key stroke", str(e)))
			
	#__________________________________________________________________
	def latchOff(self):

		GPIO.output(RELAY_LATCH, GPIO.LOW)
		self._latch_p.update("ouvert")
		self._logger.info("Latch: OFF (open)")
	
	#__________________________________________________________________
	def latchOn(self):
		
		GPIO.output(RELAY_LATCH, GPIO.HIGH)
		self._latch_p.update("fermé")
		self._logger.info("Latch: ON (close)")
	
	#__________________________________________________________________
	def loadSound(self, config):
		
		self._keynoteFolder = AUDIO_FRENCH
		if self._config_p.value() == "Anglais":
			self._keynoteFolder  = AUDIO_ENGLISH
		elif self._config_p.value() == "Français":
			self._keynoteFolder  = AUDIO_FRENCH			
		elif self._config_p.value() == "Enfants":
			self._keynoteFolder  = AUDIO_KIDS
			
		for k in KEY_NOTES:
			self._keynoteSound[k] = pygame.mixer.Sound("{}/{}.wav".format(self._keynoteFolder, k))
			if k.endswith('#'):
				self._keynoteSound[k].set_volume(0.8)
			#patch
			
			#if k == 'A#':			
			#patch2
			#if '#' in k:			
			#	self._keynoteSound[k] = pygame.mixer.Sound("{}/{}.wav".format(self._keynoteFolder, 'B'))

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
		elif message in ["Anglais", "Français", "Enfants"]:
			self._config_p.update(message)
			self.loadSound(self._config_p.value())
			self.publishMessage(self._mqttOutbox, "DONE " + message)	
		elif message.startswith("gagner:"):
			if message.endswith(":0"):
				self._gagne_p.update("non")
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._gagne_p) )# accurate flip/flop
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":1"):
				self._gagne_p.update("oui")	
				self.publishMessage(self._mqttOutbox, "DATA " + str(self._gagne_p) )# accurate flip/flop
				threading.Timer(1.200, self.playFinalAudio).start()
				threading.Timer(3, self.jackUp).start()
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("vérin:"):
			if self._jack_p.value() != "pause":
				self.publishMessage(self._mqttOutbox, "OMIT " + message+ " vérin en mouvement")				
			elif message.endswith(":descendre"):
				self.jackDown()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":monter"):
				self.jackUp()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("piano:"):
			if message.endswith(":ouvrir"):
				self.latchOff()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":fermer"):
				self.latchOn()		
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("thème:"):
			if message.endswith(":démarrer"):
				wav = "{}/{}.wav".format("/home/pi/Room/Piano/audio/melodies", "theme_exorcist")
				if os.path.isfile(wav):
					pygame.mixer.music.load(wav)
					pygame.mixer.music.play()
				else:
					self._logger.warning("{} : {}".format("Melody file not found", wav))
					self.publishMessage(self._mqttOutbox, "MESG Fichier non trouvé {}".format(wav))	
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			elif message.endswith(":arrêter"):
				pygame.mixer.music.stop()
				self.publishMessage(self._mqttOutbox, "DONE " + message)
			else:
				self.publishMessage(self._mqttOutbox, "OMIT " + message)
		elif message.startswith("jouer:solution"):
				self.playSolutionAudio()
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
