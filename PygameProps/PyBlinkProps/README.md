# Pygame Blink props
*Educational example of pure Python props using **pygame**.*

An educational example which makes a LED blinking.

# !!!!!!!!! WORK IN PROGRESS


## Installation
See [INSTALLATION.md](.../INSTALLATION.md) and as a good habit is the PyProps folder is `/home/pi/Room/Props/PyProps`

### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PyBlinkProps* requirements:
* `PyProps/core/PropsData.py`
* `PyProps/core/PropsApp.py`
* `PyProps/core/MqttApp.py`
* `PyProps/core/Singleton.py`

And you will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/PygameProps/PyBlinkProps`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/PygameProps/PyBlinkProps/main.py -s 192.168.1.42 -d

Config: {'host': '192.168.1.42'}

```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PyBlinkProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/PygameProps/PyBlinkProps/main.py -s %BROKER%
```


## Blink Props as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *PyBlinkProps* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands
* `blink:0` : deactivate blinking
* `blink:1` : activate blinking

### Props configuration
Add and configure *Raspberry Blink* connected props.

![Props configuration](props/props-configuration.png)

### Props data messages

![Outbox messages](props/outbox-messages.png)

### Props control panel

![Room control panel](props/room-control-panel.png)


## Author

**Marie FAURE** (Apr 10th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>