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

import os
import platform
import signal
import sys
import time
import uuid
import paho.mqtt.client as mqtt
import pygame

from constants import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from constants import *

try:
    PYPROPS_CORELIBPATH
    sys.path.append(PYPROPS_CORELIBPATH)
except NameError:
    pass

from PianoApp import PianoApp
from Singleton import Singleton, SingletonException

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

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

sketch = PianoApp(sys.argv, mqtt_client, debugging_mqtt=False)

done = False

# Assign handler for process exit (shows not effect on Windows in debug here)
def quit(a, b):
    global done
    done = True

signal.signal(signal.SIGTERM, quit)
signal.signal(signal.SIGINT, quit)
if platform.system() != 'Windows':
    signal.signal(signal.SIGHUP, quit)
    signal.signal(signal.SIGQUIT, quit)

clock = pygame.time.Clock()

try:
    while True:
        # time.sleep(5e-3)
        # clock.tick(30)
        time.sleep(75e-3)
        clock.tick(25)
        # time.sleep(30e-3)
        # clock.tick(20)
        if done:
            break
except:
    pass
finally:
    try:
        if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
            GPIO.cleanup()
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
    except:
        pass

del(me)
sys.exit(0)
