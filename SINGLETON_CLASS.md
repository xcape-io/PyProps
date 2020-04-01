# PyProps library: Singleton class
***Library for escape room Raspberry props written in Python.***

With the *PyProps library* you can start coding a Raspberry props for you escape room 2.0 in a few minutes.


## PyProps library core
*MqttApp* and *MqttVar* classes, which manage MQTT messaging, will simplify and speed up the coding. *MqttApp* is the base class of the Python props program.

`constants.py` and `definitions.ini` are configuration files related to the escape room MQTT topics and the props flavor.

*Singleton* class will guarantee that only one instance of the props program runs on the Raspberry board.

See:
* MqttApp and MqttVar classes
* configuration files
* Singleton class


## PyProps library flavors

...

1. Compatible hardware
2. Installation
3. Usage
4. SSH relaunch command
5. Choose your PyProps flavor
    * AsyncioProps
    * GuizeroProps
    * KivyProps
    * PygameProps
    * QtProps
    * QtGuiProps
6. Eric IDE or PyCharm Professional
7. Understanding the code
8. *PyProps library* value for escape room 2.0
9. Application protocol for escape room 2.0 props
10. Examples


## 1. Compatible hardware
*PyProps library* supported hardware:
 - Raspberry Pi boards
 - Any computer or IoT board supporting Python 3
 
For GPIO support, *PyProps library* comes with code for Raspberry Pi 3 and Pi 4.


## 2. Installation
Download `PyProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi. Rename `PyProps-master` folder the a meaningful name for you props. 

A good habit is to rename the props folder to: `/home/pi/Room/Props/MyProps`

Install dependencies
```bash
pip3 install -r requirements.txt
```

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```python
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/My room/Props/Raspberry MyProps/inbox
app-outbox = Room/My room/Props/Raspberry MyProps/outbox
;mqtt-sub-control-scenario = Room/My room/Control/game:scenario
;mqtt-sub-control-clock-minutes=Room/My room/Control/game:clock:minutes
;mqtt-sub-control-countdown-minutes=Room/My room/Control/game:countdown:minutes
;mqtt-sub-control-players=Room/My room/Control/game:players
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


## 4. SSH relaunch command
The command to relaunch the props from *<a href="https://xcape.io/" target="_blank">xcape.io</a>* **Room** software is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep MyProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/MyProps/main.py -s %BROKER%
```


## 5. Choose your PyProps flavor

### AsyncioProps
[AsyncioProps README](AsyncioProps%2FREADME.md.md)

For console (no GUI) props :
* sensor control
* actuator (digital outputs)
* sound

### GuizeroProps
... 
GuizeroProps.md

### KivyProps
... 
KivyProps.md

### PygameProps
... 
PygameProps.md

### QtProps
... 
QtProps.md

### QtGuiProps
... 
QtGuiProps.md


## 6. Eric IDE or PyCharm Professional
...


## 7. Understanding the code

### *PropsApp*
Echo props is built with the following files:
* `main.py` main script to start the props
* `constants.py`
* `definitions.ini`
* `logging.ini`
* __`PropsApp.py`__ props related code

It depends on:
* `MqttApp.py` base class to publish/subscribe MQTT messages
* `MqttVar.ini` base class to optimize network communications
* `Singleton.ini` to ensure one instance of application is running

You can use __`PropsApp.py`__ as a template to create your own connected props, you will also add GPIO elements.

About `create-props-tgz.bat`:
* install <a href="https://www.7-zip.org/" target="_blank">7-Zip</a> on your Windows desktop
* run `create-props-tgz.bat` to archive versions of your work

#### MQTT message protocol:
> This props has been created to be controlled with **Room** software so MQTT messages published in the props outbox implement the [Room Outbox protocol](PROTOCOL.md).

#### IDE for hacking `EchoApp.py`:
> You can open a PyCharm Professional project to hack the code remotely, thanks to `.idea` folder. Or if you prefer to the code hack directly on the Raspberry, we suggest <a href="https://eric-ide.python-projects.org/" target="_blank">Eric6 IDE</a>. 


### *MqttApp* and *MqttVar* base classes
*PropsApp* extends *MqttApp*, the python base app for Raspberry connected props.

MQTT topics are defined in *definitions.ini*.

***PubSub*** variables extend *MqttVar*, it is an helper to track value changes and to optimize publishing values in MQTT topic outbox.

You might not modify `MqttApp.py` an `MqttVar.py` files.

#### Notes about MQTT QoS:
>*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (particularly Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).


## 8. *PyProps library* value for escape room 2.0
### Inbox/oubox messaging  
Instead of usual MQTT topic structure which sends every data value in a different topic for every variable, *ArduinoProps library* sends data via a unique outbox topic. 

Props receives commands in its inbox MQTT topic.

Props can subscribe to any other MQTT topic to receive othe information, for example the escape game scenario (English/French/Kids) or the game clock countdown.

#### Escape room structured MQTT topics
If you're running our Escape Room control software *Room 2.0* to supervise the escape room in real-time you have to respect its syntax for inbox/outbnox MQTT topics: 
```csharp
Room/[escape room name]/Props/[propsname]/inbox|outbox

