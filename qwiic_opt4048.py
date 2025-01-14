# -------------------------------------------------------------------------------
# qwiic_opt4048.py
#
# Do you like this library? Help support SparkFun. Buy a board!
# * Qwiic 1x1:  https://www.sparkfun.com/products/22638
# * Qwiic Mini: https://www.sparkfun.com/products/22639

# Python library for the SparkFun Qwiic OPT4048 Tristiumulus Color Sensor, available here:
# * https://www.github.com/SparkFun/Qwiic_OPT4048_Py
# -------------------------------------------------------------------------------
# Written by SparkFun Electronics, November, 2023 This python library supports the SparkFun Electroncis Qwiic ecosystem
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# ===============================================================================
# Copyright (c) 2023 SparkFun Electronics
# SPDX-License-Identifier: MIT
# ===============================================================================

import qwiic_i2c

OPT4048_ADDR_HIGH = 0x45
OPT4048_ADDR_SCL = 0x45
OPT4048_ADDR_LOW = 0x44
OPT4048_ADDR_DEF = 0x44
OPT4048_ADDR_SDA = 0x46

OPT4048_DEVICE_ID = 0x821
_DEFAULT_NAME = "Qwiic OPT4048 Color Sensor"
_AVAILABLE_I2C_ADDRESS = [OPT4048_ADDR_LOW, OPT4048_ADDR_HIGH, OPT4048_ADDR_SDA]

class sfe_color_t:
    """!
    Class for storing color data from the OPT4048.
    """

    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.white = 0
        self.counterR = 0
        self.counterG = 0
        self.counterB = 0
        self.counterW = 0
        self.CRCR = 0
        self.CRCG = 0
        self.CRCB = 0
        self.CRCW = 0

