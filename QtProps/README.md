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

[QtProps](./QtProps) extends either *QCoreApplication* or *QApplication* object to add MQTT asynchronous messaging to the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> framework to facilitate your coding.

## Installation and usage
You will find installation and usage instructions in the [PyProps library INSTALLATION.md](../INSTALLATION.md)

PyQt5 must be installed:

```bash
    $ sudo apt-get update
    $ sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
```

## Qt Console  Props applications
For example:
* educational blink example ([QtEducationalProps](./QtProps/QtEducationalProps))
* fortune teller table ([FortuneTellerTableProps](./QtProps/FortuneTellerTableProps))
* game countdown on the escape room TV screen ([QtCountdownProps](./QtProps/QtCountdownProps))


## Author

**Marie FAURE** (Apr 11th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>