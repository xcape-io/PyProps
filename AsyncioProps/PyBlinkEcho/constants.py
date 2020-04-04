#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the application constants. As a rule all constants are named in all caps.
"""

APPLICATION = "Echo"

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by PropsApp
BLANK_ECHO = '---'
