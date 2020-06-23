# PyProps library
***Installation and usage of the [PyProps library](README.md).***

## Prepare your Raspberry Pi as a prop
You will find instructions in the [RASPBERRY_PI_PROPS.md](RASPBERRY_PI_PROPS.md)

## Installation
Download `PyProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi. Rename `PyProps-master` folder the a meaningful name for you prop. 

A good habit is to rename the prop folder to: `/home/pi/Room/Props/MyProps`

Install dependencies
```bash
pip3 install -r requirements.txt
```

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```ini
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/My room/Props/Raspberry MyProps/inbox
app-outbox = Room/My room/Props/Raspberry MyProps/outbox
;mqtt-sub-control-scenario = Room/My room/Control/game:scenario
;mqtt-sub-control-clock-minutes=Room/My room/Control/game:clock:minutes
;mqtt-sub-control-countdown-minutes=Room/My room/Control/game:countdown:minutes
;mqtt-sub-control-players=Room/My room/Control/game:players
``` 


## Usage
Start `main.py` script:

```bash
usage: python3 main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file
```

To switch MQTT broker, kill the program and start again with new arguments.


## SSH relaunch command
The command to relaunch the prop from *<a href="https://xcape.io/" target="_blank">xcape.io</a>* **Room** software is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep MyProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/MyProps/main.py -s %BROKER%
```


## Author

**Faure Systems** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>