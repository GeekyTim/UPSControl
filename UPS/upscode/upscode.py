class UPSCode:
    def __init__(self, log):
        # Initialise the UPS
        self.__log = log

        self.log_to_journal("Initialising UPS")

    """
    The following properties may exist in the UPS code - returning 'None' if the value cannot be extracted
    """

    @property
    def is_powered(self):
        return None

    @property
    def is_on_battery(self):
        return None

    @property
    def battery_voltage(self):
        return None

    @property
    def pi_voltage(self):
        return None

    @property
    def supply_voltage(self):
        return None

    @property
    def is_battery_ok(self):
        return None

    @property
    def is_charging(self):
        return None

    @property
    def battery_current(self):
        return None

    @property
    def battery_percent(self):
        return None

    @property
    def power_source(self):
        return None

    def log_to_journal(self, text):
        self.__log.info(text)
        print(text)

    def update_display(self):
        """
        If the UPS is able to display its condition, do so
        """
        pass
