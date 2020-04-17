# PyProps library: configuration files
*Configuration files available for every prop application.*

The *PyProps* library offers an unified coding apprach to facilitate and speed up props coding.

Two configuration files are alway avaliable:
* [`constants.py`]( #constants)
* [`definitions.ini`](#definitions)

## `constants.py`
For example here is the `constants.py` for **[PyCryingDollProp](https://github.com/xcape-io/PyProps/tree/master/AsyncioProp/PyCryingDollProp)**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py (version 0.1)

Contains all the application constants. As a rule all constants are named in all caps.
'''

APPLICATION = "Crying Doll"

PYPROPS_CORELIBPATH = '../../core'

PUBLISHALLDATA_PERIOD = 30.0

USE_GPIO = True

#__________________________________________________________________
# Required by MqttApp
CONFIG_FILE = '.config.yml'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

MQTT_KEEPALIVE = 15 # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h

#__________________________________________________________________
# Required by CryingDollApp

GPIO_RELAY_LIGHT = 16
GPIO_VIBRATION_SENSORS = [20, 21]

AUDIO_CRYING = [
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/1.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/2.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/3.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/4.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/5.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/6.wav",
	"/home/pi/Room/Props/PyProps/AsyncioProp/PyCryingDollProp/audio/7.wav"]
```

Most of the constants are self-explanatory. Each constant is required by the prop classes and its base class.

#### `PYPROPS_CORELIBPATH` constant
`PYPROPS_CORELIBPATH` is the path to *PyProps* library core classes.

#### `PUBLISHALLDATA_PERIOD` constant
`PUBLISHALLDATA_PERIOD` is usually 30 therefore all *PropData* variables are sent in a `DATA` message every 30 seconds.

#### `MQTT_` constants
`MQTT_` constants are for the Paho MQTT client that is handled by either:
* `MqttApp` class
* `QtMqttApp` class
* `KivyProp` class


## `definitions.ini`
For example here is the `definitions.py` for



## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>