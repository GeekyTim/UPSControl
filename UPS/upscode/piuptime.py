from gpiozero import InputDevice

from .upscode import UPSCode


class UPS(UPSCode):
    """
    UPS Driver for the SBComponents UPS
    """
    __batterydetectionpin = 26

    def __init__(self, log):
        super().__init__()

        self.__log = log
        self.__batterystatus = InputDevice(self.__batterydetectionpin)

    """
    The following properties should exist in all UPS code - returning 'None' if the value cannot be
    extracted
    """

    @property
    def isBatteryOk(self):
        return self.__batterystatus.is_active
