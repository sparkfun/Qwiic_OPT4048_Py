#!/usr/bin/env python
# -------------------------------------------------------------------------------
# example2_basic_lux_sensing.py
#
# This example shows the basic operation for reading lux levels of the OPT4048 Color Sensor.
#
# Products:
#     Qwiic 1x1: https://www.sparkfun.com/products/22638
#     Qwiic Mini: https://www.sparkfun.com/products/22639
#
# Repository:
#     https://github.com/sparkfun/Qwiic_OPT4048_Py
# -------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2023
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
# ===============================================================================
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2023 SparkFun Electronics
#
# ===============================================================================

import qwiic_opt4048 
import sys
import time


def runExample():
    print("\nExample 2 - Basic Lux Sensing\n")

    # Create instance of device
    myColor = qwiic_opt4048.QwOpt4048()

    # Check if it's connected
    if myColor.is_connected() is False:
        print(
            "The device isn't connected to the system. Please check your connection or that you have the correct address selected.",
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
        print("Lux: %f" % myColor.get_lux())
        # Delay time is set to the conversion time * number of channels
        # You need one channel for lux sensing @ 200ms conversion time = 200ms.
        time.sleep(0.2)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
