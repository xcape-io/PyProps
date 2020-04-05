#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PropsApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

Props base class extends MqttApp:
- add automation
- agnostic to asyncio, Qt, Tkinter or Kivy
"""

from constants import *
from MqttApp import MqttApp


class PropsApp(MqttApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

