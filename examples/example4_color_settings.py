#!/usr/bin/env python
# -------------------------------------------------------------------------------
# example4_color_settings.py
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
# Name: OPT4048.py
# ===============================================================================

import OPT4048
import sys
import time
import OPT4048_Registers as args


def runExample():
    print("\nExample 4 - Color Settings\n")

    # Create instance of device
    myColor = OPT4048.QwOpt4048()

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

    # Possible range settings:
    # RANGE_2KLUX2,
    # RANGE_4KLUX5,
    # RANGE_9LUX,
    # RANGE_18LUX,
    # RANGE_36LUX,
    # RANGE_72LUX,
    # RANGE_144LUX,
    # RANGE_AUTO
    # A higher color range will result in a lower resolution.
    # The RANGE_AUTO option will automatically select the best
    # range for the current light conditions.
    myColor.set_range(args.opt4048RangeT.RANGE_AUTO.value)

    # CONVERSION_TIME_600US,
    # CONVERSION_TIME_1MS,
    # CONVERSION_TIME_1MS8,
    # CONVERSION_TIME_3MS4,
    # CONVERSION_TIME_6MS5,
    # CONVERSION_TIME_12MS7,
    # CONVERSION_TIME_25MS,
    # CONVERSION_TIME_50MS,
    # CONVERSION_TIME_100MS,
    # CONVERSION_TIME_200MS,
    # CONVERSION_TIME_400MS,
    # CONVERSION_TIME_800MS
    # A higher conversion time will result in more precise readings.
    # For color sensing, having the highest converstion time is suggested.
    myColor.set_conversion_time(args.opt4048ConversionTimeT.CONVERSION_TIME_800MS.value)

    # OPERATION_MODE_POWER_DOWN,
    # OPERATION_MODE_AUTO_ONE_SHOT,
    # OPERATION_MODE_ONE_SHOT,
    # OPERATION_MODE_CONTINUOUS
    myColor.set_operation_mode(args.opt4048OperationModeT.OPERATION_MODE_CONTINUOUS.value)

    while True:
        print("Ciex: ")
        print(myColor.get_CIEx())
        print("\n")
        print("Ciey: ")
        print(myColor.get_CIEy())
        print("\n")
        print("Color Warmth: ")
        print(myColor.get_CCT())
        print("K\n")
        # Delay time is set to the conversion time * number of channels
        # You need three channels for color sensing @ 800ms conversion time = 3200ms.
        time.sleep(3.2)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
