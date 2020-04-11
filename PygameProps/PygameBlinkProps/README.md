# Pygame Blink props
*Educational example of pure Python props using **pygame**.*

An educational example which makes a LED blinking and making a sound.

This props uses Pygame and extends <a href="https://github.com/xcape-io/PyProps/blob/master/core/ThreadingProps.py" target="_blank">ThreadingProps</a> (so it uses multi-threading) .


## Installation
See [INSTALLATION.md](.../INSTALLATION.md) and as a good habit is the PyProps folder is `/home/pi/Room/Props/PyProps`

### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PygameBlinkProps* requirements:
* `PyProps/core/ThreadingProps.py`
* `PyProps/core/PropsApp.py`
* `PyProps/core/MqttApp.py`
* `PyProps/core/PropsData.py`
* `PyProps/core/Singleton.py`

And you will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/PygameProps/PygameBlinkProps`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/PygameProps/PygameBlinkProps/main.py -s 192.168.1.42 -d

pygame 1.9.4.post1
Hello from the pygame community. https://www.pygame.org/contribute.html
Config: {'host': '192.168.1.42'}
/home/pi/Room/Props/PyProps/PygameProps/PygameBlinkProps/BlinkApp.py:27: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
  GPIO.setup(GPIO_BLINKING_LED, GPIO.OUT, initial=GPIO.LOW)
INFO - New boolean Publishable 'led' (1/0) with initial=0
INFO - New boolean Publishable 'blinking' (yes/no) with initial=0
INFO - Program connected to MQTT server
INFO - Program sending message 'CONNECTED' (mid=1) on Room/My room/Props/Raspberry PygameBlink/outbox
INFO - Program subscribing to topic (mid=2) : Room/My room/Props/Raspberry PygameBlink/inbox
INFO - Program sending message 'DATA led=0 blinking=no' (mid=3) on Room/My room/Props/Raspberry PygameBlink/outbox
DEBUG - MQTT message is published : mid=1 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=1)
DEBUG - MQTT message is published : mid=3 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=3)
DEBUG - MQTT topic is subscribed : mid=2 granted_qos=(0,)
INFO - Program susbcribed to topic (mid=2) with QoS (0,)
```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PygameBlinkProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/PygameProps/PygameBlinkProps/main.py -s %BROKER%
```


## Pygame Blink Props as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *PygameBlinkProps* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands
* `blink:0` : deactivate blinking
* `blink:1` : activate blinking

### Props configuration
Add and configure *Raspberry PygameBlink* connected props.

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