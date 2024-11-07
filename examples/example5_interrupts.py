#!/usr/bin/env python
# -------------------------------------------------------------------------------
# example5_interrupts.py
#
# This example shows the functions for modifying the interrupt pin on the OPT4048 Color Sensor.
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
# Name: OPT4048.py
# ===============================================================================

import qwiic_opt4048
import sys
import time

def runExample():
    print("\nExample 5 - Interrupts\n")

    # Create instance of device
    myColor = qwiic_opt4048.QwOpt4048()

    # Check if it's connected
    if myColor.is_connected() is False:
        print(
            "The device isn't connected to the system. Please check your connection or that you have the correct address selected.",
            file=sys.stderr,
        )
        return

    if myColor.begin() is False:
        print(
            "Could not communicate with the Sensor, is the correct address selected?",
            file=sys.stderr,
        )
        return

    myColor.set_basic_setup()

    # Basic usage: if interrupt is set to latched mode
    # myColor.setIntLatch();

    # Select the channel that will fire the interrupt
    # Lux values are generated in Channel One.
    myColor.set_int_mechanism(myColor.INT_DR_ALL_CHANNELS)

    # Change the interrupt direction to active LOW, HIGH is default
    # myColor.set_int_active_high(False)

    # Change the interrupt to an INPUT to trigger measurements
    # set operation mode to one shot mode in this case.
    # myColor.set_int_input()

    while True:
        print(
            "CIEx: %f, CIEy: %f, CCT: %fK"
            % (myColor.get_CIEx(), myColor.get_CIEy(), myColor.get_CCT())
        )
        # Delay time is set to the conversion time * number of channels
        # You need three channels for color sensing @ 200ms conversion time = 600ms.
        time.sleep(0.6)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
