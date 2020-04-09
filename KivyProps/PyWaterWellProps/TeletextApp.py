#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
TeletextApp.py

Extending KivyProps, TeletextApp loads teletext.kv.
'''

from constants import *
from KivyProps import KivyProps

from kivy.uix.effectwidget import EffectWidget, AdvancedEffectBase
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import os
import logging, logging.config

#font = 'Something Strange'
#font = 'SpecialElite'
font = 'TheFont'

LabelBase.register(name=font,  
                   fn_regular="{}.ttf".format(font),
                   fn_bold="{}.ttf".format(font),
                   fn_italic="{}.ttf".format(font),
                   fn_bolditalic="{}.ttf".format(font))

effect_string = '''
uniform vec2 ref_coords;

vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{
    vec2 distance = 0.025*(coords - ref_coords);
    //float dist_mag = (distance.x*distance.x + distance.y*distance.y);
    float dist_mag = (distance.x*distance.x / 4.0+ distance.y*distance.y / 4.0);
    vec3 multiplier = vec3(abs(sin(dist_mag - time)));
    return vec4(multiplier * color.xyz, 1.0);
}
'''

class MyEffect(AdvancedEffectBase):
	ref_coords = ListProperty([Window.width / 2.0, 300.0 / 2.0])
	def __init__(self, *args, **kwargs):
		super(MyEffect, self).__init__(*args, **kwargs)
		self.glsl = effect_string
		self.uniforms = {'ref_coords': [Window.width / 2.0, Window.height / 2.0]}

class MyWidget(EffectWidget):
	display_text = StringProperty("ESCAPE")
	def __init__(self, *args, **kwargs):
		super(MyWidget, self).__init__(*args, **kwargs)
		self.effect = MyEffect()
		self.effects = [self.effect]
	def display(self, text):
		self.display_text = text

class TeletextApp(KivyProps):

	displayOnScreen = StringProperty('---')

	#__________________________________________________________________
	def __init__(self, client, debugging_mqtt=False, **kwargs):

		super().__init__(client, debugging_mqtt, **kwargs)

		self._logger = logging.getLogger('debug')
		self._logger.setLevel(logging.DEBUG)

		# self.publishData() called when self.displayOnScreen is modifyed ; it'sb what we exactly want!
		self.bind(displayOnScreen=self.publishData)
		
		Clock.schedule_interval(self.publishData, PUBLISHALLDATA_PERIOD)

	#__________________________________________________________________
	def build(self):
		# return nothing so teletext.kv is loaded
		#return Button(text='hello')
		self.root.ids.display_label.text = '' # must be different from initial self.displayOnScreen to publish at connect

	#__________________________________________________________________
	def mqttOnConnect(self, client, userdata, flags, rc):
		KivyProps.mqttOnConnect(self, client, userdata, flags, rc)
		self.displayOnScreen = self.root.ids.display_label.text
		self.publishData()

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		#print(topic, message)
		if message == "app:startup" or message == "erase":
			self.root.display('')
			self.sendDone(message)
			self.displayOnScreen = self.root.ids.display_label.text
			self.publishData()
			if self._mqttConnected:
				try:
					(result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS,
															 retain=True)
					self._logger.info(
						"{0} '{1}' (mid={2}) on {3}".format("Program sending message", message, mid,
															MQTT_DISPLAY_TOPIC))
				except Exception as e:
					self._logger.error(
						"{0} '{1}' on {2}".format("MQTT API : failed to call publish() for", message,
												  MQTT_DISPLAY_TOPIC))
					self._logger.debug(e)
		elif message.startswith("display:"):
			text = message[8:]
			self.root.display(text)
			self.displayOnScreen = self.root.ids.display_label.text
			self.sendDone(message)
			self.publishData()
			sound = SoundLoader.load('bell.wav')
			if sound:
				os.system("amixer set 'PCM' -- -300")  # volume -3dB
				sound.play()  # asynchronous
			if self._mqttConnected:
				try:
					(result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS,
															 retain=True)
					self._logger.info(
						"{0} '{1}' (mid={2}) on {3}".format("Program sending message", message, mid,
															MQTT_DISPLAY_TOPIC))
				except Exception as e:
					self._logger.error(
						"{0} '{1}' on {2}".format("MQTT API : failed to call publish() for", message,
												  MQTT_DISPLAY_TOPIC))
					self._logger.debug(e)
		else:
			self.sendOmit(message)

	#__________________________________________________________________
	def publishData(self, instance=None, prop=None):
		display = self.displayOnScreen
		if not display: display = '-'
		data = "display=" + display
		self.sendData(data)
