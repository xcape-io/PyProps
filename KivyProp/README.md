# Kivy props
*Examples of pure Python props using **Kivy** even loop.*

<a href="https://kivy.org/" target="_blank">Kivy</a> is a very powerful Python framework and may be recommended for advanced Python developers.

***KivyProp*** hides a lot of complexity, therefore any escape room tinkerer should be able to create his own prop with <a href="https://kivy.org/" target="_blank">Kivy</a>.

***KivyProp*** is suitable for:
* powerful graphical interface for a Raspberry with a TV display ([PyWaterWellProp](./PyWaterWellProp))
* video effects
* video games
* audio
* camera, keyboard, mouse and joystick input
* multi-touch app
* sensors and actuators (GPIO and I2C shieds)

To learn the <a href="https://kivy.org" target="_blank">Kivy</a> framework, a goods start is <a href="https://kivy.org/doc/stable/gettingstarted/intro.html" target="_blank">Kivy Guides</a>.

***KivyProp*** extends *<a href="https://kivy.org/doc/stable/api-kivy.app.html" target="_blank">KivyApp</a>*  object to add MQTT asynchronous messaging to the <a href="https://kivy.org" target="_blank">Kivy</a> framework to facilitate your coding.


## Kivy installation on Raspbian
Installing Kivy can be bumpy and crash the system, so **we recommend installing Kivy on a fresh Raspbian installation**.

<a href="https://kivy.org" target="_blank">Kivy</a> installation on Raspberry Pi is a bit tough, as you may read from <a href="https://kivy.org/doc/stable/installation/installation-rpi.html" target="_blank">Installation on Raspberry Pi</a>. We have simplied the job for you with a shell script ([install-kivy.sh](https://github.com/xcape-io/PyProps/blob/master/KivyProp/install-kivy.sh)):
1. Connect and HDMI display to the Raspberry (required during Kivy installation)
2. Update your system

```bash
    pi@raspberrypi:~ $ sudo apt-get update 
    pi@raspberrypi:~ $ sudo apt-get upgrade 
```
3. Make `install-kivy.sh` executable

```bash
    pi@raspberrypi:~ $ cd Room/Props/PyProps/KivyProp
    pi@raspberrypi:~/Room/Props/PyProps/KivyProp $ chmod a+x install-kivy.sh 
```
4. Run `install-kivy.sh`

```bash
pi@raspberrypi:~/Room/Props/PyProps/KivyProp $ ./install-kivy.sh
```




## Kivy Props applications
For props with advanced graphical interface, for example:
* display text with a water effect on the prop TV monitor ([PyWaterWellProp](PyWaterWellProp))


## Author

**Faure Systems** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>