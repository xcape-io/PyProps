#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
alphabet.py

Automation sketch to fire LEDs to display clue words.

usage: python3 alphabet.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
'''

from PyQt5.QtCore import QUuid

import paho.mqtt.client as mqtt
import os, sys, platform, signal

from constants import *
from AlphabetApp import AlphabetApp
from Singleton import Singleton, SingletonException

me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)
	
os.chdir(os.path.dirname(os.path.abspath(__file__)))

clientid = MQTT_CLIENTID_PREFIX + QUuid.createUuid().toString()

mqtt_client = mqtt.Client(clientid, clean_session=True, userdata=None)

sketch = AlphabetApp(sys.argv, mqtt_client, debugging_mqtt=False, gpio_bcm=True, no_gpio=False)

if sketch._logger:
	sketch._logger.info(sketch.tr("Sketch started"))

# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, sketch.quit)
signal.signal(signal.SIGINT, sketch.quit)
if platform.system() != 'Windows':
	signal.signal(signal.SIGHUP, sketch.quit)
	signal.signal(signal.SIGQUIT, sketch.quit)

sketch.start()

if sketch._logger:
	raspberryPi = sketch.raspberryPiVersion()
	if raspberryPi:
		sketch._logger.info("{0} {1}".format(sketch.tr("Sketch running on Raspberry Pi"), raspberryPi))
	elif platform.system() == 'Windows':
		sketch._logger.info(sketch.tr("Sketch running on Windows"))

rc = sketch.exec_()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
if sketch._logger:
	sketch._logger.info(sketch.tr("Sketch done"))

del(me)

sys.exit(rc)
