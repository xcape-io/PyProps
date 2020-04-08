#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
minimal.py (version 0.1)

Minimal Kivy app for Raspberry.

usage: python3 minimal.py  [-- [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
'''

from MinimalApp import MinimalApp

import paho.mqtt.client as mqtt
import uuid

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = MinimalApp(mqtt_client, debugging_mqtt=False)
app.run()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
