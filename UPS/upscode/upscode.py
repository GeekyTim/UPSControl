class UPSCode:
    def __init__(self):
        pass

    """
    The following properties should exist in all UPS code - returning 'None' if the value cannot be extracted
    """

    @property
    def isPowered(self):
        return None

    @property
    def isOnBattery(self):
        return None

    @property
    def batteryVoltage(self):
        return None

    @property
    def piVoltage(self):
        return None

    @property
    def supplyVoltage(self):
        return None

    @property
    def isBatteryOk(self):
        return None

    @property
    def isCharging(self):
        return None

    @property
    def current(self):
        return None

    @property
    def batteryPercent(self):
        return None

    @property
    def powerSource(self):
        return None

    def updateDisplay(self):
        """
        If the UPS is able to display its condition, do so
        """
        pass
