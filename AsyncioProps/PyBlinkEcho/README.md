# Blink Echo props
*Example of pure Python props using **asyncio**.*

An educational example which echoes messages and make a LED blinking.


## Installation
See [INSTALLATION.md](.../INSTALLATION.md) and as a good habit is the PyProps folder is `/home/pi/Room/Props/PyProps`

### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PyBlinkEcho* requirements:
* `PyProps/core/MqttApp.py`
* `PyProps/core/PropsData.py`
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

...





```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PyBlinkEcho/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/AsyncioProps/PyBlinkEcho/main.py -s %BROKER%
```


## Blink Echo as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *PyBlinkEcho* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands
* `blink:0` : deactivate blinking
* `blink:1` : activate blinking
* `echo:a message to be echoed` : echo the message


### Pros configuration
Add and configure *Raspberry BlinkEcho* connected props.

![Props configuration](props/props-configuration.png)


### Props data messages

![Outbox messages](props/outbox-messages.png)

### Props control panel

![Room control panel](props/room-control-panel.png)


### Plugin for Blink Echo props
Props control panel cannot display text on multiple lines or send text by the game master, therefore a plugin is necessary: [PyEchoPlugin](https://github.com/xcape-io/PyEchoPlugin)

![PyEchoPlugin](props/plugin.png)


## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>