# *Prop* class reference
See also:
* <a href="PropData.md" target="_blank">PropData</a> class reference

## Props unified coding
Each flavor of PyProp base class either implements or redefines the *Prop* base class interface:
* [AsyncioProp](https://github.com/xcape-io/PyProps/tree/master/AsyncioProp) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [PygameProp](https://github.com/xcape-io/PyProps/tree/master/PygameProp) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [QtProp](https://github.com/xcape-io/PyProps/tree/master/QtProp) see <a href="../core/QtPropApp.py" target="_blank">`QtPropApp.h`</a>
* [GuizeroProp](https://github.com/xcape-io/PyProps/tree/master/GuizeroProp) see <a href="../core/PropApp.py" target="_blank">`PropApp.py`</a>
* [KivyProp](https://github.com/xcape-io/PyProps/tree/master/KivyProp) see <a href="../core/KivyProp.py" target="_blank">`KivyProp.h`</a>


## Constructor
Every *Prop* constructor expects:
* `client` parameter
    - a Paho MQTT client created in `main.py` usually with
    `mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)`

Regarding the *Prop* flavor you will have to provide more parameters, such as `argv` and others.

See:
* **AsyncioProp** `main.py` example
* **PygameProp** `main.py` example
* **QtProp** `main.py` example
* **GuizeroProp** `main.py` example
* **KivyProp** `main.py` example


## Interface
The *Prop* class interface is consistent with the <a href="https://github.com/xcape-io/ArduinoProps/blob/master/help/Prop.md" target="_blank">Prop class</a> of the <a href="https://github.com/xcape-io/ArduinoProps#arduinoprops-library" target="_blank">ArduinoProps library</a> for Arduino boards.

* `addData(data)`
    -  registers a [PropData](PropData.md) instance to be treated by `sendAllData()` and `sendDataChanges()` methods
* `addPeriodicAction(title, func, time)`
    - add an action `func` to be executed every `time` period (in seconds)
* `sendAllData()`
    - sends the `DATA` message for all registered data
* `sendDataChanges()`
    - sends the `DATA` message for all registered data that value has changed since last call.
* `sendData(data)`
    - send the `data` string in a `DATA` message 
* `sendDone(action)`
    - send the `action` string in a `DONE` message  
* `sendMesg(message, topic=None)`
    - send the `message` string in a `MESG` message to the *outbox* or the `topic` parameter
* `sendOmit(action)`
    - send the `action` string in a `OMIT` message  
* `sendOver(challenge)`
    - send the `challenge` string in a `OVER` message  
* `sendProg(program)`
    - send the `program` string in a `PROG` message  
* `sendRequ(request, topic=None)`
    - send the `request` string in a `REQU` message to the *outbox* or the `topic` parameter

For `send----()` methods see <a href="https://github.com/xcape-io/PyProps/blob/master/PROTOCOL.md" target="_blank">Room Outbox protocol</a>


## Author

**Marie FAURE** (Apr 17th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>