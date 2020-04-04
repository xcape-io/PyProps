#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
teletext.py (version 0.1)

Kivy app to display clues on TV (HDMI) with Raspberry.

usage: python3 teletext.py  [-- [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]]

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

import os, sys,  uuid

#os.environ['KIVY_AUDIO'] = 'sdl2'  # mandatory if using jack audio

from TeletextApp import TeletextApp

import paho.mqtt.client as mqtt

from Singleton import Singleton, SingletonException

me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)
	
os.chdir('/home/pi/Room/Puits')

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = TeletextApp(mqtt_client, debugging_mqtt=False)
app.run()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
del(me)
