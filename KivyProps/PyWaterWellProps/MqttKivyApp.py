#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
MqttKivyApp.py (version 0.1 initial)

Base class for Kivy application with MQTT inbox/outbox.

usage: python3 script.py  [-- [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file (default ./logging.ini)

To switch MQTT broker, kill the program and start again with new arguments.

Kivy:
------
An application can be built if you return a widget on build(), or if you set
self.root.

pip:
-----
$ sudo pip3 install pyaml

Config:
----------
- in constants.py
APPLICATIONNAME = 
CONFIG_FILE = 
MQTT_DEFAULT_HOST =
MQTT_DEFAULT_PORT = 
MQTT_DEFAULT_QoS = 
- in definitions.ini
[mqtt]
sketch-inbox = 
sketch-outbox = 
mqtt-sub-room-language = 

Extend:
------------
- build(self)
- onMessage(self, topic, message):
'''

from constants import *

import gettext
try:
    gettext.find("MqttKivyApp")
    traduction = gettext.translation('MqttKivyApp', localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext # cool, this hides PyLint warning Undefined name '_'

import kivy
kivy.require('1.1.11')

from kivy.app import App
from kivy.uix.button import Button

import configparser, codecs, yaml
import logging, logging.config
import argparse
import os

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

def _is_rpi():
		return exists('/opt/vc/include/bcm_host.h')
		
class MqttKivyApp(App):

	#__________________________________________________________________
	def __init__(self, client, debugging_mqtt=False, **kwargs):

		super(MqttKivyApp, self).__init__(**kwargs)
		
		self._config = {}
		self._definitions = {}
		self._mqttSubscriptions = []
		self._mqttInbox = None
		self._mqttOutbox = None
		self._mqttServerHost = MQTT_DEFAULT_HOST
		self._mqttServerPort = MQTT_DEFAULT_PORT

		ini = 'definitions.ini'
		if os.path.isfile(ini):
			self.config = configparser.ConfigParser()
			self.config.readfp(codecs.open(ini, 'r', 'utf8'))
			if "mqtt" in self.config.sections():
				for key in self.config.options("mqtt"):
					self._definitions[key] = self.config.get("mqtt", key)
					if key.startswith('mqtt-sub-'):
						self._mqttSubscriptions.append(self._definitions[key])
					if key == 'sketch-inbox':
						self._mqttInbox = self._definitions[key]
						self._mqttSubscriptions.append(self._mqttInbox)				
					if key == 'sketch-outbox':
						self._mqttOutbox = self._definitions[key]			

		if os.path.isfile(CONFIG_FILE):
			with open(CONFIG_FILE, 'r') as conffile:
				self._config = yaml.load(conffile)
		else:
			self._config =  {}
		
		print('Config:', self._config)
		
		self._mqttClient = client
		self._mqttConnected = False
		if 'host' in self._config: 
			self._mqttServerHost = self._config['host'] 
		if 'port' in self._config: 
			self._mqttServerPort = self._config['port'] 

		self._mqttClient.on_connect = self.mqttOnConnect
		self._mqttClient.on_disconnect = self.mqttOnDisconnect
		self._mqttClient.on_message = self.mqttOnMessage
		self._mqttClient.on_publish = self.mqttOnPublish
		self._mqttClient.on_subscribe = self.mqttOnSubscribe
		self._mqttClient.on_unsubscribe = self.mqttOnUnsubscribe
		
		if debugging_mqtt:		
			self._mqttClient.on_log = self.mqttOnLog

		parser = argparse.ArgumentParser()
		parser.add_argument("-s", "--server", help="change MQTT server host", nargs=1)
		parser.add_argument("-p", "--port", help="change MQTT server port", nargs=1, type=int)
		parser.add_argument("-d", "--debug", help="set DEBUG log level", action='store_true')
		parser.add_argument("-l", "--logger", help="use logging config file", nargs=1)
		args = vars(parser.parse_args())

		if args['server']:
			self._mqttServerHost = args['server'][0]
			self._config['host'] = self._mqttServerHost

		if args['port']:
			self._mqttServerPort = args['port'][0]
			self._config['port'] = self._mqttServerHost
			
		if args['logger'] and os.path.isfile(args['logger']):
			logging.config.fileConfig(args['logger'])
			if args['debug']:
				self._logger = logging.getLogger('debug')
				self._logger.setLevel(logging.DEBUG)
			else:
				self._logger = logging.getLogger('production')
				self._logger.setLevel(logging.INFO)
		elif os.path.isfile('logging.ini'):
			logging.config.fileConfig('logging.ini')
			if args['debug']:
				self._logger = logging.getLogger('debug')
				self._logger.setLevel(logging.DEBUG)
			else:
				self._logger = logging.getLogger('production')
				self._logger.setLevel(logging.INFO)
		else:
			if args['debug']:
				self._logger = logging.getLogger('debug')
				self._logger.setLevel(logging.DEBUG)
			else:
				self._logger = logging.getLogger('production')
				self._logger.setLevel(logging.INFO)
			ch = logging.FileHandler(APPLICATIONNAME + '.log', 'w')
			ch.setLevel(logging.INFO)
			self._logger.addHandler(ch)
		
		with open(CONFIG_FILE, 'w') as conffile:
			yaml.dump(self._config, conffile, default_flow_style = False)
			
		self.start()
			
	#__________________________________________________________________
	def build(self):
		# return a Button() as a root widget
		return Button(text=_('hello world!!!') )

	#__________________________________________________________________
	def isConnectedToMqttBroker(self):	
				
		return self._mqttConnected

	#__________________________________________________________________
	def mqttOnConnect(self, client, userdata, flags, rc):

		if rc == 0:
			self._mqttConnected = True
			#self._logger.debug("Connected to MQTT server with flags: ", flags) # flags is dict
			self._logger.info(_("Program connected to MQTT server"))
			if self._mqttOutbox:
				try:
					message = "CONNECTED"
					(result, mid) = self._mqttClient.publish(self._mqttOutbox, message, qos=MQTT_DEFAULT_QoS, retain=True)
					self._logger.info("{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid, self._mqttOutbox))
				except Exception as e:
					self._logger.error("{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message, self._mqttOutbox))
					self._logger.debug(e)
			for topic in self._mqttSubscriptions:
				try:
					(result, mid) = self._mqttClient.subscribe(topic, MQTT_DEFAULT_QoS)
					self._logger.info("{0} (mid={1}) : {2}".format(_("Program subscribing to topic"), mid, topic))
				except Exception as e:
					self._logger.error(_("MQTT API : failed to call subscribe()"))
					self._logger.debug(e)
		elif rc == 1:
			self._logger.warning(_("Program failed to connect to MQTT server :  connection refused - incorrect protocol version"))
		elif rc == 2:
			self._logger.warning(_("Program failed to connect to MQTT server : connection refused - invalid client identifier"))
		elif rc == 3:
			self._logger.warning(_("Program failed to connect to MQTT server : connection refused - server unavailable"))
		elif rc == 4:
			self._logger.warning(_("Program failed to connect to MQTT server : connection refused - bad username or password"))
		elif rc == 5:
			self._logger.warning(_("Program failed to connect to MQTT server : connection refused - not authorised"))
		else:
			self._logger.warning("{0} {1}".format(_("Program failed to connect to MQTT server : return code was"), rc))

	#__________________________________________________________________
	def mqttOnDisconnect(self, client, userdata, rc):

		self._mqttConnected = False
		self._logger.info(_("Program disconnected from MQTT server"))

		serv = ''
		if isinstance(userdata, str):
			try:
				mydata = eval(userdata)
				if isinstance(mydata, dict) and 'host' in mydata and 'port' in mydata:
					serv = mydata['host'] + ':' + str(mydata['port'])
			except Exception as e:
				self._logger.debug(_("MQTT client userdata not as expected"))
				self._logger.debug(e)

		if serv:
			self._logger.warning("{0}{1} {2} {3}".format(_("Disconnected from MQTT server with rc="), rc, _("from"), serv))
		else:
			self._logger.warning("{0}{1}".format(_("Disconnected from MQTT server with rc="), rc))

	#__________________________________________________________________
	def mqttOnLog(self, client, userdata, level, buf):

		self._logger.debug("Paho log level {0} : {1}".format(level, buf))

	#__________________________________________________________________
	def mqttOnMessage(self, client, userdata, msg):

		message = None
		try:
			message = msg.payload.decode(encoding="utf-8", errors="strict")
		except:
			pass

		if message:
			self._logger.info(_("Message received : '") + message + _("' in ") + msg.topic)
			if msg.topic == self._mqttInbox and message == "@PING":
				self.publishMessage(self._mqttOutbox, "PONG")
			else:
				self.onMessage(msg.topic, message)
		else:
			self._logger.warning("{0} {1}".format(_("MQTT message decoding failed on"), msg.topic))

	#__________________________________________________________________
	def mqttOnPublish(self, client, userdata, mid):

		self._logger.debug("MQTT message is published : mid=%s userdata=%s", mid, userdata)
		self._logger.info("{0} (mid={1})".format(_("Message published"), mid))

	#__________________________________________________________________
	def mqttOnSubscribe(self, client, userdata, mid, granted_qos):

		self._logger.debug("MQTT topic is subscribed : mid=%s granted_qos=%s", mid, granted_qos) # granted_qos is (2,)
		self._logger.info("{0} (mid={1}) {2} {3}".format(_("Program susbcribed to topic"), mid, _("with QoS"), granted_qos))  # mid is a number (count)

	#__________________________________________________________________
	def mqttOnUnsubscribe(self, client, userdata, mid):

		self._logger.debug("MQTT topic is unsubscribed : mid=%s", mid)
		self._logger.info("{0} (mid={1})".format(_("Program has been unsusbcribed from topic"), mid))

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		print(topic, message)
		self.sendOmit(message)

	#__________________________________________________________________
	def publishMessage(self, topic, message):

		if not topic:
			self._logger.warning("{0} : '{1}'".format(_("Program failed to send message (no topic)"), message))			
		elif self._mqttConnected:
			try:
				(result, mid) = self._mqttClient.publish(topic, message, qos=MQTT_DEFAULT_QoS, retain=False)
				self._logger.info("{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid, topic))
			except Exception as e:
				self._logger.error("{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message, topic))
				self._logger.debug(e)
		else:
			self._logger.warning("{0} : '{1}'".format(_("Program failed to send message (disconnected)"), message))

	#__________________________________________________________________
	def start(self):	
				
		if self._mqttOutbox:
			try:
				self._mqttClient.will_set(self._mqttOutbox, payload="DISCONNECTED", qos=1, retain=True)
			except Exception as e:
				self._logger.error(_("MQTT API : failed to call will_set()"))
				self._logger.debug(e)
			
		mydata = { 'host': self._mqttServerHost, 'port': self._mqttServerPort }
		self._mqttClient.user_data_set(str(mydata))

		'''
		The loop_start() starts a new thread, that calls the loop method at 
		regular intervals for you. It also handles re-connects automatically.
		'''
		self._mqttClient.loop_start()
		
		'''
		If you use client.connect_async(), your client must use the 
		threaded interface client.loop_start()
		'''
		try:
			self._mqttClient.connect_async(self._mqttServerHost, port = self._mqttServerPort, keepalive = MQTT_KEEPALIVE)
		except Exception as e:
			self._logger.error(_("MQTT API : failed to call connect_async()"))
			self._logger.debug(e)
		

if __name__ == '__main__':
	import paho.mqtt.client as mqtt
	import uuid
	mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)
	app = MqttKivyApp(mqtt_client, debugging_mqtt=False)
	app.run()
	try:
		mqtt_client.disconnect()
		mqtt_client.loop_stop()
	except:
		pass
		
