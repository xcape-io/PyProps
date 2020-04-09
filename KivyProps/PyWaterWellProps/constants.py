#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''


APPLICATION = "Water Well"
PYPROPS_CORELIBPATH = '../../core'

PUBLISHALLDATA_PERIOD = 30.0

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by TeletextApp
#import os
#FONT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/fonts"

MQTT_DISPLAY_TOPIC = 'Room/My room/Props/Raspberry WaterWell/display'