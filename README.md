# PyProps library
***Library for escape room Raspberry props written in Python.***

With the *PyProps library* you can start coding a Raspberry prop for you escape room 2.0 in a few minutes.

PyProps core library:
* hide the code to publish / subscribe messages with MQTT
* hide the complexity to create non-blocking asynchronous code
* expose a rotating file logger
* code is robust to work 24/7

PyProps examples:
* show how to code a prop in a few lines
* provide code for common sensors / actuators

Read <a href="RASPBERRY_PI_PROPS.md" target="_blank">RASPBERRY_PI_PROPS.md</a> to prepare your Rasbpberry Pi board ready for PyProps installation.

Read [INSTALLATION.md](INSTALLATION.md) for PyProps installation and usage.

## Props unified coding
PyProps supports different Python frameworks to write any kind of props providing a base class for your props:
* [AsyncioProp](#asyncio-framework-asyncioprop)
* [PygameProp](#asyncio-framework-asyncioprop)
* [QtProp](#pyqt5-framework)
* [GuizeroProp](#guizero-tkinter-gui-framework-guizeroprop)
* [KivyProp](#kivy-framework-kivyprop)

Each props base class extends the base class *MqttApp* which handles messaging and  the base class *PropApp* which handles the periodic actions and the simple [Room Outbox protocol](PROTOCOL.md) protocol.

*PropData* is a base class that manages the prop data variables sent to the outbox.

*Singleton* class will guarantee that only one instance of the prop program runs on the Raspberry board.

Each prop must have its own `constants.py` and `definitions.ini` **[configuration files](CONFIGURATION_FILES.md)** related to the escape room MQTT topics and to the prop flavor.

`logging.ini` is the logger configuration file which can be used as is.

`main.py` is the main prop script to:
* ensure only one instance of the prop program is running
* initialize GPIO
* create the Paho MQTT client
* create the prop class
* start MQTT client event loop
* start prop framework event loop
* cleanup GPIO at end
* stop MQTT client event loop at end


## Props flavors
The *PyProps library* takes advantage for many Python frameworks available on the Raspberry Pi running Raspbian to meet the requirements of any prop created for escape rooms.

### Asyncio framework: [AsyncioProp](./AsyncioProp)
With [AsyncioProp](./AsyncioProp) flavor, you code props that do not need a graphical interface:
* sensors and actuators (GPIO and I2C shieds)
* sound (*playsound, pydub, aplay, mplayer, mpg123*)
* examples:
    - educational example which echoes messages and make a LED blinking ([PyBlinkEcho](./AsyncioProp/PyBlinkEcho))
    - detect vibrations to trigger a crying doll  ([PyCryingDollProp](./AsyncioProp/PyCryingDollProp))

The <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework allows writing non-blocking Python programs that multitask seamlessly.

[AsyncioProp](./AsyncioProp) prop hides the complexity of the <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework and adds MQTT asynchronous messaging to facilitate your coding.

### Pygame framework: [PygameProp](./PygameProp)
The <a href="https://pypi.org/project/pygame/" target="_blank">Pygame framework</a> is easy to use and is powerful for:
* audio and video output
* simultaneous sounds
* keyboard, mouse and joystick input
* video games
* sensors and actuators (GPIO and I2C shields)
* examples:
    - educational blink example ([PygameBlinkProp](./PygameProp/PygameBlinkProp))
    - piano prop with a mechanic piano ([PygamePianoProp](./PygameProp/PygamePianoProp))
    - podium with linear jack ([PyPodiumgameProp](./PygameProp/PyPodiumgameProp))
    - hacker intrusion puzzle (contact me)
    - Tetris hacked (contact me)

The <a href="https://pypi.org/project/pygame/" target="_blank">Pygame framework</a> (see <a href="https://www.pygame.org/" target="_blank">pygame.org</a>) is very popular and very easy to learn so the [PygameProp](./PygameProp) flavor may be your preferred choice most of the time.

<a href="https://www.pygame.org/" target="_blank">Pygame</a> has its own event loop to multitask seamlessly.

[PygameProp](./PygameProp) adds MQTT asynchronous messaging to the <a href="https://pypi.org/project/pygame/" target="_blank">Pygame</a> framework to facilitate your coding.

### PyQt5 framework
<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> brings the power of <a href="https://doc.qt.io/" target="_blank">Qt</a> to Python and is well supported on Raspberry Pi.

Console and GUI props with <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a>:
* multimedia playback
* graphics effects
* sensors and actuators (GPIO and I2C shieds)
* Bluetooth support,
* printing support,
* styled GUI (<a href="https://doc.qt.io/qt-5/stylesheet-reference.html" target="_blank">Qt Style Sheets</a>)
* <a href="https://doc.qt.io/qt-5/signalsandslots.html" target="_blank">Qt Signals & Slots</a> mechanism
* the power of Qt (GUI widgets, styled GUI, multimedia, Bluetooth, printing support, etc.)
* easy to reuse the props code in a control panel (necessary for complex props such as fingerprint biometric props with 2 Raspberry boards)
* reuse the props code for its associated control applet
* use the associated control applet as a <a href="https://github.com/xcape-io/PySkeletonPlugin" target="_blank">Room plugin</a>
* examples:
    - educational blink example ([QtEducationalProp](./QtProp/QtEducationalProp))
    - fortune teller table ([FortuneTellerTableProp](./QtProp/FortuneTellerTableProp))
    - game countdown in the escape room on Raspberry TV screen ([QtCountdownProp](./QtProp/QtCountdownProp))

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> has its own event loop to multitask seamlessly.

[QtProp](./QtProp) extends either *QCoreApplication* or *QApplication* object to add MQTT asynchronous messaging to the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> framework to facilitate your coding.

### Guizero (Tkinter GUI) framework: [GuizeroProp](./GuizeroProp)
<a href="https://pypi.org/project/guizero/" target="_blank">Guizero</a> is a very simple and easy GUI framework built over [Tkinter](https://docs.python.org/3/library/tkinter.html) so if you need a simple GUI for your prop it's a reasonable choice and if you need more features you have access to <a href="https://docs.python.org/3/library/tkinter.html" target="_blank">Tkinter</a> via the `_gui.tk` property.

[GuizeroProp](./GuizeroProp) is suitable for:
* simple graphical interface for a Raspberry with a TV display 
* sensors and actuators (GPIO and I2C shieds)
* sound (*playsound, pydub, aplay, mplayer, mpg123*)
* example:
    - display text on the prop TV monitor ([PyTeletextProp](./GuizeroProp/PyTeletextProp))
    
See <a href="https://pypi.org/project/guizero/" target="_blank">Guizero Gettings Started</a> and the Guizero widgets from the same web page.

[GuizeroProp](./GuizeroProp) extends *<a href="https://lawsie.github.io/guizero/app/" target="_blank">Guizero App</a>* object to add MQTT asynchronous messaging to the <a href="https://pypi.org/project/guizero/" target="_blank">Guizero</a> framework to facilitate your coding.

### Kivy framework: [KivyProp](./KivyProp)
<a href="https://kivy.org" target="_blank">Kivy</a> is a very powerful framework but is not that simple therefore more particularly recommended for advanced Python developers.

[KivyProp](./KivyProp) is suitable for:
* powerful graphical interface for a Raspberry with a TV display 
* video effects
* video games
* audio
* camera, keyboard, mouse and joystick input
* multi-touch app
* sensors and actuators (GPIO and I2C shieds)
* example: 
    - display text on the prop TV monitor ([PyWaterWellProp](./KivyProp/PyWaterWellProp))
    
To learn the <a href="https://kivy.org" target="_blank">Kivy</a> framework, a goods start is <a href="https://kivy.org/doc/stable/gettingstarted/intro.html" target="_blank">Kivy Guides</a>.

[KivyProp](./KivyProp) extends *<a href="https://kivy.org/doc/stable/api-kivy.app.html" target="_blank">KivyApp</a>*  object to add MQTT asynchronous messaging to the <a href="https://kivy.org" target="_blank">Kivy</a> framework to facilitate your coding.


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