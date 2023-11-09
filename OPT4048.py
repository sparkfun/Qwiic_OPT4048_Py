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

    # Add other methods here...

    def get_cct(self):
        CIEx = self.get_CIEx()
        CIEy = self.get_CIEy()

        n = (CIEx - 0.3320) / (0.1858 - CIEy)

        CCT = 432 * n**3 + 3601 * n**2 + 6861 * n + 5517

        return CCT
