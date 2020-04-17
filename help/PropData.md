# *PropData* reference
See also:
* <a href="Prop.md" target="_blank">Prop</a> class reference

*PropData* tracks data changes and provides escape room 2.0 propocol `DATA` ready string format.

See [**4. Application protocol for escape room 2.0 prop**](../README.md#4-application-protocol-for-escape-room-20-prop) in [README.md](../README.md).


## Constructor
* `PropData(name, type, initial, decimal=None, precision=1, alias=("1", "0"), logger=None)`
    - `name` is the variable identifier  used in `DATA` messages, it mustr not contains space characters
    - `type` is the data type (see below)
    - `initial` is the data initial value
    - `decimal` is the number of digits for a `float` value
    - `precision` is the precision (in percent, 0.1 for 10%) used to decide that the variable has changed
    - `alias` is a tuple of strings to represent a boolean value (eg. `("yes", "no")`)

Type available for `type` are:
* `bool` for a boolean value which can be substituted by an alias
* `int` for integer
* `float` for a decimal value
    - `decimal` is its number of digits
    - `precision` is its precision to decide that the variable has changed
* `str` for string

## Interface
* `change()`
    - returns the string representation of the object if the variable has been updated since last call; or returns `None`
* `update(value)`
    - update the variable
* `value()`
    - returns the variable value; the value is of the type the `PropData` was constructed

The string representation of the object is the string to send in `DATA` messages.

## Private `__str__()` method
This Python classic method returns the string representation of the object.


## Author

**Marie FAURE** (Apr 17th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>