example:
    Room/Demoniak/Props/Arduino Contrôleur/inbox
    Room/Demoniak/Props/Arduino Contrôleur/outbox
```
MQTT supports UTF-8 encoding.
 
### Sending messages only when appropriate  
Usually Arduino IoT appes send MQTT data for every variable at every loop. When the loop is fast, you can get tons of useless messages, and usually a sleeping delay is added at every loop to slow down the message flow ; this can slow down significantly the props response time to human supervision and automation commands. 

While Arduino app is sending a message it isn't doing props sensor/actuator processing, and it takes about 20 to 40 milliseconds to send a message. With too many messsages it's too much processing time wasted.

*ArduinoProps library* sends all data periodically every 30 seconds (default parameter) and sends data changes over a period of time you choose (typical 400 milliseconds for real-time behavior, but you may choose every 100 milliseconds, 1 or 3 seconds: your choice for your application).

Therefore the minimum processing time is used to send messages.

Tracking data changes could make Arduino code difficult to read and maintain but the. *ArduinoProps library* will hide this mechanism and make the code much more readable.

Some analog data can change at every loop but not significantly, for example U=2.77 volts while showing this when it changes more than 10% could be sufficient. *ArduinoProps library* offers a nice syntax to take care of this significance, with simple code.

### Maintaining MQTT server connection  
MQTT connection state must be checked at erevy app loop as well as incoming MQTT messages. *ArduinoProps library* does all in one code line.

And on Yun this same code line can switch MQTT server IP address (can be helpful in a fallback plan).

### Simple human-readable text protocol  
An escape room 2.0 is typically centrally controlled from a Windows PC which provides the Game Master with monitoring and control information as well as some automation.

To unifiy escape room 2.0 development, *ArduinoProps library* provides a simple protocol between props and room controller at application level:
```csharp
    DATA -> send variables to control
    MESG -> send text to display in control
    DONE -> acknowledge a command has been performed
    OMIT -> acknowledge a command has been ignored
    OVER -> notify a challenge is over
    REQU -> request a command to another props
    PROG -> request a control program
```

### Handling long message seamlessly and efficiently  
MQTT standard limitations are far above what we need:
- maximum topic length 65,536 bytes (64k)
- maximum message size 268,435,456 bytes (256M)

However, on Arduino the limit is for the addition of topic length + message length:
- Wifi shield limit is 80 bytes
- Yun limit (due to Bridge) is 120 bytes

DATA messages when many I/O like on Arduino Mega 2560 and MESG information messages can go very long, and crash the app without notice at run-time.

*ArduinoProps library* seamlessly splits long messages smartly when required.

## 9. Application protocol for escape room 2.0 props

A *level 7* protocol (*application level*) is necessary for connected props to report data and to be controlled for the escape room automation and game play.

We have defined a simple human-readable text protocol. Messages are encoded in UTF-8, in Arduino appes use:
```csharp
    str = u8"la chaîne avec des caractères non Latin1";
```

Messages are sent/received thru outbox/inbox MQTT topics:
```csharp
    Room/[escape room name]/Props/[propsname]/inbox
    Room/[escape room name]/Props/[propsname]/outbox
```

Props connection state is handled in the outbox topic:
* with a `DISCONNECTED` **Will** when MQTT server connection is broken
* with a `CONNECTED` **retained message** when MQTT server connection is established.

More MQTT topics can be use for anything (room scenario, etc.).

#### Messages sent from the Arduino props are formatted
```csharp
    DATA sensor=24.26 light=on challenge=pinball
    MESG Warning: sensor not detected
    DONE power:1
    OMIT power:1
    OVER pinball
    REQU Arduino Relay -> door:open
    PROG audio-final:start
```

#### Message received by the Arduino props have no particular format
```csharp
    power:1                  for example to power on the room 
    porte-salon:ouvrir       for example to open a door
    lumière-salon:éteindre   for example to switch-off a light
```

    
#### @PING-PONG special messages
```csharp
    @PING is received in inbox then the props sends just PONG in outbox
    -> so the escape room controller can monitor response time at application level
```


## 10. Examples

...



## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>