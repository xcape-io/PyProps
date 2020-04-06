#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
main.py

Main script for AsyncioProps.

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

import asyncio
import os
import platform
import signal
import sys
import uuid

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from constants import *

try:
    PYPROPS_CORELIBPATH
    sys.path.append(PYPROPS_CORELIBPATH)
except NameError:
    pass

from BlinkEchoApp import BlinkEchoApp
from Singleton import Singleton, SingletonException

me = None
try:
    me = Singleton()
except SingletonException:
    sys.exit(-1)
except BaseException as e:
    print(e)

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = BlinkEchoApp(sys.argv, mqtt_client, debugging_mqtt=False)

if app.logger:
    app.logger.info("Program started")

loop = asyncio.get_event_loop()

# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, loop.stop)
signal.signal(signal.SIGINT, loop.stop)
if platform.system() != 'Windows':
    signal.signal(signal.SIGHUP, loop.stop)
    signal.signal(signal.SIGQUIT, loop.stop)

# Periodic actions
for title, (func, time) in app.periodicActions.items():
    loop.create_task(func(time))
    app.logger.info("Periodic task created '{0}' every {1} seconds".format(title, time))

loop.run_forever()
loop.close()

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.cleanup()

try:
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
except:
    pass

if app.logger:
    app.logger.info("Program done")

del (me)

sys.exit(0)
