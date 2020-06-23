#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeletextApp.py
MIT License (c) Faure Systems <dev at faure dot systems>

TeletextApp extends GuizeroProp.
"""

from constants import *

from PropData import PropData
from GuizeroProp import GuizeroProp
from Sound import Sound
from guizero import Text

import os, platform, sys, logging
if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
	import RPi.GPIO as GPIO

class TeletextApp(GuizeroProp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self._light_p = PropData('light', bool, 0, logger=self._logger)
        self.addData(self._light_p)
        self._blinking_p = PropData('blinking', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._blinking_p)

        GPIO.setup(GPIO_RELAY_LIGHT, GPIO.OUT, initial=GPIO.LOW)

        self._blinking_p.update(False)
        self._light_p.update(False)
        GPIO.output(GPIO_RELAY_LIGHT, self._light_p.value())

        if platform.system() != 'Windows':
            if self.logger.level != logging.DEBUG:
                self._gui.full_screen = True  # exit fullscreen with Esc (so for props without a keyboard)
        else:
            self._gui.width = 592
            self._gui.height = 333

        self._gui.bg = 'black'
        self._gui.tk.config(cursor="none")

        self._texte = Text(self._gui, "")  # "" value is translated to "-" for MQTT_DISPLAY_TOPIC
        self._texte.height = 1080
        self._texte.text_color = 'green'
        self._texte.font = "Helvetica"

        if platform.system() != 'Windows':
            self._texte.size = "90"
        else:
            self._texte.size = "28"

        self._sound = Sound(self._logger)

        self.addPeriodicAction("blink", self.blink, 1.0)

        if platform.system() != 'Windows':
            os.system("amixer cset numid=3 1")  # audio jack
            os.system("amixer set 'PCM' -- -1000")

        if self._mqttConnected:
            self.sendAllData()
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format("MQTT API : failed to call publish() for", "-", MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def blink(self):
        # test periodic
        try:
            if self._blinking_p.value():
                self._light_p.update(not self._light_p.value())
                GPIO.output(GPIO_RELAY_LIGHT, self._light_p.value())
                self.sendData(str(self._light_p))  # immediate notification
        except Exception as e:
            self._logger.error("Failed to execute periodic 'blink'")
            self._logger.debug(e)
        finally:
            self.playInSeconds(self.blink, 1.0)

    # __________________________________________________________________
    def lightOff(self):
        self._light_p.update(False)
        GPIO.output(GPIO_RELAY_LIGHT, self._light_p.value())
        self.sendData(str(self._light_p))  # immediate notification

    # __________________________________________________________________
    def lightOn(self):
        self._light_p.update(True)
        GPIO.output(GPIO_RELAY_LIGHT, self._light_p.value())
        self.sendData(str(self._light_p))  # immediate notification

    # __________________________________________________________________
    def lightOnForSeconds(self, time):
        self._light_p.update(True)
        GPIO.output(GPIO_RELAY_LIGHT, self._light_p.value())
        self.sendData(str(self._light_p))  # immediate notification
        self.playInSeconds(self.lightOff, time)

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        self.sendAllData()
        # display message will '-' for black screen
        if hasattr(self, '_texte'):
            text = self._texte.value
            if not text:
                text = "-"
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format("MQTT API : failed to call publish() for", text, MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message in ["app:startup", "app:quit"]:
            super().onMessage(topic, message)
        elif message.startswith("display:"):
            text = message[8:]
            self._texte.value = text
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
            self.sendDone(message)
            self.sendDataChanges()
            self.lightOnForSeconds(3.0)
            self._sound.play('media/bell.wav')
        elif message.startswith("erase"):
            self._texte.value = ""
            if self._mqttConnected:
                try:
                    (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
                    self._logger.info(
                        "{0} '{1}' (mid={2}) on {3}".format("Program sending message", message, mid,
                                                            MQTT_DISPLAY_TOPIC))
                except Exception as e:
                    self._logger.error(
                        "{0} '{1}' on {2}".format("MQTT API : failed to call publish() for", message,
                                                  MQTT_DISPLAY_TOPIC))
                    self._logger.debug(e)
            self.sendDone(message)
            self.sendDataChanges()
        elif message.startswith("blink:"):
            if message.endswith(":0"):
                self._blinking_p.update(False)
                self.sendDataChanges()
                self.sendDone(message)
            elif message.endswith(":1"):
                self._blinking_p.update(True)
                self.sendDataChanges()
                self.sendDone(message)
            else:
                self.sendOmit(message)
        else:
            self.sendOmit(message)

    # __________________________________________________________________
    def quit(self):
        self._gui.exit_full_screen()
        self._gui.destroy()
        try:
            self._mqttClient.disconnect()
            self._mqttClient.loop_stop()
        except:
            pass
        sys.exit(0)
