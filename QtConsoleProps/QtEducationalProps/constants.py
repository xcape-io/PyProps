#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "educational"

PYPROPS_CORELIBPATH = '../../core'

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
'''
Data changes sent every SKETCH_INTERVAL_DATA
full data sent at least SKETCH_INTERVAL_DATA * SKETCH_DATA_COUNT
'''
SKETCH_INTERVAL_AUTOMATION = 500 # milliseconds
SKETCH_INTERVAL_DATA = 1000 # milliseconds
SKETCH_DATA_COUNT = 30 # for 30 seconds

#__________________________________________________________________
# Required by EducationalApp
DISPLAY_ON_TIME = 800 # milliseconds
DISPLAY_OFF_TIME = 400
GARLAND_ON_TIME = 350
GARLAND_OFF_TIME = 100
ON = 1
OFF = 0
'''
	 F  E  D  C  B  A
	 -  -  -  -  -  -  -  -
 1 | A  B  C  D  E  F  
 2 | G  H  I  J  K  L   
 3 | M  N  O  P  Q  R  
 4 | S  T  U  V  W  X
 5 | Y  Z  0  1  2  3
 6 | 4  5  5  7  8  9
   |	
   |		
'''
RELAYS = {	'A' : ('F',1) , 'B' : ('E',1) , 'C' : ('D',1) , 'D' : ('C',1) , 'E' : ('B',1) , 'F' : ('A',1) , 
			'G' : ('F',2) , 'H' : ('E',2) , 'I' : ('D',2) , 'J' : ('C',2) , 'K' : ('B',2) , 'L' : ('A',2) , 
			'M' : ('F',3) , 'N' : ('E',3) , 'O' : ('D',3) , 'P' : ('C',3) , 'Q' : ('B',3) , 'R' : ('A',3) , 
			'S' : ('F',4) , 'T' : ('E',4) , 'U' : ('D',4) , 'V' : ('C',4) , 'W' : ('B',4) , 'X' : ('A',4) , 
			'Y' : ('F',5) , 'Z' : ('E',5) , '0' : ('D',5) , '1' : ('C',5) , '2' : ('B',5) , '3' : ('A',5) , 
			'4' : ('F',6) , '5' : ('E',6) , '6' : ('D',6) , '7' : ('C',6) , '8' : ('B',6) , '9' : ('A',6) }
			
RELAYS_ALPHA = {
	'A' : 4,
	'B' : 17,
	'C' : 27,
	'D' : 22,
	'E' : 23, #26,
	'F' : 24, #19
	}
	
RELAYS_NUMER = {
	1 : 13,
	2 : 6,
	3 : 5,
	4 : 16, #21,
	5 : 20,
	6 : 21 #16
	}

PIRELAY_INBOX = 'Live/Demeure/Raspberry Relais/inbox'
