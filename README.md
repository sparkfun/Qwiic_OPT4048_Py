Qwiic_OPT4048_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun_Qwiic_OPT4048_py/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_opt4048_tristimulus_color_sensor.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_OPT4048_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_OPT4048_Py.svg" /></a>
	<a href="https://qwiic-buzzer-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/sparkfun_Qwiic_OPT4048_py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_OPT4048_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src=""  align="right" width=300 alt="SparkFun Qwiic Tristimulus Color Sensor OPT4048">


Python module for the [SparkFun OPT4048 Tristiumulus Color Sensor](https://www.sparkfun.com/products/22638) and [SparkFun _Mini_ OPT4048 Tristiumulus Color Sensor](https://www.sparkfun.com/products/22639)

This python package is a port of the existing [SparkFun OPT4048 Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Buzzer_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### :warning: **Using this sensor on a Raspberry Pi**? :warning:
Your system might need modification. See this [note](#raspberry-pi-use).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The qwiic Buzzer Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
<!---
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)
-->

Dependencies 
--------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic Trisitumuls Color Sensor module documentation is hosted at [ReadTheDocs](https://sparkfun_Qwiic_OPT4048_py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun_opt4048_tristimulus_color_sensor](https://pypi.org/project/sparkfun_opt4048_tristimulus_color_sensor/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun_opt4048_tristiumuls_color_sensor
```
For the current user:

```sh
pip install sparkfun_opt4048_tristiumuls_color_sensor
```
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun_opt4048_tristimulus_color_sensor-<version>.tar.gz
```

Raspberry Pi Use
-------------------
For this sensor to work on the Raspberry Pi, I2C clock stretching must be enabled. 

To do this:
- Login as root to the target Raspberry Pi
- Open the file /boot/config.txt in your favorite editor (vi, nano ...etc)
- Scroll down until the block that contains the following is found:
```ini
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=spi=on
```
- Add the following line:
```ini
# Enable I2C clock stretching
dtparam=i2c_arm_baudrate=10000
```
- Save the file
- Reboot the raspberry pi

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
import qwiic_opt4048 
import sys
import time


def runExample():
    print("\nExample 1 - Basic Settings\n")

    # Create instance of device
    myColor = qwiic_opt4048.QwOpt4048()

    # Check if it's connected
    if myColor.is_connected() is False:
        print(
            "The device isn't connected to the system. Please check your connection",
            file=sys.stderr,
        )
        return

    # Initialize the device
    if myColor.begin() is False:
        print(
            "Could not communicate with the Sensor, is the correct address selected?",
            file=sys.stderr,
        )
        return

    myColor.set_basic_setup()

    while True:
        print("CIEx: %f, CIEy: %f" % (myColor.get_CIEx(), myColor.get_CIEy()))
        # Delay time is set to the conversion time * number of channels
        # You need three channels for color sensing @ 200ms conversion time = 600ms.
        time.sleep(0.6)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
