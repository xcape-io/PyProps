#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the application constants. As a rule all constants are named in all caps.
"""

APPLICATION = "Blink Echo"

PYPROPS_CORELIBPATH = '../../core'

PUBLISHALLDATA_PERIOD = 30.0

USE_GPIO = True

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by BlinkEchoApp
BLANK_ECHO = '---'

GPIO_BLINKING_LED = 16
