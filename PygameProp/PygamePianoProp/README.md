# Pygame Piano prop
*A prop from <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a> using **pygame**.*

A real word prop, we wired an antic mechanic piano to a Raspberry Pi; black keys play real music notes and white keys play slices of the infamous phrase of the Exorcist "Your mother suck cocks in hell".

Players must hit the 7 white keys in order to win the challenge that opens the piano top with a linear grip and plays the scary Exorcist music.

To reset the challenge (close the top), the game master plays a melody with 7 secret black keys.

This is a good example of GPIO events with debouncing and multi channel audio.

## Installation
This prop was created before PyProps library was released so there is no dependencies with PyProps.

You will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/PygameProp/PygamePianoProp`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/PygameProp/PygamePianoProp/main.py -s 192.168.1.42 -d

pygame 1.9.4.post1
Hello from the pygame community. https://www.pygame.org/contribute.html
Config: {}
INFO - New str Publishable 'configuration' with initial=''
INFO - New str Publishable 'gagné' with initial=''
INFO - New str Publishable 'séquence' with initial=''
INFO - New str Publishable 'solution' with initial=''
INFO - New str Publishable 'magic' with initial=Do# Sol# Ré# Fa# Do# Sol# Ré#
INFO - New str Publishable 'vérin' with initial=''
INFO - New str Publishable 'piano' with initial=''
INFO - GPIO: setup A input pulled-up.5
INFO - GPIO: setup B input pulled-up.6
INFO - GPIO: setup C input pulled-up.13
INFO - Program connected to MQTT server
INFO - GPIO: setup D input pulled-up.16
INFO - Program sending message 'CONNECTED' (mid=1) on Room/My room/Props/Raspberry Piano/app-outbox
INFO - GPIO: setup E input pulled-up.19
INFO - Program subscribing to topic (mid=2) : Room/My room/Props/Raspberry Piano/inbox
INFO - GPIO: setup F input pulled-up.20
INFO - Program subscribing to topic (mid=3) : Room/My room/Props/Room Control/game:setup
INFO - GPIO: setup G input pulled-up.21
INFO - GPIO: setup A# input pulled-up.17
INFO - GPIO: setup C# input pulled-up.22
INFO - GPIO: setup D# input pulled-up.23
INFO - GPIO: setup F# input pulled-up.24
INFO - GPIO: setup G# input pulled-up.27
INFO - GPIO: setup RELAY_VR_PLUS output.25 = 1
DEBUG - MQTT topic is subscribed : mid=2 granted_qos=(2,)
INFO - GPIO: setup RELAY_VR_MINUS output.25 = 1
INFO - Program susbcribed to topic (mid=2) with QoS (2,)
INFO - GPIO: setup RELAY_LATCH output.25 = 1
DEBUG - MQTT topic is subscribed : mid=3 granted_qos=(2,)
INFO - Program susbcribed to topic (mid=3) with QoS (2,)
DEBUG - MQTT message is published : mid=1 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=1)
numid=3,iface=MIXER,name='PCM Playback Route'
  ; type=INTEGER,access=rw------,values=1,min=0,max=3,step=0
  : values=1
Simple mixer control 'PCM',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback -10239 - 400
  Mono: Playback -100 [95%] [-1.00dB] [on]
INFO - Program sending message 'DATA configuration=Français gagné=non séquence=- solution=Ré Sol Fa La Do Si Mi magic=Do# Sol# Ré# Fa# Do# Sol# Ré# vérin=pause piano=fermé' (mid=4) on Room/My room/Props/Raspberry Piano/app-outbox
DEBUG - MQTT message is published : mid=4 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=4)

```


## SSH relaunch command
The command to relaunch the prop is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PygamePianoProp/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/PygameProp/PygamePianoProp/main.py -s %BROKER%
```


## Piano Prop as a prop for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
This prop is used as a prop for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software.

### Prop commands
Commands are in French; look at the code in `PianoApp.onMessage()` method.


## Author

**Marie FAURE** (Apr 10th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>