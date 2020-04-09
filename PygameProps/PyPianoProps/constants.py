#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "Piano"

PYPROPS_CORELIBPATH = '../../core'

#__________________________________________________________________
# Required by PropsApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 2

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by PianoApp
CHALLENGE = "Piano"

''' GPIO music keys '''
KEY_NOTES = {
	'A' : 5,
	'B' : 6,
	'C' : 13,
	'D' : 16,
	'E' : 19,
	'F' : 20,
	'G' : 21,
	'A#' : 17,
	'C#' : 22,
	'D#' : 23,
	'F#' : 24,
	'G#' : 27
	}
	
''' French music keys '''
KEY_FRENCH = {
	'A' : 'La',
	'B' : 'Si',
	'C' : 'Do',
	'D' : 'Ré',
	'E' : 'Mi',
	'F' : 'Fa',
	'G' : 'Sol',
	'A#' : 'La#',
	'C#' : 'Do#',
	'D#' : 'Ré#',
	'F#' : 'Fa#',
	'G#' : 'Sol#'
	}
	
''' Audio files '''
import os
AUDIO_ENGLISH = os.path.dirname(os.path.abspath(__file__)) + "/audio/english"
AUDIO_FRENCH = os.path.dirname(os.path.abspath(__file__)) + "/audio/french"
AUDIO_KIDS = os.path.dirname(os.path.abspath(__file__)) + "/audio/kids"

''' Sampling: 20 10 2 for sampling every 20 milliseconds, positive if 8 for 10 values'''
SAMPLING_INTERVAL = 20e-3
SAMPLING_SIZE = 4
SAMPLING_TOLERANCE = 3

''' GPIO jack and latch '''
RELAY_VR_PLUS = 25
RELAY_VR_MINUS = 26
RELAY_LATCH = 12
JACK_COURSE = 8.0 # seconds to move the jack (course is about 6 seconds)
JACK_RESET = "C# G# D# F# C# G# D#" # 7 keys like soluce
#patch2
#JACK_RESET = "# # # # # # #" # 7 keys like soluce

SOLUCE = "D G F A C B E"
#patch
#SOLUCE = "D G F A C A# E"
#patch2
#SOLUCE = "D G F A C # E"
