# PyProps library configuration files
*Configuration files are available for every prop application.*

The *PyProps* library offers an unified coding apprach to facilitate and speed up props coding.

Two configuration files are always avaliable:
* [`constants.py`]( #constantspy)
* [`definitions.ini`](#definitionsini)

## `constants.py`
For example here is the `constants.py` for [PyCryingDollProp](https://github.com/xcape-io/PyProps/tree/master/AsyncioProp/PyCryingDollProp)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
constants.py

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
For example here is the `definitions.py` for [QtCountdownProp](https://github.com/xcape-io/PyProps/tree/master/QtProp/QtCountdownProp)
```ini
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttConsoleApp
app-inbox = Room/My room/Props/Raspberry Countdown/inbox
app-outbox = Room/My room/Props/Raspberry Countdown/outbox
mqtt-sub-countdown-seconds = Room/My room/Control/game:countdown:seconds
```

#### `app-inbox` and `app-outbox` definitions
The prop *inbox* and *outbox* MQTT topics are loaded by the prop base class (either [`MqttApp`](https://github.com/xcape-io/PyProps/blob/master/core/MqttApp.py), [`QtMqttApp`](https://github.com/xcape-io/PyProps/blob/master/core/QtMqttApp.py) or [`KivyProp`](https://github.com/xcape-io/PyProps/blob/master/core/KivyProp.py)).

For *inbox* and *outbox* topics see [PROTOCOL.md](https://github.com/xcape-io/PyProps/blob/master/PROTOCOL.md)

#### `mqtt-sub-*` definitions
Each topic starting with `mqtt-sub-` is subscribed by the prop base class and messages are received in `onMessage(topic, message)` method which also receives messages from the *inbox*.


## Author

**Faure Systems** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>