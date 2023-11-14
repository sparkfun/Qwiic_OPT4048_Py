#!/usr/bin/env python
# -------------------------------------------------------------------------------
# qwiic_template_ex1_title.py TODO: replace template and title
#
# TODO: Add description for this example
# -------------------------------------------------------------------------------
# Written by SparkFun Electronics, TODO: month and year
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
# ===============================================================================
# Copyright (c) 2023 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===============================================================================

import OPT4048  # TODO Import correct package
import sys
import time


def runExample():
    # TODO Replace template and title
    print("\nQwiic Template Example 1 - Title\n")

    # Create instance of device
    myColor = OPT4048.QwOpt4048()  # TODO update as needed

    # Check if it's connected
    if myColor.is_connected() is False:
        print(
            "The device isn't connected to the system. Please check your connection",
            file=sys.stderr,
        )
        return

    # Initialize the device
    myColor.begin()


    myColor.set_basic_setup()
    
    print("Ciex: ")
    print(myColor.get_CIEx())
    print("Ciey: ")
    print(myColor.get_CIEy())
    time.sleep(.2)


if __name__ == "__main__":
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
