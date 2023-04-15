from time import sleep

from gpiozero import InputDevice

from .upscode import UPSCode


class UPS(UPSCode):
    """
    UPS Driver for the SBComponents UPS
    """
    __batterydetectionpin = 26

    def __init__(self, log):
        super().__init__(log)

        self.__batterystatus = InputDevice(self.__batterydetectionpin)

        # If the battery is not okay when this code starts, then assume that the UPS is either not connected,
        # or there is a fault.
        # We don't want to shut the system down immediately, otherwise we may not be able to
        # access the device without it shutting itself down.
        if not self.is_battery_ok:
            sleep(2)
            if not self.is_battery_ok:
                self.__log.info("The battery status is 'not OK' at the start - exiting UPS code.")
                exit(1)

    """
    The following properties should exist in all UPS code - returning 'None' if the value cannot be
    extracted
    """

    @property
    def is_battery_ok(self):
        return self.__batterystatus.is_active
