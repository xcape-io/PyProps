#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
TeletextApp.py

TeletextApp loads teletext.kv and  extends MqttKivyApp.

'''

from MqttKivyApp import MqttKivyApp

#from MqttKivyApp import _is_rpi
#if _is_rpi: import RPi.GPIO as GPIO

from kivy.uix.effectwidget import EffectWidget, AdvancedEffectBase
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import os

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

class TeletextApp(MqttKivyApp):

	displayOnScreen = StringProperty('---')

	#__________________________________________________________________
	def __init__(self, client, debugging_mqtt=False, **kwargs):

		super().__init__(client, debugging_mqtt, **kwargs)
		
		# self.publishData() called when self.displayOnScreen is modifyed ; it'sb what we exactly want!
		self.bind(displayOnScreen=self.publishData)
		
		Clock.schedule_interval(self.publishData, 30.0)

	#__________________________________________________________________
	def build(self):
		# return nothing so teletext.kv is loaded
		#return Button(text=_('hello') )
		self.root.ids.display_label.text = '' # must be different from initial self.displayOnScreen to publish at connect
		pass
		
	#__________________________________________________________________
	def mqttOnConnect(self, client, userdata, flags, rc):

		MqttKivyApp.mqttOnConnect(self, client, userdata, flags, rc)
		self.displayOnScreen = self.root.ids.display_label.text

	#__________________________________________________________________
	def onMessage(self, topic, message):
		# extend as a virtual method
		#print(topic, message)
		if message == "app:startup" or message == "effacer":
			self.root.display('')
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			self.displayOnScreen = self.root.ids.display_label.text
		elif message.startswith("afficher:"):
			text = message[9:]
			self.root.display(text)
			self.publishMessage(self._mqttOutbox, "DONE " + message)
			self.displayOnScreen = self.root.ids.display_label.text
			sound = SoundLoader.load('bell.wav')
			if sound:
				os.system("amixer set 'PCM' -- -300") # volume -3dB
				sound.play() # asynchronous
		else:
			self.publishMessage(self._mqttOutbox, "OMIT " + message)

	#__________________________________________________________________
	def publishData(self, instance=None, prop=None):
		display = self.displayOnScreen
		if not display: display = '-'
		data = "DATA " + "affichage=" + display
		self.publishMessage(self._mqttOutbox, data)
