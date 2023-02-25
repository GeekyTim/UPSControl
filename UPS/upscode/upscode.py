class UPSCode:
    """
    UPS Driver for the SBComponents UPS
    """
    __batterydetectionpin = 26

    def __init__(self):
        pass

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
        return None

    @property
    def ischarging(self):
        return None

    @property
    def getcurrent(self):
        return None

    @property
    def batterypercentage(self):
        return None

    @property
    def getpowersource(self):
        return None

    def updatedisplay(self):
        """
        If the UPS is able to display its condition, do so
        """
        pass
