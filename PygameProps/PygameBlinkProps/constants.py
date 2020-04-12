#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "PygameBlink"

PYPROPS_CORELIBPATH = '../../core'

USE_GPIO = True

#__________________________________________________________________
# Required by PropsApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 0  # usually 2 but client blocks is packet loiss so try 1 (maybe 0 like Yun is safer)

# try 5 seconds cause of wifi
MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by BlinkApp
CHALLENGE = "Podium"

PUBLISHALLDATA_PERIOD = 30.0
PUBLISHDATACHANGES_PERIOD = 3.0

GPIO_BLINKING_LED = 20

