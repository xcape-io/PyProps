#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

Main script for GuizeroProps.

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
"""

import os
import sys
import uuid

import paho.mqtt.client as mqtt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = TeletextApp(sys.argv, mqtt_client, debugging_mqtt=False)

# guizero event loop
app.loop()

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.cleanup()

try:
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
except:
    pass

del (me)

sys.exit(0)
