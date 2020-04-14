#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "educational"

QTGUI = False # optional

PYPROPS_CORELIBPATH = '../../core'

PUBLISHALLDATA_PERIOD = 10.0

USE_GPIO = True

NFC_MODULE = None # or 'SPI' or 'Hat'

#__________________________________________________________________
# Required by MqttConsoleApp
ORGANIZATIONDOMAIN = "xcape.io"
ORGANIZATIONNAME = "xcape.io"

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by EducationalApp
GPIO_BLINKING_LED = 16
