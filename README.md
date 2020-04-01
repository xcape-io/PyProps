﻿# PyProps library
***Library for escape room Raspberry props written in Python.***

With the *PyProps library* you can start coding a Raspberry props for you escape room 2.0 in a few minutes.


## PyProps library core
*MqttApp* and *MqttVar* classes, which manage MQTT messaging, will simplify and speed up the coding. *MqttApp* is the base class of the Python props program.

`constants.py` and `definitions.ini` are configuration files related to the escape room MQTT topics and the props flavor.

*Singleton* class will guarantee that only one instance of the props program runs on the Raspberry board.

See:
* [MqttApp and MqttVar classes](MQTT_CLASSES.md)
* [configuration files](CONFIGURATION_FILES.md)
* [Singleton class](SINGLETON_CLASS.md)
* [Installation and usage](INSTALLATION.md)


## PyProps library flavors
The *PyProps library* takes advantage for many Python frameworks available on the Raspberry Pi running Raspbian to meet the requirements of any props created for the escape rooms.

### Asyncio framework: [AsyncioProps](./AsyncioProps)
With [AsyncioProps](./AsyncioProps) flavor, you code props that do not need a graphical interface:
* sensors and actuators (GPIO and I2C shieds)
* sound (*playsound, pydub, aplay, mplayer, mpg123*)

The <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework allows writing non-blocking Python programs that multitask seamlessly.

[AsyncioProps](./AsyncioProps) props hides the complexity of the <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework and adds MQTT asynchronous messaging to facilitate your coding.

### Pygame framework: [PygameProps](./PygameProps)
The <a href="https://pypi.org/project/pygame/" target="_blank">Pygame framework</a> is easy to use and is powerful for:
* audio and video output
* keyboard, mouse and joystick input
* sensors and actuators (GPIO and I2C shields)

The <a href="https://pypi.org/project/pygame/" target="_blank">Pygame framework</a> (see <a href="https://www.pygame.org/" target="_blank">pygame.org</a>) is very popular and very easy to learn so the [PygameProps](./PygameProps) flavor may be your preferred choice most of the time.

<a href="https://www.pygame.org/" target="_blank">Pygame</a> has its own event loop to multitask seamlessly.

[PygameProps](./PygameProps) adds MQTT asynchronous messaging to the <a href="https://pypi.org/project/pygame/" target="_blank">Pygame</a> framework to facilitate your coding.

### PyQt5 framework: [QtProps](./QtProps) and [QtGuiProps](./QtGuiProps)
<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> brings the power of <a href="https://doc.qt.io/" target="_blank">Qt</a> to Python and is well supported on Raspberry Pi.

Two flavors:
* [QtProps](./QtProps)
* [QtGuiProps](./QtGuiProps)

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> has its own event loop to multitask seamlessly.

[QtProps](./QtProps) and [QtGuiProps](./QtGuiProps) extend *QApplication* object to add MQTT asynchronous messaging to the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> framework to facilitate your coding.

### Guizero (Tkinter GUI) framework: [GuizeroProps](./GuizeroProps)
<a href="https://pypi.org/project/guizero/" target="_blank">Guizero</a> is a very simple and easy GUI framework built over [Tkinter](https://docs.python.org/3/library/tkinter.html) so if you need a simple GUI for your props it's a reasonable choice and if you need more features you have access to <a href="https://docs.python.org/3/library/tkinter.html" target="_blank">Tkinter</a> via the `_gui.tk` property.

See <a href="https://pypi.org/project/guizero/" target="_blank">Guizero Gettings Started</a> and the Guizero widgets from the same web page.

[GuizeroProps](./GuizeroProps) extends *<a href="https://lawsie.github.io/guizero/app/" target="_blank">Guizero App</a>* object to add MQTT asynchronous messaging to the <a href="https://pypi.org/project/guizero/" target="_blank">Guizero</a> framework to facilitate your coding.

### Kivy framework: [KivyProps](./KivyProps)
<a href="https://kivy.org" target="_blank">Kivy</a> is a very powerful framework but is not that simple therefore more particularly recommended for advanced Python developers.

To install <a href="https://kivy.org" target="_blank">Kivy</a> on Raspberry Pi, see <a href="https://kivy.org/doc/stable/installation/installation-rpi.html" target="_blank">Installation on Raspberry Pi</a> in the <a href="https://kivy.org/doc/stable/gettingstarted/intro.html" target="_blank">Kivy Guides</a>.

[KivyProps](./KivyProps) extends *<a href="https://kivy.org/doc/stable/api-kivy.app.html" target="_blank">Kivy App </a>* object to add MQTT asynchronous messaging to the <a href="https://kivy.org" target="_blank">Kivy</a> framework to facilitate your coding.


## Compatible hardware
*PyProps library* supported hardware:
 - Raspberry Pi boards
 - Any computer or IoT board supporting Python 3
 
For GPIO support, *PyProps library* comes with code for Raspberry Pi 3 and Pi 4.


## Eric IDE or PyCharm Professional
You can use any Python IDE for your props development however we recommend:
* Eric IDE to code and debug directly on the props via the VNC viewer
* <a href="https://www.jetbrains.com/pycharm/" target="_blank">PyCharm Professional</a> on your PC to code and debug remotely

<a href="https://eric-ide.python-projects.org/" target="_blank">Eric IDE</a> is free, powerful particularly for debugging and its installation is easy:

```bash
$ sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
$ sudo apt-get install eric
```

## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>