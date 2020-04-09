#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
main.py

usage: python3 main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
'''

import paho.mqtt.client as mqtt
import os, sys, platform, signal, uuid
import time

from constants import *
from PianoApp import PianoApp
from Singleton import Singleton, SingletonException

import RPi.GPIO as GPIO

import pygame
pygame.mixer.pre_init(44100, -16, 1, 4096)
pygame.init()
pygame.mixer.init()

me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)
	
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# translation
import gettext
try:
 gettext.find(APPLICATION)
 traduction = gettext.translation(APPLICATION, localedir='locale', languages=['fr'])
 traduction.install()
except:
 _ = gettext.gettext # cool, this hides PyLint warning Undefined name '_'

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

sketch = PianoApp(sys.argv, mqtt_client, debugging_mqtt=False)

if sketch._logger:
	sketch._logger.info(_("Program started"))

done= False	
def quit(a,b):
	global done
	done = True
	
# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, quit)
signal.signal(signal.SIGINT, quit)
if platform.system() != 'Windows':
	signal.signal(signal.SIGHUP, quit)
	signal.signal(signal.SIGQUIT, quit)

if sketch._logger:
	if os.path.isfile('/opt/vc/include/bcm_host.h'):
		sketch._logger.info(_("Program running on Raspberry Pi"))
	elif platform.system() == 'Windows':
		sketch._logger.info(_("Program running on Windows"))


clock = pygame.time.Clock()

while True:
	#time.sleep(5e-3)
	#clock.tick(30)
	time.sleep(50e-3)
	clock.tick(10)
	if done:
		break

GPIO.cleanup()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
if sketch._logger:
	sketch._logger.info(_("Program done"))

del(me)
print(_("\nDone"))
sys.exit(0)
