from pijuice import PiJuice

from .upscode import UPSCode


class UPS(UPSCode):
    __minBattery = 0.15  # 15 Percentage, at which battery charge can reduce to
    __connectiontries = 5

    def __init__(self, log):
        super().__init__(log)

        connectiontries = self.__connectiontries

        while connectiontries > 0:
            try:
                self.log_to_journal("Connecting to PiJuice")
                self.__pijuice = PiJuice(1, 0x14)
                self.log_to_journal("Connected to PiJuice")
                break
            except Exception as err:
                self.log_to_journal(f"ERROR: Is the PiJuice HAT attached? {err}")

            if self.__pijuice.status.GetStatus()['error'] == 'COMMUNICATION_ERROR':
                self.log_to_journal("ERROR: Unable to communicate with the PiJuice UPS.")

            connectiontries -= 1

        if self.__connectiontries == 0:
            self.log_to_journal("ERROR: Unable to connect with the PiJuice UPS. Exiting UPS Control.")
            exit(0)

    @property
    def is_powered(self):
        status = self.__pijuice.status.GetStatus()['data']
        response = False

        if status['powerInput'] == 'PRESENT' or status['powerInput5vIo'] == 'PRESENT':
            response = True

        return response

    @property
    def is_on_battery(self):
        return self.__pijuice.status.GetStatus()['data']['battery'] == 'NORMAL'

    @property
    def battery_voltage(self):
        return self.__pijuice.status.GetBatteryVoltage()['data'] / 1000.0

    @property
    def pi_voltage(self):
        voltage = None
        if self.__pijuice.status.GetStatus()['data']['powerInput5vIo'] == 'PRESENT':
            voltage = self.__pijuice.status.GetIoVoltage()['data'] / 1000.0
        return voltage

    @property
    def supply_voltage(self):
        return self.__pijuice.status.GetIoVoltage()['data'] / 1000.0

    @property
    def is_battery_ok(self):
        isbatteryok = True

        if self.is_on_battery and self.battery_percent < self.__minBattery:
            isbatteryok = False

        return isbatteryok

    @property
    def is_charging(self):
        status = self.__pijuice.status.GetStatus()['data']['battery']
        return status == 'CHARGING_FROM_IN' or status == 'CHARGING_FROM_5V_IO'

    @property
    def battery_current(self):
        return self.__pijuice.status.GetBatteryCurrent()['data'] / 1000.0

    @property
    def battery_percent(self):
        return self.__pijuice.status.GetChargeLevel()['data'] / 100.0

    @property
    def power_source(self):
        status = self.__pijuice.status.GetStatus()['data']
        response = 'Unknown'

        if status['powerInput'] == 'PRESENT':
            response = 'HAT'
        elif status['powerInput5vIo'] == 'PRESENT':
            response = 'Pi'
        elif status['battery'] == 'NORMAL':
            response = 'Battery'

        return response

    def update_display(self):
        """
        If the UPS is able to display its condition, do so
        """
        pass
