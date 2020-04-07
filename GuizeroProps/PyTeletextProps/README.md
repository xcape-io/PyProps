# Teletext props
***Display messages in the Escape Room with a Raspberry Pi.***

This props listens to MQTT messages and then displays the text on an HDMI display, rings a bell and turns on a light for 3 seconds.

Messages are sent by the game master with the [Teletext Plugin](https://github.com/fauresystems/TeletextPlugin) or any application able to publish MQTT messages.

The [Teletext Plugin](https://github.com/fauresystems/TeletextPlugin) can be used as a standalone applet, without the need of <a href="https://xcape.io/go/room" target="_blank">Room software</a>. If you use <a href="https://xcape.io/go/room" target="_blank">Room software</a>, you will find <a href="https://xcape.io/public/documentation/en/room/AddaRaspberrypropsTeletext.html" target="_blank">detailed installation help in the Room manual</a>.


## Installation
See [INSTALLATION.md](.../INSTALLATION.md) and as a good habit is the PyProps folder is `/home/pi/Room/Props/PyProps`

### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PyBlinkEcho* requirements:
* `PyProps/core/AsyncioProps.py`
* `PyProps/core/PropsData.py`
* `PyProps/core/Singleton.py`

And you will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
$ pip3 install guizero
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/GuizeroProps/PyTeletextProps`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/GuizeroProps/PyTeletextProps/main.py -s 192.168.1.42 -d

Config: {'host': '192.168.1.42'}
INFO - Program connected to MQTT server
INFO - Program sending message 'CONNECTED' (mid=1) on Room/My room/Props/Raspberry Teletext/outbox
INFO - Program subscribing to topic (mid=2) : Room/My room/Props/Raspberry Teletext/inbox
INFO - Program subscribing to topic (mid=3) : Room/My room/Control/game:scenario
DEBUG - MQTT message is published : mid=1 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=1)
DEBUG - MQTT topic is subscribed : mid=2 granted_qos=(1,)
INFO - Program susbcribed to topic (mid=2) with QoS (1,)
DEBUG - MQTT topic is subscribed : mid=3 granted_qos=(1,)
INFO - Program susbcribed to topic (mid=3) with QoS (1,)
INFO - Message received : '@PING' in Room/My room/Props/Raspberry Teletext/inbox
INFO - Program sending message 'PONG' (mid=4) on Room/My room/Props/Raspberry Teletext/outbox
DEBUG - MQTT message is published : mid=4 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=4)
numid=3,iface=MIXER,name='PCM Playback Route'
  ; type=INTEGER,access=rw------,values=1,min=0,max=3,step=0
  : values=1
Simple mixer control 'PCM',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback -10239 - 400
  Mono: Playback -1000 [87%] [-10.00dB] [on]
DEBUG - MQTT message is published : mid=5 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=5)
INFO - Message received : 'afficher:1515' in Room/My room/Props/Raspberry Teletext/inbox
Room/My room/Props/Raspberry Teletext/inbox afficher:1515
INFO - Program sending message 'afficher:1515' (mid=6) on Room/My room/Props/Raspberry Teletext/display
INFO - Program sending message 'DONE afficher:1515' (mid=7) on Room/My room/Props/Raspberry Teletext/outbox
```

To switch MQTT broker, kill the program and start again with new arguments.


## Understanding the code

### *TeletextApp*
Teletext props is built with the following files:
* `teletext.py` main script to start the props
* `constants.py`
* `definitions.ini`
* `logging.ini`
* __`TeletextApp.py`__ props related code

It depends on:
* `GuizeroProps.py` base class to create a guizero event loop
* `MqttApp.py` base class to publish/subscribe MQTT messages
* `PropsData.ini` base class to optimize network communications
* `Singleton.ini` to ensure one instance of application is running
* `Sound.py` simple *aplay* wrapper

Use ***TeletextApp*** as a model to create your own connected props if you need simple text display, sound playback. You can also add GPIO stuff.

About `create-teletextprops-tgz.bat`:
* install <a href="https://www.7-zip.org/" target="_blank">7-Zip</a> on your Windows desktop
* run `create-teletextprops-tgz.bat` to archive versions of your work

#### MQTT message protocol:
> This props has been created for [Live Escape Grenoble](https://www.live-escape.net/) rooms, controlled with **Room** software so MQTT messages published in the props outbox implement the <a href="https://github.com/fauresystems/TeletextProps/blob/master/PROTOCOL.md" target="_blank">Room Outbox protocol</a>.

#### IDE for hacking `TeletextApp.py`:
> You can open a PyCharm Professional project to hack the code remotely, thanks to `.idea` folder. Or if you prefer to the code hack directly on the Raspberry, we suggest <a href="https://eric-ide.python-projects.org/" target="_blank">Eric6 IDE</a>. 


### *GuizeroProps* base class
*TeletextApp* extends *GuizeroProps*, python base app for Raspberry connected props which require simple text display. 

For more advanced text display (visual effects, True-Type fonts) you may see *Kivi* props below such as TelefxProps.

GUI is built with *<a href="https://lawsie.github.io/guizero/" target="_blank">guizero</a>* library. If you don't need display, prefer *Asyncio* props.

Extend this base class to build a connected props which does simple text display, sound playback. Optionally you can GPIO stuff.

You might not modify `GuizeroProps.py` file.


### *MqttApp* and *PropsData* base classes
*GuizeroProps* extends *MqttApp*, the python base app for Raspberry connected props.


MQTT topics are defined in *definitions.ini*.

PubSub variables extend *PropsData*, it is an helper to track value changes and to optimize publishing values in MQTT topic outbox.

You might not modify `MqttApp.py` an `PropsData.py` files.

#### Notes about MQTT QoS:
>*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (particularly Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).


## Author

**Marie FAURE** (Apr 7th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>