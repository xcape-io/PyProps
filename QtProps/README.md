# Qt Props
*Examples of pure Python props using **PyQt5** even loop.*

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> brings the power of <a href="https://doc.qt.io/" target="_blank">Qt</a> to Python and is well supported on Raspberry Pi.

***QtProps*** is suitable for console and GUI props with <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a>:
* multimedia playback
* graphics effects
* sensors and actuators (GPIO and I2C shieds)
* Bluetooth support,
* printing support,
* styled GUI (<a href="https://doc.qt.io/qt-5/stylesheet-reference.html" target="_blank">Qt Style Sheets</a>)
* <a href="https://doc.qt.io/qt-5/signalsandslots.html" target="_blank">Qt Signals & Slots</a> mechanism
* easy to reuse the props code in a control panel (necessary for complex props such as fingerprint biometric props with 2 Raspberry boards)
* reuse the props code for its associated control applet
* use the associated control applet as a <a href="https://github.com/xcape-io/PySkeletonPlugin" target="_blank">Room plugin</a>

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> has its own event loop to multitask seamlessly.

***QtProps*** extends either *QCoreApplication* or *QApplication* object to add MQTT asynchronous messaging to the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> framework to facilitate your coding.

## Installation and usage
You will find installation and usage instructions in the [PyProps library INSTALLATION.md](../INSTALLATION.md)

PyQt5 must be installed:

```bash
    $ sudo apt-get update
    $ sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
    $ sudo apt-get install python3-pyqt5 python3-pyqt5-dbg
```

You will have to install more packages from `python3-pyqt5` packages:

```bash
    $ sudo apt-get update
    $ apt-cache search pyqt5 | grep python3-pyqt5
    
    python3-pyqt5 - Python 3 bindings for Qt5
    python3-pyqt5-dbg - Python 3 bindings for Qt5 (debug extensions)
    python3-pyqt5.qsci - Python 3 bindings for QScintilla 2 with Qt 5
    python3-pyqt5.qsci-dbg - Python 3 bindings for QScintilla 2 (Qt 5 debug extensions)
    python3-pyqt5.qtchart - Python 3 bindings for Qt5's Charts module
    python3-pyqt5.qtchart-dbg - Python 3 bindings for Qt5's Charts module (debug extension)
    python3-pyqt5.qtmultimedia - Python 3 bindings for Qt5's Multimedia module
    python3-pyqt5.qtmultimedia-dbg - Python 3 bindings for Qt5's Multimedia module (debug extensions)
    python3-pyqt5.qtopengl - Python 3 bindings for Qt5's OpenGL module
    python3-pyqt5.qtopengl-dbg - Python 3 bindings for Qt5's OpenGL module (debug extension)
    python3-pyqt5.qtpositioning - Python 3 bindings for QtPositioning module
    python3-pyqt5.qtpositioning-dbg - Python 3 bindings for QtPositioning module (debug extension)
    python3-pyqt5.qtquick - Python 3 bindings for QtQuick module
    python3-pyqt5.qtquick-dbg - Python 3 bindings for QtQuick module (debug extension)
    python3-pyqt5.qtsensors - Python 3 bindings for QtSensors module
    python3-pyqt5.qtsensors-dbg - Python 3 bindings for QtSensors module (debug extension)
    python3-pyqt5.qtserialport - Python 3 bindings for QtSerialPort module
    python3-pyqt5.qtserialport-dbg - Python 3 bindings for QtSerialPort module (debug extension)
    python3-pyqt5.qtsql - Python 3 bindings for Qt5's SQL module
    python3-pyqt5.qtsql-dbg - Python 3 bindings for Qt5's SQL module (debug extension)
    python3-pyqt5.qtsvg - Python 3 bindings for Qt5's SVG module
    python3-pyqt5.qtsvg-dbg - Python 3 bindings for Qt5's SVG module (debug extension)
    python3-pyqt5.qtwebchannel - Python 3 bindings for Qt5's WebChannel module
    python3-pyqt5.qtwebchannel-dbg - Python 3 bindings for Qt5's Webchannel module (debug extension)
    python3-pyqt5.qtwebkit - Python 3 bindings for Qt5's WebKit module
    python3-pyqt5.qtwebkit-dbg - Python 3 bindings for Qt5's WebKit module (debug extensions)
    python3-pyqt5.qtwebsockets - Python 3 bindings for Qt5's WebSockets module
    python3-pyqt5.qtwebsockets-dbg - Python 3 bindings for Qt5's WebSockets module (debug extensions)
    python3-pyqt5.qtx11extras - Python 3 bindings for QtX11Extras module
    python3-pyqt5.qtx11extras-dbg - Python 3 bindings for QtX11Extras module (debug extension)
    python3-pyqt5.qtxmlpatterns - Python 3 bindings for Qt5's XmlPatterns module
    python3-pyqt5.qtxmlpatterns-dbg - Python 3 bindings for Qt5's XmlPatterns module (debug extension)
    python3-pyqt5.qwt - Python version of the Qwt6 technical widget library (Python3)

```

## Qt Console  Props applications
For example:
* educational blink example ([QtEducationalProps](./QtEducationalProps))
* fortune teller table ([FortuneTellerTableProps](./FortuneTellerTableProps))
* game countdown on the escape room TV screen ([QtCountdownProps](./QtCountdownProps))


## Author

**Marie FAURE** (Apr 11th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>