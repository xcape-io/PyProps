#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "Crying Doll"

PYPROPS_CORELIBPATH = '../../core'

PUBLISHALLDATA_PERIOD = 30.0
PUBLISHDATACHANGES_PERIOD = 1.0

USE_GPIO = True

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 2

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by CryingDollApp

GPIO_RELAY_LIGHT = 16
GPIO_VIBRATION_SENSORS = [20, 21]

AUDIO_CRYING = [
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/1.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/2.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/3.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/4.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/5.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/6.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProps/PyCryingDollProps/audio/7.wav"]

