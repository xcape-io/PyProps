# Blink Echo props
*Example of pure Python props using **asyncio**.*

An educational example which echoes messages and make a LED blinking.


## Installation
See [INSTALLATION.md](.../INSTALLATION.md) and as a good habit is the PyProps folder is `/home/pi/Room/Props/PyProps`

### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PyBlinkEcho* requirements:
* `PyProps/core/MqttApp.py`
* `PyProps/core/MqttVar.py`
* `PyProps/core/Singleton.py`

And you will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/AsyncioProps/PyBlinkEcho`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/AsyncioProps/PyBlinkEcho/main.py -s 192.168.1.42 -d
Config: {'host': '192.168.1.42'}
INFO - New boolean Publishable 'light' (1/0) with initial=0
INFO - New boolean Publishable 'crying' (1/0) with initial=0
INFO - New boolean Publishable 'activated' (yes/no) with initial=0
INFO - Setup vibration sensor input pin on 20
INFO - Setup vibration sensor input pin on 21
numid=3,iface=MIXER,name='PCM Playback Route'
  ; type=INTEGER,access=rw------,values=1,min=0,max=3,step=0
  : values=1
Simple mixer control 'PCM',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback -10239 - 400
  Mono: Playback 400 [100%] [4.00dB] [on]
INFO - Program started
INFO - Program connected to MQTT server
INFO - Program subscribing to topic (mid=1) : Room/My room/Raspberry CryingDoll/inbox
DEBUG - MQTT topic is subscribed : mid=1 granted_qos=(2,)
DEBUG - MQTT message is published : mid=2 userdata={'host': 'localhost', 'port': 1883}

```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PyBlinkEcho/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/AsyncioProps/PyBlinkEcho/main.py -s %BROKER%
```


## Vibration sensor
We use two vibration sensors module SW-420 connected on GPIO 20 and 21:

![SW-420](sensor/sw-420-vibration-sensor.png)

<a href="sensor%2FVibration%20Sensor%20Module%20SW420.pdf" target="_blank">Vibration Sensor Module SW420.pdf</a>


## Relay module
An SRD relay module is connected to GPIO 16 to control the light.

![SRD rely module](actuator/srd-relay-shield.jpg)


## Crying Doll as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *PyBlinkEcho* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands
* `activate:0` : deactivate sensor
* `activate:1` : activate sensor
* `light:off` : switch off the light
* `light:on` : switch off the light
* `cry:_` : trigger crying

Use `activate` to enable the cries at the right time (when starting a new game or when a challenge is completed).

Use `cry` if automatic detection doesn't work (sensor failure or calibration issue during a game) or to test sound level.

### Pros configuration
Add and configure *Raspberry CryingDoll* connected props.

![Props configuration](props/props-configuration.png)


### Props data messages

![Outbox messages](props/outbox-messages.png)

### Props control panel
Configure *Raspberry CryingDoll* control panel using the SVG images ![Crying doll](props/doll.png) provided in [images folder](images).

![Room control panel](props/room-control-panel.png)


## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>