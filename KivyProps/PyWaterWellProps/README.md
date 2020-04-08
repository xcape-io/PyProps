# Water  Well props (*PyWaterWellProps*)

...

## Installation
Install Kivy with the  ([install-kivy.sh](https://github.com/fauresystems/PyProps/blob/master/KivyProps/PyWaterWellProps/install-kivy.sh)) shell script.

```bash
pi@raspberrypi:~/Room/Props/PyProps/KivyProps/PyWaterWellProps $ chmod a+x install-kivy.sh 
pi@raspberrypi:~/Room/Props/PyProps/KivyProps/PyWaterWellProps $ ./install-kivy.sh 

```


### Dependencies
If you don't install the whole PyProps library, you will have to fulfill the  *PyWaterWellProps* requirements:
* `PyProps/core/KivyProps.py`
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

...

## PyWaterWellProps as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *PyTeletextProps* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands
* `blink:0` : deactivate blinking
* `blink:1` : activate blinking
* `display:a message to display on the TV` : display the message


### Props configuration
Add and configure *Raspberry WaterWell* connected props.

The SSH relaunch command for GUI props relies on `signal.SIGUSR1`:
```bash
echo host: %BROKER%> /home/pi/Room/Props/PyProps/KivyProps/PyWaterWellProps/.config.yml && ps aux | grep python | grep -v "grep python" | grep PyWaterWellProps/main.py | awk '{print $2}' | xargs kill -10
```

![Props configuration](props/props-configuration.png)


### Props data messages

![Outbox messages](props/outbox-messages.png)


### Props control panel

![Room control panel](props/room-control-panel.png)


### Plugin for Water Well props
The [Teletext Plugin](https://github.com/fauresystems/TeletextPlugin) can be used as a standalone applet, without the need of <a href="https://xcape.io/go/room" target="_blank">Room software</a>. If you use <a href="https://xcape.io/go/room" target="_blank">Room software</a>, you will find <a href="https://xcape.io/public/documentation/en/room/AddaRaspberrypropsTeletext.html" target="_blank">detailed installation help in the Room manual</a>.

![PyTeletextPlugin](props/plugin.png)


## Author

**Marie FAURE** (Apr 8th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>