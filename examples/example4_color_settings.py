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

    # Initialize the device
    myColor.begin()

    myColor.set_range(args.opt4048RangeT.RANGE_2KLUX2)
    myColor.set_conversion_time(args.opt4048ConversionTimeT.CONVERSION_TIME_800MS)
    myColor.set_conversion_time(args.opt4048ConversionTimeT.CONVERSION_TIME_800MS)
    myColor.set_operation_mode(args.opt4048OperationModeT.OPERATION_MODE_CONTINUOUS)
    
    print("Ciex: ")
    print(myColor.get_CIEx())
    print("\n")
    print("Ciey: ")
    print(myColor.get_CIEy())
    print("\n")
    print("Color Warmth: ")
    print(myColor.get_cct())
    print("K\n")
    time.sleep(.2)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
