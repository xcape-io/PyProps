# *Prop* class reference
See also:
* <a href="PropData.md" target="_blank">PropData</a> class reference

## Props unified coding
Each flavor of PyProp base class either implements or redefines the *Prop* base class interface:
* [AsyncioProp](#asyncio-framework-asyncioprop) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [PygameProp](#asyncio-framework-asyncioprop) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [QtProp](#pyqt5-framework) see <a href="../core/QtPropApp.py" target="_blank">`QtPropApp.h`</a>
* [GuizeroProp](#guizero-tkinter-gui-framework-guizeroprop) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [KivyProp](#kivy-framework-kivyprop) see <a href="../core/KivyProp.py" target="_blank">`KivyProp.h`</a>


## Constructor


## Interface
The *Prop* class interface is consistent with the <a href="https://github.com/xcape-io/ArduinoProps/blob/master/help/Prop.md" target="_blank">Prop class</a> of the <a href="https://github.com/xcape-io/ArduinoProps#arduinoprops-library" target="_blank">ArduinoProps library</a> for Arduino boards.

* `addData(data)`
    -  registers a [PropData](PropData.md) instance to be treated by sendAllData() and sendDataChanges() methods.
* `addPeriodicAction(title, func, time)`
    - update the variable
* `sendAllData()`
    - returns 
* `sendDataChanges()`
    - returns 
* `sendData(data)`
    - returns 
* `sendDone(action)`
    - returns 
* `sendMesg(message, topic=None)`
    - returns 
* `sendOmit(action)`
    - returns 
* `sendOver(challenge)`
    - returns 
* `sendProg(program)`
    - returns 
* `sendRequ(request, topic=None)`
    - returns 



## Author

**Marie FAURE** (Apr 17th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>