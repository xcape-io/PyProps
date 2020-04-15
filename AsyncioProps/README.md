# Asyncio Props
*Examples of pure Python props using **asyncio**.*

With ***AsyncioProps*** flavor, you code props that do not need a graphical interface:
* sensors and actuators (GPIO and I2C shieds)
* sound (<a href="https://pypi.org/project/playsound/" target="_blank">playsound</a>, <a href="https://pypi.org/project/pydub/" target="_blank">pydub</a> or native player like _aplay_, _mplayer_ and _mpg123_)

The <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework allows writing non-blocking Python programs that multitask seamlessly.

***AsyncioProps*** props hides the complexity of the <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a> framework and adds MQTT asynchronous messaging to facilitate your coding.

You will choose your sound solution according to the latency required for the prop to play an audio file.

## Installation and usage
You will find installation and usage instructions in the [PyProps library INSTALLATION.md](../INSTALLATION.md)


## Asyncio Props applications
For most the common console props (without graphical interface), for example:
* educational example which echoes messages and make a LED blinking ([PyBlinkEcho](PyBlinkEcho))
* detect vibrations to trigger a crying doll  ([PyCryingDollProps](PyCryingDollProps))
* detect RFID tag with a NFC I2C shield
* play sound


## Author

**Marie FAURE** (Mar 30th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>