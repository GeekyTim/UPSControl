from os import path
from gpiozero import InputDevice



class UPS:
    """
    UPS Driver for the SBComponents UPS
    """
    __batterydetectionpin = 26
    __batterylowerlimit = 15.0  # Percent

    __verbose = False


    def __init__(self):
        batterystatus = InputDevice(self.__batterydetectionpin)

    """
    The following properties should exist in all UPS code - returning 'None' if the value cannot be extracted
    """

    @property
    def ispowered(self):
        return None

    @property
    def isonbattery(self):
        return None

    @property
    def getbatteryvoltage(self):
        return None

    @property
    def getpivoltage(self):
        return None

    @property
    def getsupplyvoltage(self):
        return None

    @property
    def isbatteryok(self):
        return

    @property
    def ischarging(self):
        return None

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
