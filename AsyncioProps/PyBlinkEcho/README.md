# PyBlinkEcho props
*Example of pure Python props using **asyncio**.*

1. Compatible hardware
2. Installation
3. Usage
4. Eric IDE or PyCharm Professional
5. Understanding the code


## 1. Compatible hardware
*PyBlinkEcho props* supported hardware:
 - Raspberry Pi boards (GPIO support)


## 2. Installation
Download `PyProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi. Rename `PyProps-master` folder the a meaningful name for you props. 

A good habit is to rename the props folder to `/home/pi/Room/Props/MyProps` and the *PyBlinkEcho props* path will be `/home/pi/Room/Props/MyProps/examples/PyBlinkEcho`

Install dependencies
```bash
pi@raspberrypi:~/Room/Props/MyProps/examples/PyBlinkEcho $ pip3 install -r requirements.txt
```

To configure the props for <a href="https://xcape.io/go/room" target="_blank">xcape.io **Room**</a> software, edit `definitions.ini` to set MQTT topics for your Escape Room::
```python
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/My room/Props/Raspberry BlinkEcho/inbox
app-outbox = Room/My room/Props/Raspberry BlinkEcho/outbox
``` 


## 3. Usage
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

### SSH relaunch command
The command to relaunch the props from *<a href="https://xcape.io/" target="_blank">xcape.io</a>* **Room** software is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep MyProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/MyProps/main.py -s %BROKER%
```


## 4. Eric IDE or PyCharm Professional
...


## 5. Understanding the code



## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>