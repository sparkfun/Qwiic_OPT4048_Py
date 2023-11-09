class SFEColor:
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
    def __init__(self):
        self._sfeBus = None
        self._i2cAddress = None
        self.crcEnabled = False

    def init(self):
        if not self._sfeBus.ping(self._i2cAddress):
            return False

        if self.getDeviceID() != OPT4048_DEVICE_ID:
            return False

        return True

    def is_connected(self):
        if self.getDeviceID() != OPT4048_DEVICE_ID:
            return False
        else:
            return True

    def get_device_id(self):
        buff = [0, 0]
        unique_id = 0

        retVal = self.read_register_region(SFE_OPT4048_REGISTER_DEVICE_ID, buff)

        id_reg = ((buff[0] << 8) | buff[1])

        unique_id = (id_reg.DIDH << 2) | id_reg.DIDL

        if retVal != 0:
            return 0

        return unique_id

    def set_communication_bus(self, the_bus, i2c_address):
        self._sfeBus = the_bus
        self._i2cAddress = i2c_address

    def set_communication_bus(self, the_bus):
        self._sfeBus = the_bus

    def write_register_region(self, offset, data, length):
        return self._sfeBus.write_register_region(self._i2cAddress, offset, data, length)

    def read_register_region(self, offset, data, length):
        return self._sfeBus.read_register_region(self._i2cAddress, offset, data, length)

    def set_basic_setup(self):
        self.set_range(RANGE_36LUX)
        self.set_conversion_time(CONVERSION_TIME_200MS)
        self.set_operation_mode(OPERATION_MODE_CONTINUOUS)

    def set_range(self, range):
        buff = [0, 0]
        retVal = self.read_register_region(SFE_OPT4048_REGISTER_CONTROL, buff)

        if retVal != 0:
            return False

        controlReg = ((buff[0] << 8) | buff[1])
        controlReg.range = range

        buff[0] = controlReg.word >> 8
        buff[1] = controlReg.word

        retVal = self.write_register_region(SFE_OPT4048_REGISTER_CONTROL, buff)

        if retVal != 0:
            return False

        return True

    def get_range(self):
        buff = [0, 0]
        controlReg = opt4048_reg_control_t()

        self.read_register_region(SFE_OPT4048_REGISTER_CONTROL, buff)

        controlReg.word = (buff[0] << 8) | buff[1]

        return opt4048_range_t(controlReg.range)

    def getConvReadyFlag(self):
        flagReg = self.getAllFlags()

        if flagReg.conv_ready_flag != 1:
            return False

        return True

    def getTooBrightFlag(self):
        flagReg = self.getAllFlags()

        if flagReg.flag_high != 1:
            return False

        return True

    def getTooDimFlag(self):
        flagReg = self.getAllFlags()

        if flagReg.flag_low != 1:
            return False

        return True

    def setFaultCount(self, count):
        buff = [0, 0]
        retVal = self.readRegisterRegion(SFE_OPT4048_REGISTER_CONTROL, buff)

        if retVal != 0:
            return False

        controlReg = (buff[0] << 8) | buff[1]
        controlReg = (controlReg & 0xFFFC) | (count & 0x3)

        buff[0] = (controlReg >> 8) & 0xFF
        buff[1] = controlReg & 0xFF

        retVal = self.writeRegisterRegion(SFE_OPT4048_REGISTER_CONTROL, buff)

        if retVal != 0:
            return False

        return True

    def getFaultCount(self):
        buff = [0, 0]
        controlReg = 0

        self.readRegisterRegion(SFE_OPT4048_REGISTER_CONTROL, buff)

        controlReg = (buff[0] << 8) | buff[1]

        return controlReg 

    def set_threshold_low(self, thresh):
        if not (2.15 <= thresh <= 144000):
            return False

        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        retVal = self.write_register_region(SFE_OPT4048_REGISTER_THRESH_L_EXP_RES, buff)

        if retVal != 0:
            return False

        return True


    def get_threshold_low(self):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        threshReg = opt4048_reg_thresh_exp_res_low_t()

        self.read_register_region(SFE_OPT4048_REGISTER_THRESH_L_EXP_RES, buff)

        threshReg.word = (buff[0] << 8) | buff[1]

        thresholdLow = threshReg.thresh_result << threshReg.thresh_exp

        return thresholdLow


    def set_i2c_burst(self, enable):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        retVal = self.read_register_region(SFE_OPT4048_REGISTER_INT_CONTROL, buff)

        if retVal != 0:
            return False

        intReg = opt4048_reg_int_control_t()
        intReg.word = (buff[0] << 8) | buff[1]

        intReg.i2c_burst = int(enable)

        buff[0] = intReg.word >> 8
        buff[1] = intReg.word

        retVal = self.write_register_region(SFE_OPT4048_REGISTER_INT_CONTROL, buff)

        if retVal != 0:
            return False

        return True


    def get_i2c_burst(self):
        buff = bytearray([0, 0])  # Assuming buff is of type uint8_t[2]
        intReg = opt4048_reg_int_control_t()

        self.read_register_region(SFE_OPT4048_REGISTER_INT_CONTROL, buff)

        intReg.word = (buff[0] << 8) | buff[1]

        if intReg.i2c_burst != 1:
            return False

     def get_ADC_ch0(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self.read_register_region(SFE_OPT4048_REGISTER_EXP_RES_CH0, buff, 4)
        adc1_reg = self.read_register_region(SFE_OPT4048_REGISTER_RES_CNT_CRC_CH0, buff, 4)

        mantissa = (adc_reg.result_msb_ch0 << 8) | adc1_reg.result_lsb_ch0

        adc_code = mantissa << adc_reg.exponent_ch0

        return adc_code

    def get_ADC_ch1(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self.read_register_region(SFE_OPT4048_REGISTER_EXP_RES_CH1, buff, 4)
        adc1_reg = self.read_register_region(SFE_OPT4048_REGISTER_RES_CNT_CRC_CH1, buff, 4)

        mantissa = (adc_reg.result_msb_ch1 << 8) | adc1_reg.result_lsb_ch1

        adc_code = mantissa << adc_reg.exponent_ch1

        return adc_code

    def get_ADC_ch2(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self.read_register_region(SFE_OPT4048_REGISTER_EXP_RES_CH2, buff, 4)
        adc1_reg = self.read_register_region(SFE_OPT4048_REGISTER_RES_CNT_CRC_CH2, buff, 4)

        mantissa = (adc_reg.result_msb_ch2 << 8) | adc1_reg.result_lsb_ch2

        adc_code = mantissa << adc_reg.exponent_ch2

        return adc_code

    def get_ADC_ch3(self):
        buff = [0] * 4
        adc_code = 0
        mantissa = 0

        adc_reg = self.read_register_region(SFE_OPT4048_REGISTER_EXP_RES_CH3, buff, 4)
        adc1_reg = self.read_register_region(SFE_OPT4048_REGISTER_RES_CNT_CRC_CH3, buff, 4)

        mantissa = (adc_reg.result_msb_ch3 << 8) | adc1_reg.result_lsb_ch3

        adc_code = mantissa << adc_reg.exponent_ch3

        return adc_code   # Add other methods here...

    def get_cct(self):
        CIEx = self.get_CIEx()
        CIEy = self.get_CIEy()

        n = (CIEx - 0.3320) / (0.1858 - CIEy)

        CCT = 432 * n**3 + 3601 * n**2 + 6861 * n + 5517

        return CCT
