# Pygame Podium props
*A props from <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a> using **pygame**.*

A real word props, we created a rostrum (*podium* in French) powered by a Raspberry Pi; the players have clues in the room to find the correct sequence of coded keys; when a correct key is struck, an associated sound is played and when a wrong key in the sequence is struck, another sound is played.

Players must play the correct sequence to win the challenge that opens the rostrum hidden door with a linear grip.

This is a good example of GPIO events with debouncing and audio.

## Installation
This props was created before PyProps library was released so there is no dependencies with PyProps.

You will have to install following Python packages:
```bash
$ pip3 install paho-mqtt
$ pip3 install PyYAML
```

## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/PygameProps/PygamePodiumProps`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/PygameProps/PygamePodiumProps/main.py -s 192.168.1.42 -d

pygame 1.9.4.post1
Hello from the pygame community. https://www.pygame.org/contribute.html
Config: {'host': '192.168.1.42'}
INFO - GPIO: setup A input pulled-up.16
INFO - GPIO: setup B input pulled-up.20
INFO - GPIO: setup C input pulled-up.5
INFO - GPIO: setup D input pulled-up.6
INFO - GPIO: setup E input pulled-up.13
INFO - GPIO: setup F input pulled-up.19
INFO - GPIO: setup RELAY_JEU_DES_BILLES output.21 = 0
INFO - GPIO: setup RELAY_LIGHT output.22 = 1
INFO - GPIO: setup RELAY_VR_PLUS output.17 = 1
INFO - GPIO: setup RELAY_VR_MINUS output.27 = 1
INFO - New str Publishable 'activé' with initial=''
INFO - New str Publishable 'gagné' with initial=''
INFO - New str Publishable 'séquence' with initial=''
INFO - New str Publishable 'précédente' with initial=''
INFO - New str Publishable 'solution' with initial=''
INFO - New str Publishable 'magic' with initial=AAAA-BBBB-CCCC
INFO - New str Publishable 'vérin' with initial=''
INFO - New boolean Publishable 'lumière' (1/0) with initial=
INFO - New boolean Publishable 'billes' (1/0) with initial=
INFO - New str Publishable 'porte_avant' with initial=''
INFO - New str Publishable 'porte_arrière' with initial=''
INFO - New str Publishable 'bâton_avant' with initial=''
INFO - New str Publishable 'bâton_arrière' with initial=''
numid=3,iface=MIXER,name='PCM Playback Route'
  ; type=INTEGER,access=rw------,values=1,min=0,max=3,step=0
  : values=1
Simple mixer control 'PCM',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback -10239 - 400
  Mono: Playback 400 [100%] [4.00dB] [on]
WARNING - Program failed to send message (disconnected) : 'DATA vérin=en rentrée'
WARNING - Program failed to send message (disconnected) : 'DATA activé=non gagné=non séquence=- précédente=- solution=EDCA-EDAF-FBCE magic=AAAA-BBBB-CCCC vérin=en rentrée lumière=0 billes=0 porte_avant=3000 porte_arrière=4000 bâton_avant=6000 bâton_arrière=7000'
INFO - Program connected to MQTT server
INFO - Program sending message 'CONNECTED' (mid=1) on Room/My room/Props/Raspberry Podium/app-outbox
INFO - Program subscribing to topic (mid=2) : Room/My room/Props/Raspberry Podium/inbox
DEBUG - MQTT message is published : mid=1 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=1)
DEBUG - MQTT topic is subscribed : mid=2 granted_qos=(0,)
INFO - Program susbcribed to topic (mid=2) with QoS (0,)
INFO - Program sending message 'DATA activé=non gagné=non séquence=- précédente=- solution=EDCA-EDAF-FBCE magic=AAAA-BBBB-CCCC vérin=en rentrée lumière=0 billes=0 porte_avant=3000 porte_arrière=4000 bâton_avant=6000 bâton_arrière=7000' (mid=3) on Room/My room/Props/Raspberry Podium/app-outbox
DEBUG - MQTT message is published : mid=3 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=3)
INFO - Program sending message 'DATA activé=non gagné=non séquence=- précédente=- solution=EDCA-EDAF-FBCE magic=AAAA-BBBB-CCCC vérin=en rentrée lumière=0 billes=0 porte_avant=3000 porte_arrière=4000 bâton_avant=6000 bâton_arrière=7000' (mid=4) on Room/My room/Props/Raspberry Podium/app-outbox
DEBUG - MQTT message is published : mid=4 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=4)
INFO - Program sending message 'DATA vérin=rentré' (mid=5) on Room/My room/Props/Raspberry Podium/app-outbox
DEBUG - MQTT message is published : mid=5 userdata={'host': '192.168.1.42', 'port': 1883}
INFO - Message published (mid=5)

```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PygamePodiumProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/PygameProps/PygamePodiumProps/main.py -s %BROKER%
```


## Podium Props as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
This props is used as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software.

### Props commands
Commands are in French; look at the code in `PodiumApp.onMessage()` method.


## Author

**Marie FAURE** (Apr 10th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>