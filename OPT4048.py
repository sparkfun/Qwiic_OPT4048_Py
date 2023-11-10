from dataclasses import dataclass
import qwiic_i2c
import time
import OPT4048_Register.py


@dataclass
class SFEColor:
    red : int = 0
    green : int = 0
    blue : int = 0
    white : int = 0
    counterR : int = 0
    counterG : int = 0
    counterB : int = 0
    counterW : int = 0
    CRCR : int = 0
    CRCG : int = 0
    CRCB : int = 0
    CRCW : int = 0


class CRCBits:
    def __init__(self):
        self.bit0 = 0
        self.bit1 = 0
        self.bit2 = 0
        self.bit3 = 0


class ExponBits:
    def __init__(self):
        self.bit0 = 0
        self.bit1 = 0
        self.bit2 = 0
        self.bit3 = 0


class MantissaBits:
    def __init__(self):
        self.bit0 = 0
        self.bit1 = 0
        self.bit2 = 0
        self.bit3 = 0
        self.bit4 = 0
        self.bit5 = 0
        self.bit6 = 0
        self.bit7 = 0
        self.bit8 = 0
        self.bit9 = 0
        self.bit10 = 0
        self.bit11 = 0
        self.bit12 = 0
        self.bit13 = 0
        self.bit14 = 0
        self.bit15 = 0
        self.bit16 = 0
        self.bit17 = 0
        self.bit18 = 0
        self.bit19 = 0

