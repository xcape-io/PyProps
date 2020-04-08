# Raspberry Pi Props


## 1. Prepare az ation with latest NOOBS
Prepare a clean SD Card (16GB Class 10 U1 recommended):
* format the SD card with <a href="https://www.sdcard.org/downloads/formatter/" target="_blank">SD Card Formatter</a>

> format the SD card with <a href="https://www.sdcard.org/downloads/formatter/" target="_blank">SD Card Formatter</a>
> > ![SD Card Formatter](assets/format-sdcard.png)

## 1. Preparation with latest NOOBS
At the moment of writting this how-to the current version is NOOBS 3.3.1.

Download NOOBS offline install from https://www.raspberrypi.org/downloads/noobs/ and unzip all files in a clean SD Card (16GB recommended)

1. Boot on NOOBS, choose complete install and proceed
2. Enable VNC and SSH in raspi-config
3. Set passwords:

    ```csharp
    $ passwd
    -> for pi (former is raspberry)
    $ sudo passwd root
    -> for root
    ```
    
4. Update Raspbian:

    ```csharp
    $ sudo apt-get update
    $ sudo apt-get upgrade
    ```
    
5. Add screen 	

    ```csharp
    $ sudo apt-get install screen
    ```

## Author

**Marie FAURE** (Apr 8th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>