# PyProps library
***Library for escape room Raspberry props written in Python.***

With the *PyProps library* you can start coding a Raspberry props for you escape room 2.0 in a few minutes.

PyProps core library:
* hide the code to publish / subscribe messages with MQTT
* hide the complexity to create non-blocking asynchronous code
* expose a rotating file logger
* code is robust to work 24/7

PyProps examples:
* show how to code a props in a few lines
* provide code for common sensors / actuators

Read [INSTALLATION.md](INSTALLATION.md) for installation and usage.

## Props unified coding
PyProps supports different Python frameworks to write any kind of props providing a base class for your props:
* [AsyncioProps](./AsyncioProps)
* [PygameProps](./PygameProps)
* [QtConsoleProps](./QtConsoleProps)
* [QtGuiProps](./QtGuiProps)
* [GuizeroProps](./GuizeroProps)
* [KivyProps](./KivyProps)

Each props base class extends the base class *MqttApp* which handles messaging and  the base class *PropsApp* which handles the periodic actions and the simple [Room Outbox protocol](PROTOCOL.md) protocol.

*PropsData* is a base class that manages the props data variables sent to the outbox.

*Singleton* class will guarantee that only one instance of the props program runs on the Raspberry board.

Each props must have its own `constants.py` and `definitions.ini` [configuration files](CONFIGURATION_FILES.md) related to the escape room MQTT topics and to the props flavor.

`logging.ini` is the logger configuration file which can be used as is.

`main.py` is the main props script to:
* ensure only one instance of the props program is running
* initialize GPIO
* create the Paho MQTT client
* create the props class
* start MQTT client event loop
* start props framework event loop
* cleanup GPIO at end
* stop MQTT client event loop at end


## Props flavors
The *PyProps library* takes advantage for many Python frameworks available on the Raspberry Pi running Raspbian to meet the requirements of any props created for escape rooms.

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
* video games
* sensors and actuators (GPIO and I2C shields)

The <a href="https://pypi.org/project/pygame/" target="_blank">Pygame framework</a> (see <a href="https://www.pygame.org/" target="_blank">pygame.org</a>) is very popular and very easy to learn so the [PygameProps](./PygameProps) flavor may be your preferred choice most of the time.

<a href="https://www.pygame.org/" target="_blank">Pygame</a> has its own event loop to multitask seamlessly.

[PygameProps](./PygameProps) adds MQTT asynchronous messaging to the <a href="https://pypi.org/project/pygame/" target="_blank">Pygame</a> framework to facilitate your coding.

### PyQt5 framework: [QtConsoleProps](./QtConsoleProps) and [QtGuiProps](./QtGuiProps)
<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> brings the power of <a href="https://doc.qt.io/" target="_blank">Qt</a> to Python and is well supported on Raspberry Pi.

Two flavors:
* [QtConsoleProps](./QtConsoleProps)
* [QtGuiProps](./QtGuiProps)
* the power of Qt (printing support, multimedia, styled GUI, Bluetooth, etc.)
* easy to reuse the props code in a control panel (necessary for complex props such as fingerprint biometric props with 2 Raspberry boards)
* use same code for the props and its <a href="https://github.com/xcape-io/PySkeletonPlugin" target="_blank">Room plugin</a>

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> has its own event loop to multitask seamlessly.

[QtConsoleProps](./QtConsoleProps) and [QtGuiProps](./QtGuiProps) extend *QApplication* object to add MQTT asynchronous messaging to the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> framework to facilitate your coding.

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
You can use any Python IDE for your props development, however we recommend:
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