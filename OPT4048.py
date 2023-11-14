from dataclasses import dataclass
import qwiic_i2c
import OPT4048_Registers

OPT4048_ADDR_HIGH = 0x45
OPT4048_ADDR_SCL = 0x45
OPT4048_ADDR_LOW = 0x44
OPT4048_ADDR_DEF = 0x44
OPT4048_ADDR_SDA = 0x46

OPT4048_DEVICE_ID = 0x2084
_DEFAULT_NAME = "Qwiic OPT4048"
_AVAILABLE_I2C_ADDRESS = [OPT4048_ADDR_LOW, OPT4048_ADDR_HIGH, OPT4048_ADDR_SDA]


@dataclass
class SFEColor:
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 0
    counterR: int = 0
    counterG: int = 0
    counterB: int = 0
    counterW: int = 0
    CRCR: int = 0
    CRCG: int = 0
    CRCB: int = 0
    CRCW: int = 0


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
    # Return Types and Parameter Arguements
    sfe_color_t = SFEColor()

    # Union for register contents
    opt4048_register_exp_res_ch0 = OPT4048_Registers.opt4048_reg_exp_res_ch0_t()
    opt4048_register_res_cnt_crc_ch0 = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch0_t()
    opt4048_reg_exp_res_ch1 = OPT4048_Registers.opt4048_reg_exp_res_ch1_t()
    opt4048_reg_res_cnt_crc_ch1 = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch1_t()
    opt4048_reg_exp_res_ch2 = OPT4048_Registers.opt4048_reg_exp_res_ch2_t()
    opt4048_reg_res_cnt_crc_ch2 = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch2_t()
    opt4048_reg_exp_res_ch3 = OPT4048_Registers.opt4048_reg_exp_res_ch3_t()
    opt4048_reg_res_cnt_crc_ch3 = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch3_t()
    opt4048_reg_thresh_exp_res_low = (
        OPT4048_Registers.opt4048_reg_thresh_exp_res_low_t()
    )
    opt4048_reg_thresh_exp_res_high = (
        OPT4048_Registers.opt4048_reg_thresh_exp_res_high_t()
    )
    opt4048_reg_control = OPT4048_Registers.opt4048_reg_control_t()
    opt4048_reg_int_control = OPT4048_Registers.opt4048_reg_int_control_t()
    opt4048_reg_flags = OPT4048_Registers.opt4048_reg_flags_t()
    opt4048_reg_device_id = OPT4048_Registers.opt4048_reg_device_id_t()

    cie_matrix = [
        [0.000234892992, -0.0000189652390, 0.0000120811684, 0],
        [0.0000407467441, 0.000198958202, -0.0000158848115, 0.00215],
        [0.0000928619404, -0.0000169739553, 0.000674021520, 0],
        [0, 0, 0, 0],
    ]

    OPT_MATRIX_ROWS = 4
    OPT_MATRIX_COLS = 4

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
        Determine if a OPT4048 device is conntected to the system..

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
        unique_id = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_DEVICE_ID
        )

        return unique_id

    def set_basic_setup(self):
        self.set_range(OPT4048_Registers.opt4048RangeT.RANGE_36LUX)
        self.set_conversion_time(
            OPT4048_Registers.opt4048ConversionTimeT.CONVERSION_TIME_200MS
        )
        self.set_operation_mode(
            OPT4048_Registers.opt4048OperationModeT.OPERATION_MODE_CONTINUOUS
        )

    def set_range(self, range):
        reg = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        self.opt4048_reg_control.word = reg
        self.opt4048_reg_control.range = range

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            self.opt4048_reg_control.word,
        )

    def get_range(self):
        reg = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        self.opt4048_reg_control.word = reg

        return self.opt4048_reg_control.range

    def set_conversion_time(self, time):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.conversion_time = time

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_conversion_time(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.conversion_time

    def set_qwake(self, enable):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.qwake = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_qwake(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.qwake

    def set_operation_mode(self, mode):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.op_mode = mode

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_operation_mode(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.op_mode

    def set_int_latch(self, enable):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.latch = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_int_latch(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.latch

    def set_int_active_high(self, enable):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.int_pol = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_int_active_high(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.int_pol

    def set_int_input(self, enable):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        int_control_reg.int_dir = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL,
            int_control_reg.word,
        )

    def get_int_input_enable(self):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        return int_control_reg.int_dir

    def set_int_mechanism(self, enable):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        int_control_reg.int_cfg = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL,
            int_control_reg.word,
        )

    def get_int_mechanism(self):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        return int_control_reg.int_cfg

    def get_all_flags(self):
        flag_reg = OPT4048_Registers.opt4048_reg_flags_t()

        flag_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_FLAGS
        )

        return flag_reg.word

    def get_overload_flag(self):
        flag_reg = OPT4048_Registers.opt4048_reg_flags_t()

        flag_reg.word = self.get_all_flags()

        return flag_reg.overload_flag

    def get_conv_ready_falg(self):
        flag_reg = OPT4048_Registers.opt4048_reg_flags_t()

        flag_reg.word = self.get_all_flags()

        return flag_reg.conv_ready_flag

    def get_too_bright_flag(self):
        flag_reg = OPT4048_Registers.opt4048_reg_flags_t()

        flag_reg.word = self.get_all_flags()

        return flag_reg.flag_high

    def get_too_dim_flag(self):
        flag_reg = OPT4048_Registers.opt4048_reg_flags_t()

        flag_reg.word = self.get_all_flags()

        return flag_reg.flag_low

    def set_fault_count(self, count):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        control_reg.fault_count = count

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL,
            control_reg.word,
        )

    def get_fault_count(self):
        control_reg = OPT4048_Registers.opt4048_reg_control_t()

        control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_CONTROL
        )

        return control_reg.fault_count

    def set_threshold_low(self, thresh):
        thresh_reg = OPT4048_Registers.opt4048_reg_thresh_exp_res_low_t()

        thresh_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES
        )

        thresh_reg.thresh_exp = thresh

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES,
            thresh_reg.word,
        )

    def get_threshold_low(self):
        thresh_reg = OPT4048_Registers.opt4048_reg_thresh_exp_res_low_t()

        thresh_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_L_EXP_RES
        )

        return thresh_reg.thresh_exp

    def set_threshold_high(self, thresh):
        thresh_reg = OPT4048_Registers.opt4048_reg_thresh_exp_res_high_t()

        thresh_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES
        )

        thresh_reg.thresh_exp = thresh

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES,
            thresh_reg.word,
        )

    def get_threshold_high(self):
        thresh_reg = OPT4048_Registers.opt4048_reg_thresh_exp_res_high_t()

        thresh_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_THRESH_H_EXP_RES
        )

        return thresh_reg.thresh_exp

    def set_i2c_burst(self, enable):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        int_control_reg.i2c_burst = enable

        self._i2c.writeWord(
            self.address,
            OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL,
            int_control_reg.word,
        )

    def get_i2c_burst(self):
        int_control_reg = OPT4048_Registers.opt4048_reg_int_control_t()

        int_control_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_INT_CONTROL
        )

        return int_control_reg.i2c_burst

    def get_adc_ch0(self):
        adc_code = 0
        mantissa = 0

        adc_reg = OPT4048_Registers.opt4048_reg_exp_res_ch0_t()
        adc1_reg = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch0_t()

        adc_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_EXP_RES_CH0
        )
        adc1_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_RES_CNT_CRC_CH0
        )

        mantissa = (adc_reg.result_msb_ch0 << 8) | adc1_reg.result_lsb_ch0

        adc_code = mantissa << adc_reg.exponent_ch0

        return adc_code

    def get_adc_ch1(self):
        adc_code = 0
        mantissa = 0

        adc_reg = OPT4048_Registers.opt4048_reg_exp_res_ch1_t()
        adc1_reg = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch1_t()

        adc_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_EXP_RES_CH1
        )
        adc1_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_RES_CNT_CRC_CH1
        )

        mantissa = (adc_reg.result_msb_ch1 << 8) | adc1_reg.result_lsb_ch1

        adc_code = mantissa << adc_reg.exponent_ch1

        return adc_code

    def get_adc_ch2(self):
        adc_code = 0
        mantissa = 0

        adc_reg = OPT4048_Registers.opt4048_reg_exp_res_ch2_t()
        adc1_reg = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch2_t()

        adc_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_EXP_RES_CH2
        )
        adc1_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_RES_CNT_CRC_CH2
        )

        mantissa = (adc_reg.result_msb_ch2 << 8) | adc1_reg.result_lsb_ch2

        adc_code = mantissa << adc_reg.exponent_ch2

        return adc_code

    def get_adc_ch3(self):
        adc_code = 0
        mantissa = 0

        adc_reg = OPT4048_Registers.opt4048_reg_exp_res_ch3_t()
        adc1_reg = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch3_t()

        adc_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_EXP_RES_CH3
        )
        adc1_reg.word = self._i2c.readWord(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_RES_CNT_CRC_CH3
        )

        mantissa = (adc_reg.result_msb_ch3 << 8) | adc1_reg.result_lsb_ch3

        adc_code = mantissa << adc_reg.exponent_ch3

        return adc_code

    def get_all_adc(self):
        color = self.sfe_color_t
        color.red = self.get_adc_ch0()
        color.green = self.get_adc_ch1()
        color.blue = self.get_adc_ch2()
        color.white = self.get_adc_ch3()

        return color

    def get_all_channel_data(self, color):
        buff = bytearray()

        adc0_msb = OPT4048_Registers.opt4048_reg_exp_res_ch0_t()
        adc0_lsb = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch0_t()

        adc1_msb = OPT4048_Registers.opt4048_reg_exp_res_ch1_t()
        adc1_lsb = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch1_t()

        adc2_msb = OPT4048_Registers.opt4048_reg_exp_res_ch2_t()
        adc2_lsb = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch2_t()

        adc3_msb = OPT4048_Registers.opt4048_reg_exp_res_ch3_t()
        adc3_lsb = OPT4048_Registers.opt4048_reg_res_cnt_crc_ch3_t()

        buff = self._i2c.readBlock(
            self.address, OPT4048_Registers.SFE_OPT4048_REGISTER_EXP_RES_CH0, 16
        )

        adc0_msb.word = (buff[0] << 8) | buff[1]
        adc0_lsb.word = (buff[2] << 8) | buff[3]

        adc1_msb.word = (buff[4] << 8) | buff[5]
        adc1_lsb.word = (buff[6] << 8) | buff[7]

        adc2_msb.word = (buff[8] << 8) | buff[9]
        adc2_lsb.word = (buff[10] << 8) | buff[11]

        adc3_msb.word = (buff[12] << 8) | buff[13]
        adc3_lsb.word = (buff[14] << 8) | buff[15]

        mantissa_ch0 = (adc0_msb.result_msb_ch0 << 8) | adc0_lsb.result_lsb_ch0
        adc_code_ch0 = mantissa_ch0 << adc0_msb.exponent_ch0

        mantissa_ch1 = (adc1_msb.result_msb_ch1 << 8) | adc1_lsb.result_lsb_ch1
        adc_code_ch1 = mantissa_ch1 << adc1_msb.exponent_ch1

        mantissa_ch2 = (adc2_msb.result_msb_ch2 << 8) | adc2_lsb.result_lsb_ch2
        adc_code_ch2 = mantissa_ch2 << adc2_msb.exponent_ch2

        mantissa_ch3 = (adc3_msb.result_msb_ch3 << 8) | adc3_lsb.result_lsb_ch3
        adc_code_ch3 = mantissa_ch3 << adc3_msb.exponent_ch3

        color.red = adc_code_ch0
        color.green = adc_code_ch1
        color.blue = adc_code_ch2
        color.white = adc_code_ch3

        color.counterR = adc0_lsb.counter_ch0
        color.counterG = adc1_lsb.counter_ch1
        color.counterB = adc2_lsb.counter_ch2
        color.counterW = adc3_lsb.counter_ch3

        color.CRCR = adc0_lsb.crc_ch0
        color.CRCG = adc1_lsb.crc_ch1
        color.CRCB = adc2_lsb.crc_ch2
        color.CRCW = adc3_lsb.crc_ch3

        return color

    def get_lux(self):
        adc_ch1 = self.get_adc_ch1()

        return adc_ch1 * self.cie_matrix[1][3]

    def get_CIEx(self):
        x, y, z = 0, 0, 0
        color = self.sfe_color_t

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        return x / (x + y + z)

    def get_CIEy(self):
        x, y, z = 0, 0, 0
        color = self.sfe_color_t

        self.get_all_channel_data(color)

        for row in range(self.OPT_MATRIX_ROWS):
            x += color.red * self.cie_matrix[row][0]
            y += color.green * self.cie_matrix[row][1]
            z += color.blue * self.cie_matrix[row][2]

        return y / (x + y + z)

    def get_cct(self):
        CIEx = self.get_CIEx()
        CIEy = self.get_CIEy()

        n = (CIEx - 0.3320) / (0.1858 - CIEy)

        CCT = 432 * n**3 + 3601 * n**2 + 6861 * n + 5517

        return CCT
