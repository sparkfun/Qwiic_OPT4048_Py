# Addresses
OPT4048_ADDR_HIGH = 0x45
OPT4048_ADDR_LOW = 0x44
OPT4048_ADDR_DEF = 0x44
OPT4048_ADDR_SDA = 0x46
OPT4048_ADDR_SCL = 0x45

OPT4048_DEVICE_ID = 0x2084

# Range Settings
class opt4048_range_t:
    RANGE_2KLUX2 = 0x00
    RANGE_4KLUX5 = 0x01
    RANGE_9LUX = 0x02
    RANGE_18LUX = 0x03
    RANGE_36LUX = 0x04
    RANGE_72LUX = 0x05
    RANGE_144LUX = 0x06
    RANGE_AUTO = 0x0C

# Conversion Settings
class opt4048_conversion_time_t:
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
class opt4048_operation_mode_t:
    OPERATION_MODE_POWER_DOWN = 0x00
    OPERATION_MODE_AUTO_ONE_SHOT = 0x01
    OPERATION_MODE_ONE_SHOT = 0x02
    OPERATION_MODE_CONTINUOUS = 0x03

# Fault count settings
class opt4048_fault_count_t:
    FAULT_COUNT_1 = 0x00
    FAULT_COUNT_2 = 0x01
    FAULT_COUNT_3 = 0x02
    FAULT_COUNT_8 = 0x03

# Threshold channel settings
class opt4048_threshold_channel_t:
    THRESH_CHANNEL_CH0 = 0x00
    THRESH_CHANNEL_CH1 = 0x01
    THRESH_CHANNEL_CH2 = 0x02
    THRESH_CHANNEL_CH3 = 0x03

# Interrupt settings
class opt4048_int_cfg_t:
    INT_SMBUS_ALERT = 0x00
    INT_DR_NEXT_CHANNEL = 0x01
    INT_DR_ALL_CHANNELS = 0x03

# Register for Exponent and Result (MSB) for Channel 0
SFE_OPT4048_REGISTER_EXP_RES_CH0 = 0x00

# Register for Result (LSB), Counter, and CRC for Channel 0
SFE_OPT4048_REGISTER_RES_CNT_CRC_CH0 = 0x01

# Register for Exponent and Result (MSB) for Channel 1
SFE_OPT4048_REGISTER_EXP_RES_CH1 = 0x02

# Register for Result (LSB), Counter, and CRC for Channel 1
SFE_OPT4048_REGISTER_RES_CNT_CRC_CH1 = 0x03

# Register for Exponent and Result (MSB) for Channel 2
SFE_OPT4048_REGISTER_EXP_RES_CH2 = 0x04

# Register for Result (LSB), Counter, and CRC for Channel 2
SFE_OPT4048_REGISTER_RES_CNT_CRC_CH2 = 0x05

# Register for Exponent and Result (MSB) for Channel 3
SFE_OPT4048_REGISTER_EXP_RES_CH3 = 0x06

# Register for Result (LSB), Counter, and CRC for Channel 3
SFE_OPT4048_REGISTER_RES_CNT_CRC_CH3 = 0x07

# Register for Threshold  Exponent and Result - Low
SFE_OPT4048_REGISTER_THRESH_L_EXP_RES = 0x08

# Register for Threshold Exponent and Threshold Result - High
SFE_OPT4048_REGISTER_THRESH_H_EXP_RES = 0x09

# Register that controls the main functions of the device.
SFE_OPT4048_REGISTER_CONTROL = 0x0A

# Register with settings for the interrupt pin.
SFE_OPT4048_REGISTER_INT_CONTROL = 0x0B

# Register containing various status flags.
SFE_OPT4048_REGISTER_FLAGS = 0x0C

# Register containing the device ID.
SFE_OPT4048_REGISTER_DEVICE_ID = 0x11