class QwOpt4048:
    """!
    QwOpt4048
    """

    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # This matrix is used to convert the ADC values to CIE values.
    cie_matrix = [
        [0.000234892992, -0.0000189652390, 0.0000120811684, 0],
        [0.0000407467441, 0.000198958202, -0.0000158848115, 0.00215],
        [0.0000928619404, -0.0000169739553, 0.000674021520, 0],
        [0, 0, 0, 0],
    ]

    OPT_MATRIX_ROWS = 4
    OPT_MATRIX_COLS = 4

    # Register Map
    SFE_OPT4048_REGISTER_EXP_RES_CH0 = 0x00     # Register for Exponent and Result (MSB) for Channel 0
    SFE_OPT4048_REGISTER_RES_CNT_CRC_CH0 = 0x01 # Register for Result (LSB), Counter, and CRC for Channel 0
    SFE_OPT4048_REGISTER_EXP_RES_CH1 = 0x02     # Register for Exponent and Result (MSB) for Channel 1
    SFE_OPT4048_REGISTER_RES_CNT_CRC_CH1 = 0x03 # Register for Result (LSB), Counter, and CRC for Channel 1
    SFE_OPT4048_REGISTER_EXP_RES_CH2 = 0x04 # Register for Exponent and Result (MSB) for Channel 2
    SFE_OPT4048_REGISTER_RES_CNT_CRC_CH2 = 0x05 # Register for Result (LSB), Counter, and CRC for Channel 2
    SFE_OPT4048_REGISTER_EXP_RES_CH3 = 0x06     # Register for Exponent and Result (MSB) for Channel 3
    SFE_OPT4048_REGISTER_RES_CNT_CRC_CH3 = 0x07 # Register for Result (LSB), Counter, and CRC for Channel 3
    SFE_OPT4048_REGISTER_THRESH_L_EXP_RES = 0x08 # Register for Threshold  Exponent and Result - Low
    SFE_OPT4048_REGISTER_THRESH_H_EXP_RES = 0x09  # Register for Threshold Exponent and Threshold Result - High
    SFE_OPT4048_REGISTER_CONTROL = 0x0A  # Register that controls the main functions of the device.
    SFE_OPT4048_REGISTER_INT_CONTROL = 0x0B  # Register with settings for the interrupt pin.
    SFE_OPT4048_REGISTER_FLAGS = 0x0C  # Register containing various status flags.
    SFE_OPT4048_REGISTER_DEVICE_ID = 0x11  # Register containing the device ID.

    # Enums
    # Range Settings
    RANGE_2KLUX2 = 0x00
    RANGE_4KLUX5 = 0x01
    RANGE_9LUX = 0x02
    RANGE_18LUX = 0x03
    RANGE_36LUX = 0x04
    RANGE_72LUX = 0x05
    RANGE_144LUX = 0x06
    RANGE_AUTO = 0x0C

    # Conversion Settings
    CONVERSION_TIME_600US = 0x00
    CONVERSION_TIME_1MS = 0x01
    CONVERSION_TIME_1MS8 = 0x02
    CONVERSION_TIME_3MS4 = 0x03
    CONVERSION_TIME_6MS5 = 0x04
    CONVERSION_TIME_12MS7 = 0x05
    CONVERSION_TIME_25MS = 0x06
    CONVERSION_TIME_50MS = 0x07
    CONVERSION_TIME_100MS = 0x08
    CONVERSION_TIME_200MS = 0x09
    CONVERSION_TIME_400MS = 0x0A
    CONVERSION_TIME_800MS = 0x0B
    
    # Operation mode settings
    OPERATION_MODE_POWER_DOWN = 0x00
    OPERATION_MODE_AUTO_ONE_SHOT = 0x01
    OPERATION_MODE_ONE_SHOT = 0x02
    OPERATION_MODE_CONTINUOUS = 0x03

    # Fault count settings
    FAULT_COUNT_1 = 0x00
    FAULT_COUNT_2 = 0x01
    FAULT_COUNT_3 = 0x02
    FAULT_COUNT_8 = 0x03

    # Threshold channel settings
    THRESH_CHANNEL_CH0 = 0x00
    THRESH_CHANNEL_CH1 = 0x01
    THRESH_CHANNEL_CH2 = 0x02
    THRESH_CHANNEL_CH3 = 0x03

    # Interrupt settings
    INT_SMBUS_ALERT = 0x00
    INT_DR_NEXT_CHANNEL = 0x01
    INT_DR_ALL_CHANNELS = 0x03

    # Flags Register Shifts/Masks
    FLAGS_SHIFT_OVERLOAD = 3
    FLAGS_SHIFT_CONV_READY = 2
    FLAGS_SHIFT_FLAG_HIGH = 1
    FLAGS_SHIFT_FLAG_LOW = 0

    FLAGS_MASK_OVERLOAD = 0b1 << FLAGS_SHIFT_OVERLOAD
    FLAGS_MASK_CONV_READY = 0b1 << FLAGS_SHIFT_CONV_READY
    FLAGS_MASK_FLAG_HIGH = 0b1 << FLAGS_SHIFT_FLAG_HIGH
    FLAGS_MASK_FLAG_LOW = 0b1 << FLAGS_SHIFT_FLAG_LOW

    # ADC Channel Shifts/Masks
    CH_EXP_RES_SHIFT_EXP = 12
    CH_EXP_RES_SHIFT_RES_MSB = 0

    CH_RES_CNT_CRC_SHIFT_RES_LSB = 8
    CH_RES_CNT_CRC_SHIFT_CNT = 4
    CH_RES_CNT_CRC_SHIFT_CRC = 0

    CH_EXP_RES_MASK_EXP = 0xF << CH_EXP_RES_SHIFT_EXP
    CH_EXP_RES_MASK_RES_MSB = 0xFFF << CH_EXP_RES_SHIFT_RES_MSB

    CH_RES_CNT_CRC_MASK_RES_LSB = 0xFF << CH_RES_CNT_CRC_SHIFT_RES_LSB
    CH_RES_CNT_CRC_MASK_CNT = 0xF << CH_RES_CNT_CRC_SHIFT_CNT
    CH_RES_CNT_CRC_MASK_CRC = 0xF << CH_RES_CNT_CRC_SHIFT_CRC

    def __init__(self, address=None, i2c_driver=None):
        """!
        Initialize the QwOpt4048 device class.

        @param address: The I2C address to use for the device.
        @param i2c_driver: An existing i2c driver object to use (optional).

        @return **Object** The QwOpt4048 device object.
        """
        # Did the user specify an I2C address?
        self.address = self.available_addresses[0] if address is None else address

        # load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    def is_connected(self):
        """!
        Determine if a OPT4048 device is conntected to the system..

        @return **bool** True if the device is connected, otherwise False.
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """

        if self.get_device_id() != OPT4048_DEVICE_ID:
            return False

        return True

    def get_device_id(self):
        """!
        Retrieve the unique device ID of the OPT4048.

        @return **int** Unique device ID.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_DEVICE_ID, 2)

        unique_id = (block[0] << 8) | block[1]

        return unique_id

    def set_basic_setup(self):
        """!
        Configure basic setup for the OPT4048.

        This function sets the range, conversion time, and operation mode to default values.
        It's meant to just get the device up and running with minimal thought from the user.

        @return None
        """
        self.set_range(self.RANGE_36LUX)
        self.set_conversion_time(self.CONVERSION_TIME_200MS)
        self.set_operation_mode(self.OPERATION_MODE_CONTINUOUS)

    def set_range(self, color_range):
        """!
        Set the range of the OPT4048.

        @param int (Must be one of the valid range settings in the RANGE_... enums above) color_range: The desired range to set.

        @return None or -1 on Error
        """

        if color_range < self.RANGE_2KLUX2 or (color_range > self.RANGE_144LUX and color_range != self.RANGE_AUTO):
            return -1
        
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x3C00
        control_reg |= color_range << 10

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_range(self):
        """!
        Retrieve the current range setting of the OPT4048.

        @return **int** Current range setting.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return (control_reg & 0x3C00) >> 10

    def set_conversion_time(self, time):
        """!
        Set the time used to convert light to analog values. Longer times result in more accurate
        readings.

        @param int time: The desired conversion time to set.

        @return None
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x03C0
        control_reg |= time << 6

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_conversion_time(self):
        """!
        Gets the time used to convert light to analog values. Longer times result in more accurate
        readings.

        @return **int** Current conversion time setting.
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return (control_reg & 0x03C0) >> 6

    def set_qwake(self, enable=True):
        """!
        Sets the quick wake bit for the OPT4048. When enabled, not all systems are put into
        deep sleep when the device is set to this mode, resulting in faster wake times.

        @param bool enable: Enable or disable quick wake.
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x8000
        control_reg |= enable << 15

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_qwake(self):
        """!
        Retrieve the quick wake bit for the OPT4048. When enabled, not all systems are put into
        deep sleep when the device is set to this mode, resulting in faster wake times.

        @return **int** Quick wake bit.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return (control_reg & 0x8000) >> 15

    def set_operation_mode(self, mode):
        """!
        Set the operation mode of the OPT4048: Power-down, Forced auto-range, one-shot, or continuous.

        @param int mode: The desired operation mode to set.

        @return None
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x0030
        control_reg |= mode << 4

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_operation_mode(self):
        """!
        Retrieve the current operation mode of the OPT4048.

        @return **int** Current operation mode.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return (control_reg & 0x0030) >> 4

    def set_int_latch(self, enable=True):
        """!
        Set the interrupt latch of the OPT4048. When enabled, the interrupt pin will remain active
        until the interrupt register is read.

        @param bool enable: Enable or disable interrupt latch.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x0008
        control_reg |= enable << 3

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock( self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_int_latch(self):
        """!
        Retrieve the interrupt latch of the OPT4048. When enabled, the interrupt pin will remain active
        until the interrupt register is read.

        @return **bool** Interrupt latch.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return control_reg & 0x0008

    def set_int_active_high(self, enable=True):
        """!
        Set the interrupt polarity of the OPT4048. When enabled, the interrupt pin is active high.

        @param bool enable: Enable or disable interrupt polarity.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x0004
        control_reg |= enable << 2

        block_out = [0, 0]
        block_out[0] = control_reg >> 8
        block_out[1] = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out)

    def get_int_active_high(self):
        """!
        Retrieve the interrupt polarity of the OPT4048. When enabled, the interrupt pin is active high.

        @return **bool** Interrupt polarity.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return (control_reg & 0x0004) >> 2

    def set_int_input(self, enable=True):
        """!
        Set the interrupt input of the OPT4048. When enabled, the interrupt pin is used as an input.

        @param bool enable: Enable or disable interrupt input.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]
        int_control_reg &= ~0x0010
        int_control_reg |= enable << 4

        block_out = [0, 0]
        block_out[0] = int_control_reg >> 8
        block_out[1] = int_control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, block_out)

    def get_int_input_enable(self):
        """!
        Retrieve the interrupt input of the OPT4048. When enabled, the interrupt pin is used as an input.

        @return **bool** Interrupt input.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]

        return (int_control_reg & 0x0010) >> 4

    def set_int_mechanism(self, mechanism):
        """!
        Set the interrupt mechanism of the OPT4048: SMBus Alert, INT Pin data ready for next channel,
        or INT Pin data ready for all channels.

        @param bool enable: Enable or disable interrupt mechanism.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]
        int_control_reg &= ~0x000C
        int_control_reg |= mechanism << 2

        block_out = [0, 0]
        block_out[0] = int_control_reg >> 8
        block_out[1] = int_control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, block_out)

    def get_int_mechanism(self):
        """!
        Retrieve the interrupt mechanism of the OPT4048: SMBus Alert, INT Pin data ready for next channel,
        or INT Pin data ready for all channels.

        @return **int** Interrupt mechanism.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]

        return (int_control_reg & 0x000C) >> 2

    def get_all_flags(self):
        """!
        Retrieve all flags of the OPT4048.

        @return **int** All flags of the OPT4048.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_FLAGS, 2)

        return block[0] << 8 | block[1]

    def get_overload_flag(self):
        """!
        Retrieve the flag that indicates the ADC is overloaded.

        @return **bool** Flag that indicates the ADC is overloaded.
        """
        flags = self.get_all_flags()

        return ( flags & self.FLAGS_MASK_OVERLOAD == self.FLAGS_MASK_OVERLOAD )

    def get_conv_ready_flag(self):
        """!
        Retrieve the flag that indicates a conversion is ready to be read.

        @return **bool** Flag that indicates a conversion is ready to be read.
        """
        flags = self.get_all_flags()

        return ( flags & self.FLAGS_MASK_CONV_READY == self.FLAGS_MASK_CONV_READY)

    def get_too_bright_flag(self):
        """!
        Retrieve the flag that indicates lux has is above the current range. This
        is considered a fault and is stored int the fault register.

        @return **bool** Flag that indicates lux is above the current range.
        """
        flags = self.get_all_flags()
        return ( flags & self.FLAGS_MASK_FLAG_HIGH == self.FLAGS_MASK_FLAG_HIGH)

    def get_too_dim_flag(self):
        """!
        Retrieve the flag that indicates lux has is below the current range. This
        is considered a fault and is stored int the fault register.

        @return **bool** Flag that indicates lux is below the current range.
        """
        flags = self.get_all_flags()
        return ( flags & self.FLAGS_MASK_FLAG_LOW == self.FLAGS_MASK_FLAG_LOW)

    def set_fault_count(self, count):
        """!
        Set the number of faults needed to trigger an interupt.

        @param int count: Number of faults needed to trigger an interupt.

        @return None
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]
        control_reg &= ~0x0003
        control_reg |= count

        block_out = [0, 0]
        block_out = control_reg >> 8
        block_out = control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, block_out )

    def get_fault_count(self):
        """!
        Retrieve the number of faults that have been triggered.

        @return **int** Number of faults that have been triggered.
        """

        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_CONTROL, 2)

        control_reg = (block[0] << 8) | block[1]

        return control_reg & 0x0003

    def set_threshold_low(self, thresh):
        """!
        Set the low interrupt threshold value of the OPT4048.

        @param int thresh: Low interrupt threshold value.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES, 2)

        thresh_reg = (block[0] << 8) | block[1]
        thresh_reg &= ~0xF000
        thresh_reg |= thresh << 12

        block_out = [0, 0]
        block_out[0] = thresh_reg >> 8
        block_out[1] = thresh_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES, block_out)

    def get_threshold_low(self):
        """!
        Retrieve the low interrupt threshold value of the OPT4048.

        @return **int** Low interrupt threshold value.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES, 2)

        thresh_reg = (block[0] << 8) | block[1]

        return thresh_reg >> 12

    def set_threshold_high(self, thresh):
        """!
        Set the high interrupt threshold value of the OPT4048.

        @param int thresh: High interrupt threshold value.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES, 2)

        thresh_reg = (block[0] << 8) | block[1]
        thresh_reg &= ~0xF000
        thresh_reg |= thresh << 12

        block_out = [0, 0]
        block_out[0] = thresh_reg >> 8
        block_out[1] = thresh_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES, block_out)

    def get_threshold_high(self):
        """!
        Retrieve the high interrupt threshold value of the OPT4048.

        @return **int** High interrupt threshold value.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES, 2)

        thresh_reg = (block[0] << 8) | block[1]

        return thresh_reg >> 12

    def set_i2c_burst(self, enable=True):
        """!
        Set the I2C burst setting of the OPT4048: auto-increment or single register I2C reads.

        @param bool enable: Enable or disable I2C burst setting.

        @return None
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]
        int_control_reg &= ~0x0001
        int_control_reg |= enable

        block_out = [0, 0]
        block_out = int_control_reg >> 8
        block_out = int_control_reg & 0x00FF

        self._i2c.writeBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, block_out)

    def get_i2c_burst(self):
        """!
        Retrieve the I2C burst setting of the OPT4048: auto-increment or single register I2C reads.
        On by default.

        @return **bool** I2C burst setting.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_INT_CONTROL, 2)

        int_control_reg = (block[0] << 8) | block[1]

        return int_control_reg & 0x0001

    def get_adc_ch0(self):
        """!
        Retrieve the ADC value of channel 0 of the OPT4048.

        @return **int** ADC value of channel 0.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_EXP_RES_CH0, 4)
        
        return self.get_adc_code(block)

    def get_adc_code(self, bytes):
        """!
        Calculate the ADC code from the 2 words read from an ADC register

        @param list of int bytes: The resulting list of doing a 4 byte block read from an ADC register.

        @return ADC code.
        """
        adc_reg_word = (bytes[0] << 8) | bytes[1]
        adc1_reg_word = (bytes[2] << 8) | bytes[3]

        result_msb = (adc_reg_word & self.CH_EXP_RES_MASK_RES_MSB) >> self.CH_EXP_RES_SHIFT_RES_MSB
        result_lsb = (adc1_reg_word & self.CH_RES_CNT_CRC_MASK_RES_LSB) >> self.CH_RES_CNT_CRC_SHIFT_RES_LSB

        exponent = (adc_reg_word & self.CH_EXP_RES_MASK_EXP) >> self.CH_EXP_RES_SHIFT_EXP

        mantissa = (result_msb << 8) | result_lsb

        adc_code = mantissa << exponent

        return adc_code

    def get_adc_counter(self, bytes):
        """!
        Calculate the ADC counter from the 2 words read from an ADC register

        @param list of int bytes: The resulting list of doing a 4 byte block read from an ADC register.

        @return ADC counter.
        """
        adc1_reg_word = (bytes[2] << 8) | bytes[3]

        return (adc1_reg_word & self.CH_RES_CNT_CRC_MASK_CNT) >> self.CH_RES_CNT_CRC_SHIFT_CNT

    def get_adc_crc(self, bytes):
        """!
        Calculate the ADC CRC from the 2 words read from an ADC register

        @param list of int bytes: The resulting list of doing a 4 byte block read from an ADC register.

        @return ADC CRC.
        """
        adc1_reg_word = (bytes[2] << 8) | bytes[3]

        return (adc1_reg_word & self.CH_RES_CNT_CRC_MASK_CRC) >> self.CH_RES_CNT_CRC_SHIFT_CRC

    def get_adc_ch1(self):
        """!
        Retrieve the ADC value of channel 1 of the OPT4048.

        @return **int** ADC value of channel 1.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_EXP_RES_CH1, 4)
        
        return self.get_adc_code(block)

    def get_adc_ch2(self):
        """!
        Retrieve the ADC value of channel 2 of the OPT4048.

        @return **int** ADC value of channel 2.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_EXP_RES_CH2, 4)
        
        return self.get_adc_code(block)
    
    def get_adc_ch3(self):
        """!
        Retrieve the ADC value of channel 3 of the OPT4048.

        @return **int** ADC value of channel 3.
        """
        block = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_EXP_RES_CH3, 4)
        
        return self.get_adc_code(block)

    def get_all_adc(self):
        """!
        Retrieve the ADC values of all channels of the OPT4048.

        @return **sfe_color_t** ADC values of all channels.
        """
        color = sfe_color_t()
        color.red = self.get_adc_ch0()
        color.green = self.get_adc_ch1()
        color.blue = self.get_adc_ch2()
        color.white = self.get_adc_ch3()

        return color

    def get_all_channel_data(self, color):
        """!
        Retrieve the ADC values of all channels of the OPT4048.

        @param sfe_color_t color: Color data object to store the ADC values.

        @return **sfe_color_t** ADC values of all channels.
        """
        buff = self._i2c.readBlock(self.address, self.SFE_OPT4048_REGISTER_EXP_RES_CH0, 16)

        color.red = self.get_adc_code(buff[0:4])
        color.green = self.get_adc_code(buff[4:8])
        color.blue = self.get_adc_code(buff[8:12])
        color.white = self.get_adc_code(buff[12:16])

        color.counterR = self.get_adc_counter(buff[0:4])
        color.counterG = self.get_adc_counter(buff[4:8])
        color.counterB = self.get_adc_counter(buff[8:12])
        color.counterW = self.get_adc_counter(buff[12:16])

        color.CRCR = self.get_adc_crc(buff[0:4])
        color.CRCG = self.get_adc_crc(buff[4:8])
        color.CRCB = self.get_adc_crc(buff[8:12])
        color.CRCW = self.get_adc_crc(buff[12:16])

        return color

    def get_lux(self):
        """!
        Retrieve the Lux value of the OPT4048.

        @return **float** Lux value.
        """
        adc_ch1 = self.get_adc_ch1()

        return adc_ch1 * self.cie_matrix[1][3]

    def get_CIEx(self):
        """!
        Retrieve the CIEx value of the OPT4048.

        @return **float** CIEx value.
        """
        x, y, z = 0, 0, 0
        color = sfe_color_t()

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        if (x + y + z) == 0:
            return 0

        # Calculate the CIE x value, all of the
        # math required to do this is in the datasheet.
        return x / (x + y + z)

    def get_CIEy(self):
        """!
        Retrieve the CIEy value of the OPT4048.

        @return **float** CIEy value.
        """
        x, y, z = 0, 0, 0
        color = sfe_color_t()

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        if (x + y + z) == 0:
            return 0

        # Calculate the CIE y value, all of the
        # math required to do this is in the datasheet.
        return y / (x + y + z)

    def get_CCT(self):
        """!
        Retrieve the CCT value of the OPT4048.

        @return **float** CCT value.
        """
        x, y, z = 0, 0, 0
        color = sfe_color_t()

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        if (x + y + z) == 0:
            return 0

        CIEx = x / (x + y + z)
        CIEy = y / (x + y + z)

        # Calculate the correlated color temperature, all of the
        # math required to do this is in the datasheet.
        n = (CIEx - 0.3320) / (0.1858 - CIEy)

        CCT = 432 * n**3 + 3601 * n**2 + 6861 * n + 5517

        return CCT
