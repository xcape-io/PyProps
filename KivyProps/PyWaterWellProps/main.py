#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
main.py (version 0.1)

Kivy app to display clues with graphics effects on TV (HDMI) with Raspberry.

usage: python3 main.py  [-- [-h] [-d] ]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           set DEBUG log level
'''

import os
import sys
import uuid

import paho.mqtt.client as mqtt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.environ['KIVY_AUDIO'] = 'sdl2'  # mandatory if using jack audio

from constants import *

try:
    PYPROPS_CORELIBPATH
    sys.path.append(PYPROPS_CORELIBPATH)
except NameError:
    pass

from TeletextApp import TeletextApp
from Singleton import Singleton, SingletonException

me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)


mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = TeletextApp(mqtt_client, debugging_mqtt=False)
app.run()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
del(me)
