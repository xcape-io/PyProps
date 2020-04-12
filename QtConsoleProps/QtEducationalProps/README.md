# PyQt5 Educational props
*Educational example of pure Python props using **PyQt5**.*

An educational example which makes a LED blinking and making a sound when an RFID tag is detected.

This props uses PyQt5 and extends <a href="https://github.com/xcape-io/PyProps/blob/master/core/QtProps.py" target="_blank">ThreadingProps</a> (so it uses multi-threading) .

We use a MIFARE RFID-RC522 module:

https://www.waveshare.com/wiki/PN532_NFC_HAT
http://wiki.sunfounder.cc/index.php?title=Mifare_RC522_Module_RFID_Reader


![](docs/1-module%20schema.png)


## Installation
This props was created before PyProps library was released so there is no dependencies with PyProps.

You will have to install following Python packages:
```bash
    $ pip3 install paho-mqtt
    $ pip3 install PyYAML
    $ sudo apt-get update
    $ sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
```

### RFID-RC522 module configuration
1) enable SPI in **raspi-config**
2) check:
```bash
    $ lsmod | grep spi
    spidev                 16384  0
    spi_bcm2835            16384  0
```
3) install python library
```bash
    $ sudo apt-get update
    $ sudo apt-get upgrade
```
4) download and install SPI-Py
```bash
    $ cd ~
    $ git clone https://github.com/lthiery/SPI-Py.git
    $ cd ~/SPI-Py
    $ sudo python3 setup.py install
```


## Usage
Start `main.py` script in `/home/pi/Room/Props/PyProps/QtConsoleProps/QtEducationalProps/`:

```bash
pi@raspberrypi:~ $ python3 ~/Room/Props/PyProps/QtConsoleProps/QtEducationalProps/main.py -s 192.168.1.42 -d

...
...

```


## SSH relaunch command
The command to relaunch the props is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep QtEducationalProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyProps/QtConsoleProps/QtEducationalProps/main.py -s %BROKER%
```


## Fortune Teller Table Props as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a>
To use *QtEducationalProps* as a props for <a href="https://xcape.io/" target="_blank">*xcape.io* **Room**</a> software, here are props commands and messages as well as a suggested control panel.

### Props commands

...


## Author

**Marie FAURE** (Apr 10th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>