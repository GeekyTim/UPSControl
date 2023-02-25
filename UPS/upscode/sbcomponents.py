from os import path

import smbus

from .oled_091 import SSD1306
from .upscode import UPSCode


class Bus_Voltage_Range:
    """Constants for ``__bus_voltage_range``"""
    RANGE_16V = 0x00  # set __bus voltage range to 16V
    RANGE_32V = 0x01  # set __bus voltage range to 32V (default)


class Gain:
    """Constants for ``__gain``"""
    DIV_1_40MV = 0x00  # shunt prog. __gain set to  1, 40 mV range
    DIV_2_80MV = 0x01  # shunt prog. __gain set to /2, 80 mV range
    DIV_4_160MV = 0x02  # shunt prog. __gain set to /4, 160 mV range
    DIV_8_320MV = 0x03  # shunt prog. __gain set to /8, 320 mV range


class ADC_Resolution:
    """Constants for ``__bus_adc_resolution`` or ``__shunt_adc_resolution``"""
    ADCRES_9BIT_1S = 0x00  # 9bit,   1 sample,     84us
    ADCRES_10BIT_1S = 0x01  # 10bit,   1 sample,    148us
    ADCRES_11BIT_1S = 0x02  # 11 bit,  1 sample,    276us
    ADCRES_12BIT_1S = 0x03  # 12 bit,  1 sample,    532us
    ADCRES_12BIT_2S = 0x09  # 12 bit,  2 samples,  1.06ms
    ADCRES_12BIT_4S = 0x0A  # 12 bit,  4 samples,  2.13ms
    ADCRES_12BIT_8S = 0x0B  # 12bit,   8 samples,  4.26ms
    ADCRES_12BIT_16S = 0x0C  # 12bit,  16 samples,  8.51ms
    ADCRES_12BIT_32S = 0x0D  # 12bit,  32 samples, 17.02ms
    ADCRES_12BIT_64S = 0x0E  # 12bit,  64 samples, 34.05ms
    ADCRES_12BIT_128S = 0x0F  # 12bit, 128 samples, 68.10ms


class Mode:
    """Constants for ``mode``"""
    POWERDOWN = 0x00  # power down
    SVOLT_TRIGGERED = 0x01  # shunt voltage triggered
    BVOLT_TRIGGERED = 0x02  # __bus voltage triggered
    SANDBVOLT_TRIGGERED = 0x03  # shunt and __bus voltage triggered
    ADCOFF = 0x04  # ADC off
    SVOLT_CONTINUOUS = 0x05  # shunt voltage continuous
    BVOLT_CONTINUOUS = 0x06  # __bus voltage continuous
    SANDBVOLT_CONTINUOUS = 0x07  # shunt and __bus voltage continuous


class UPS(UPSCode):
    """
    UPS Driver for the SBComponents UPS
    """
    __ups_i2c_bus = 1
    __ups_addr = 0x42
    __batterylowerlimit = 15.0  # Percent

    __verbose = False

    _REG_CONFIG = 0x00  # Config Register (R/W)
    _REG_SHUNTVOLTAGE = 0x01  # SHUNT VOLTAGE REGISTER (R)
    _REG_BUSVOLTAGE = 0x02  # BUS VOLTAGE REGISTER (R)
    _REG_POWER = 0x03  # POWER REGISTER (R)
    _REG_CURRENT = 0x04  # CURRENT REGISTER (R)
    _REG_CALIBRATION = 0x05  # CALIBRATION REGISTER (R/W)

    __DIR_PATH = path.abspath(path.dirname(__file__))
    __DefaultFont = path.join(__DIR_PATH, "../resources/GothamLight.ttf")

    def __init__(self):
        super().__init__()

        # The OLED Display - over I2C
        self.__oled_display = SSD1306()

        # The UPS status over I2C
        self.__bus = smbus.SMBus(self.__ups_i2c_bus)
        self.__addr = self.__ups_addr

        # Set chip to known config values to start
        self.__cal_value = 4096
        self.__current_lsb = 0.1  # __getcurrent LSB = 100uA per bit
        self.__power_lsb = 0.002  # __power LSB = 2mW per bit
        self.__calibrate()

        self.__pipower = False
        self.__upsusbpower = False
        self.__upsexternalpower = False
        self.__batterypower = False

    def __read(self, address):
        data = self.__bus.read_i2c_block_data(self.__addr, address, 2)
        return (data[0] * 256) + data[1]

    def __write(self, address, data):
        temp = [0, 0]
        temp[1] = data & 0xFF
        temp[0] = (data & 0xFF00) >> 8
        self.__bus.write_i2c_block_data(self.__addr, address, temp)

    def __calibrate(self):  # set __calibrate 32V ,2A
        """Configures to INA219 to be able to measure up to 32V and 2A of current. Counter
           overflow occurs at 3.2A.
           ..note :: These calculations assume a 0.1 shunt ohm resistor is present
        """

        # Set Calibration register to 'Cal' calculated above
        self.__write(self._REG_CALIBRATION, self.__cal_value)

        # Set Config register to take into account the settings
        config = Bus_Voltage_Range.RANGE_32V << 13 | \
                 Gain.DIV_8_320MV << 11 | \
                 ADC_Resolution.ADCRES_12BIT_32S << 7 | \
                 ADC_Resolution.ADCRES_12BIT_32S << 3 | \
                 Mode.SANDBVOLT_CONTINUOUS

        self.__write(self._REG_CONFIG, config)

    def __shuntvoltage(self):  # shunt voltage in milli volts
        # self.__write(self._REG_CALIBRATION, self.__cal_value)
        value = self.__read(self._REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01

    def __getcurrent(self):  # current in milli amp
        value = self.__read(self._REG_CURRENT)
        if value > 32767:
            value -= 65535
        return (value * self.__current_lsb) / 1000.0

    def __power(self):
        # self.__write(self._REG_CALIBRATION, self.__cal_value)
        value = self.__read(self._REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self.__power_lsb

    def __busvoltage(self):
        # self.__write(self._REG_CALIBRATION, self.__cal_value)
        value = self.__read(self._REG_BUSVOLTAGE)
        return (value >> 3) * 0.004

    def __get_batterypercentage(self):
        batterypercentage = ((self.__busvoltage() - 6.0) / 2.4) * 100.0
        if batterypercentage > 100.0:
            batterypercentage = 100.0
        if batterypercentage < 0.0:
            batterypercentage = 0.0
        return batterypercentage

    """
    The following properties should exist in all UPS code - returning 'None' if the value cannot be extracted
    """

    @property
    def ispowered(self):
        return self.__power() <= 1.0

    @property
    def isonbattery(self):
        return self.__power() > 1.0

    @property
    def getsupplyvoltage(self):
        return self.__busvoltage()

    @property
    def isbatteryok(self):
        return self.__get_batterypercentage() >= self.__batterylowerlimit

    @property
    def getcurrent(self):
        return self.__getcurrent()

    @property
    def batterypercentage(self):
        return self.__get_batterypercentage()

    @property
    def getpowersource(self):
        powersource = "Unknown"

        if self.ispowered:
            powersource = "External"
        elif self.isonbattery:
            powersource = "Battery"

        return powersource

    def updatedisplay(self):
        """
        If the UPS is able to display its condition, do so
        """
        if self.ispowered:
            self.__oled_display.PrintText("Powered", cords=(1, 4), FontSize=28)
        else:
            self.__oled_display.PrintText("Battery: {:3.1f}%".format(self.batterypercentage), cords=(3, 10),
                                          FontSize=16)

        self.__oled_display.ShowImage()