class QwOpt4048:

    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
    
    self.opt4048_range_t = opt4048RangeT
    self.opt4048_conversion_time_t = opt4048ConversionTimeT
    self.opt4048_operation_mode_t = opt4048OperationModeT
    self.sfe_color_t = SFEColor
    
    self.opt4048_reg_control = 

    def __init__(self, address=None, i2c_driver=None):

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
        """
            Determine if a BME280 device is conntected to the system..

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):

        if self.get_device_id() != OPT4048_DEVICE_ID:
            return False

        return True


    def get_device_id(self):

        unique_id = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_DEVICE_ID)

        return unique_id

    def set_basic_setup(self):
        self.set_range(opt4048_range_t.RANGE_36LUX)
        self.set_conversion_time(opt4048_range_t.CONVERSION_TIME_200MS)
        self.set_operation_mode(opt4048_range_t.OPERATION_MODE_CONTINUOUS)

    def set_range(self, range):

        reg_range = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        buff[0] = controlReg.word >> 8
        buff[1] = controlReg.word

        retVal = self._i2c.writeWord(SFE_OPT4048_REGISTER_CONTROL)

        if retVal != 0:
            return False

        return True

    def get_range(self):
        buff = [0, 0]
        controlReg = opt4048_reg_control_t()

        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        controlReg.word = (buff[0] << 8) | buff[1]

        return opt4048_range_t(controlReg.range)

    def set_conversion_time(self, time):
        buff = bytearray([0, 0])
        retVal = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if retVal != 0:
            return False

        controlReg = (buff[0] << 8) | buff[1]

        controlReg &= ~(0xF00)  # Clear the conversion time bits
        controlReg |= (time << 8)  # Set the new conversion time bits

        buff[0] = controlReg >> 8
        buff[1] = controlReg & 0xFF

        retVal = self.writeRegisterRegion(SFE_OPT4048_REGISTER_CONTROL

        if retVal != 0:
            return False

        return True

    def get_conversion_time(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        controlReg = (buff[0] << 8) | buff[1]

        return (controlReg >> 8) & 0xF

    def set_qwake(self, enable):
        buff = bytearray([0, 0])
        retVal = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if retVal != 0:
            return False

        controlReg = (buff[0] << 8) | buff[1]

        if enable:
            controlReg |= (1 << 0)  # Set Qwake bit
        else:
            controlReg &= ~(1 << 0)  # Clear Qwake bit

        buff[0] = controlReg >> 8
        buff[1] = controlReg & 0xFF

        retVal = self.writeRegisterRegion(SFE_OPT4048_REGISTER_CONTROL

        if retVal != 0:
            return False

        return True

    def get_qwake(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        controlReg = (buff[0] << 8) | buff[1]

        return (controlReg & 0x01) == 1

    def set_operation_mode(self, mode):
        buff = bytearray([0, 0])
        retVal = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if retVal != 0:
            return False

        controlReg = (buff[0] << 8) | buff[1]

        controlReg &= ~(0x30)  # Clear the operation mode bits
        controlReg |= (mode << 4)  # Set the new operation mode bits

        buff[0] = controlReg >> 8
        buff[1] = controlReg & 0xFF

        retVal = self.writeRegisterRegion(SFE_OPT4048_REGISTER_CONTROL

        if retVal != 0:
            return False

        return True

    def get_operation_mode(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        controlReg = (buff[0] << 8) | buff[1]

        return (controlReg >> 4) & 0x03

    def set_int_latch(self, enable):
        buff = bytearray([0, 0])
        ret_val = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if ret_val != 0:
            return False

        control_reg = (buff[0] << 8) | buff[1]
        control_reg = control_reg & 0xfffe | enable

        buff[0] = control_reg >> 8
        buff[1] = control_reg

        ret_val = self._i2c.writeWord(SFE_OPT4048_REGISTER_CONTROL

        if ret_val != 0:
            return False

        return True

    def get_int_latch(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        control_reg = (buff[0] << 8) | buff[1]

        return control_reg & 0x0001 == 1

    def set_int_active_high(self, enable):
        buff = bytearray([0, 0])
        ret_val = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if ret_val != 0:
            return False

        int_reg = (buff[0] << 8) | buff[1]
        int_reg = int_reg & 0xfffd | (enable << 1)

        buff[0] = int_reg >> 8
        buff[1] = int_reg

        ret_val = self._i2c.writeWord(SFE_OPT4048_REGISTER_CONTROL

        if ret_val != 0:
            return False

        return True

    def get_int_active_high(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        int_reg = (buff[0] << 8) | buff[1]

        return (int_reg & 0x0002) >> 1 == 1

    def set_int_input(self, enable):
        buff = bytearray([0, 0])
        ret_val = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        if ret_val != 0:
            return False

        int_reg = (buff[0] << 8) | buff[1]
        int_reg = int_reg & 0xfffd | (enable << 1)

        buff[0] = int_reg >> 8
        buff[1] = int_reg

        ret_val = self._i2c.writeWord(SFE_OPT4048_REGISTER_INT_CONTROL

        if ret_val != 0:
            return False

        return True

    def get_int_input_enable(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        int_reg = (buff[0] << 8) | buff[1]

        return (int_reg & 0x0002) >> 1 == 1

    def set_int_mechanism(self, mechanism):
        buff = bytearray([0, 0])
        ret_val = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        if ret_val != 0:
            return False

        int_reg = (buff[0] << 8) | buff[1]

        int_reg &= ~(0b11 << 2)
        int_reg |= (mechanism << 2)

        buff[0] = int_reg >> 8
        buff[1] = int_reg

        ret_val = self._i2c.writeWord(SFE_OPT4048_REGISTER_INT_CONTROL

        if ret_val != 0:
            return False

        return True


    def get_int_mechanism(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        int_reg = (buff[0] << 8) | buff[1]

        return (int_reg >> 2) & 0b11


    def get_all_flags(self):
        buff = bytearray([0, 0])
        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_FLAGS)

        flag_reg = (buff[0] << 8) | buff[1]

        return flag_reg


    def get_overload_flag(self):
        flag_reg = self.get_all_flags()

        return (flag_reg & 0b1000) != 0

    def get_conv_ready_falg(self):
        flagReg = self.get_all_flags()

        if flagReg.conv_ready_flag != 1:
            return False

        return True

    def get_too_bright_flag(self):
        flagReg = self.get_all_flags()

        if flagReg.flag_high != 1:
            return False

        return True

    def get_too_dim_flag(self):
        flagReg = self.get_all_flags()

        if flagReg.flag_low != 1:
            return False

        return True

    def set_fault_count(self, count):
        buff = [0, 0]
        retVal = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        if retVal != 0:
            return False

        controlReg = (buff[0] << 8) | buff[1]
        controlReg = (controlReg & 0xFFFC) | (count & 0x3)

        buff[0] = (controlReg >> 8) & 0xFF
        buff[1] = controlReg & 0xFF

        retVal = self.writeRegisterRegion(SFE_OPT4048_REGISTER_CONTROL

        if retVal != 0:
            return False

        return True

    def get_fault_count(self):
        buff = [0, 0]
        controlReg = 0

        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_CONTROL)

        controlReg = (buff[0] << 8) | buff[1]

        return controlReg 

    def set_threshold_low(self, thresh):
        if not (2.15 <= thresh <= 144000):
            return False

        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        retVal = self._i2c.writeWord(SFE_OPT4048_REGISTER_THRESH_L_EXP_RES

        if retVal != 0:
            return False

        return True


    def get_threshold_low(self):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        threshReg = opt4048_reg_thresh_exp_res_low_t()

        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_THRESH_L_EXP_RES)

        threshReg.word = (buff[0] << 8) | buff[1]

        thresholdLow = threshReg.thresh_result << threshReg.thresh_exp

        return thresholdLow


    def set_i2c_burst(self, enable):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        retVal = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        if retVal != 0:
            return False

        intReg = opt4048_reg_int_control_t()
        intReg.word = (buff[0] << 8) | buff[1]

        intReg.i2c_burst = int(enable)

        buff[0] = intReg.word >> 8
        buff[1] = intReg.word

        retVal = self._i2c.writeWord(SFE_OPT4048_REGISTER_INT_CONTROL

        if retVal != 0:
            return False

        return True


    def get_i2c_burst(self):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        intReg = opt4048_reg_int_control_t()

        self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_INT_CONTROL)

        intReg.word = (buff[0] << 8) | buff[1]

        if intReg.i2c_burst != 1:
            return False

     def get_ADC_ch0(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_EXP_RES_CH04)
        adc1_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_RES_CNT_CRC_CH04)

        mantissa = (adc_reg.result_msb_ch0 << 8) | adc1_reg.result_lsb_ch0

        adc_code = mantissa << adc_reg.exponent_ch0

        return adc_code

    def get_ADC_ch1(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_EXP_RES_CH14)
        adc1_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_RES_CNT_CRC_CH14)

        mantissa = (adc_reg.result_msb_ch1 << 8) | adc1_reg.result_lsb_ch1

        adc_code = mantissa << adc_reg.exponent_ch1

        return adc_code

    def get_ADC_ch2(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_EXP_RES_CH24)
        adc1_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_RES_CNT_CRC_CH24)

        mantissa = (adc_reg.result_msb_ch2 << 8) | adc1_reg.result_lsb_ch2

        adc_code = mantissa << adc_reg.exponent_ch2

        return adc_code

    def get_ADC_ch3(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_EXP_RES_CH34)
        adc1_reg = self._i2c.readWord(self.address, SFE_OPT4048_REGISTER_RES_CNT_CRC_CH34)

        mantissa = (adc_reg.result_msb_ch3 << 8) | adc1_reg.result_lsb_ch3

        adc_code = mantissa << adc_reg.exponent_ch3

        return adc_code   # Add other methods here...

    def get_all_adc():
        color = self.sfe_color_t()
        color.red = get_adc_ch0()
        color.green = get_adc_ch1()
        color.blue = get_adc_ch2()
        color.white = get_adc_ch3()
        return color


    def get_all_channel_data():
        buff = read_register_region(SFE_OPT4048_REGISTER_EXP_RES_CH0, 16)
        
        adc0MSB = opt4048_reg_exp_res_ch0_t((buff[0] << 8) | buff[1])
        adc0LSB = opt4048_reg_res_cnt_crc_ch0_t((buff[2] << 8) | buff[3])
        
        adc1MSB = opt4048_reg_exp_res_ch1_t((buff[4] << 8) | buff[5])
        adc1LSB = opt4048_reg_res_cnt_crc_ch1_t((buff[6] << 8) | buff[7])
        
        adc2MSB = opt4048_reg_exp_res_ch2_t((buff[8] << 8) | buff[9])
        adc2LSB = opt4048_reg_res_cnt_crc_ch2_t((buff[10] << 8) | buff[11])
        
        adc3MSB = opt4048_reg_exp_res_ch3_t((buff[12] << 8) | buff[13])
        adc3LSB = opt4048_reg_res_cnt_crc_ch3_t((buff[14] << 8) | buff[15])

        mantissa_ch0 = adc0MSB.result_msb_ch0 << 8 | adc0LSB.result_lsb_ch0
        adc_code_ch0 = mantissa_ch0 << adc0MSB.exponent_ch0
        
        mantissa_ch1 = adc1MSB.result_msb_ch1 << 8 | adc1LSB.result_lsb_ch1
        adc_code_ch1 = mantissa_ch1 << adc1MSB.exponent_ch1
        
        mantissa_ch2 = adc2MSB.result_msb_ch2 << 8 | adc2LSB.result_lsb_ch2
        adc_code_ch2 = mantissa_ch2 << adc2MSB.exponent_ch2
        
        mantissa_ch3 = adc3MSB.result_msb_ch3 << 8 | adc3LSB.result_lsb_ch3
        adc_code_ch3 = mantissa_ch3 << adc3MSB.exponent_ch3
        
        color = sfe_color_t(
            red=adc_code_ch0, green=adc_code_ch1, blue=adc_code_ch2, white=adc_code_ch3,
            counterR=adc0LSB.counter_ch0, counterG=adc1LSB.counter_ch1,
            counterB=adc2LSB.counter_ch2, counterW=adc3LSB.counter_ch3,
            CRCR=adc0LSB.crc_ch0, CRCG=adc1LSB.crc_ch1, CRCB=adc2LSB.crc_ch2, CRCW=adc3LSB.crc_ch3
        )

    return color
    def get_lux(self):
        adc_ch1 = self.get_adc_ch1()
        lux = adc_ch1 * self.cie_matrix[1][3]
        return lux

    def get_CIEX(self):
        x, y, z = 0, 0, 0
        cie_x = 0
        color = sfe_color_t()

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        total = x + y + z
        if total != 0:
            cie_x = x / total

        return cie_x

    def get_CIEY(self):
        x, y, z = 0, 0, 0
        cie_y = 0
        color = sfe_color_t()

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        total = x + y + z
        if total != 0:
            cie_y = y / total

        return cie_y

    def get_cct(self):
        CIEx = self.get_CIEx()
        CIEy = self.get_CIEy()

        n = (CIEx - 0.3320) / (0.1858 - CIEy)

        CCT = 432 * n**3 + 3601 * n**2 + 6861 * n + 5517

        return CCT
