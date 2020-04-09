#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "Podium"

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 0  # usually 2 but client blocks is packet loiss so try 1 (maybe 0 like Yun is safer)

# try 5 seconds cause of wifi
MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by PodiumApp
CHALLENGE = "Podium"

''' GPIO symbol keys '''
KEY_SYMBOLS = {
	'A' : 16,
	'B' : 20,
	'C' : 5,
	'D' : 6,
	'E' : 13,
	'F' : 19,
	}
	
''' Audio files '''
import os
AUDIO = os.path.dirname(os.path.abspath(__file__)) + "/audio"

''' Sampling: 20 10 2 for sampling every 20 milliseconds, positive if 8 for 10 values'''
SAMPLING_INTERVAL = 20e-3
SAMPLING_SIZE = 4
SAMPLING_TOLERANCE = 3

RELAY_JEU_DES_BILLES = 21 # lumière et gâche, en NO pour ne pas décoller la porte au reboot
RELAY_LIGHT = 22 

''' GPIO jack '''
RELAY_VR_PLUS = 17
RELAY_VR_MINUS = 27
JACK_COURSE_DOOR_PREAUDIO = 7000
JACK_COURSE_DOOR_FORWARD = 3000
JACK_COURSE_DOOR_BACKWARD = JACK_COURSE_DOOR_FORWARD + 1000
JACK_COURSE_STICK_FORWARD = 6000
JACK_COURSE_STICK_BACKWARD = JACK_COURSE_STICK_FORWARD + 1000
JACK_RESET = "A A A A B B B B C C C C" # 12 keys like soluce

SOLUCE = "E D C A E D A F F B C E"

