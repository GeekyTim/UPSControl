from os import path
import serial

from .upscode import UPSCode


class UPS(UPSCode):
    """
    UPS Driver for the UPiS Advanced
    """
    __baudrate = 38400
    __timeout = 1
    __rtscts = 0
    __xonxoff = 0

    __port = "/dev/ttyAMA0"
    __batterylowerlimit = 3.4

    def __init__(self, log):
        super().__init__(log)

        self.__serial = serial

        # Check if a serial port device exists
        if not path.exists(self.__port):
            self.__log.info(f"ERROR: Serial port '{str(self.__port)}' cannot be found!")
            exit(1)

        self.__powersource()

    def __queryups(self, query, resultstring):
        # Set up the connection to the UPS
        upis = self.__serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout,
                                    rtscts=self.__rtscts, xonxoff=self.__xonxoff)

        upis.write(f"@{query}\r".encode())
        upis.flush()
        results = upis.readlines()

        upis.close()

        response = None
        for line in results:
            # get rid of the newline characters
            line = line.decode().strip()

            # is it the answer we are looking for? (yep, should be regexp...)
            if resultstring in line:
                response = line.split(":", 1)[1].split(" ")[0]

        return response

    def __powersource(self):
        powersource = self.__queryups("PM", "Powering Source")

        if powersource is not None:
            self.__pipower = False
            self.__upsusbpower = False
            self.__upsexternalpower = False
            self.__batterypower = False

            if powersource == 'RPI':
                self.__pipower = True
            elif powersource == 'EPR':
                self.__upsexternalpower = True
            elif powersource == 'BAT':
                self.__batterypower = True
            elif powersource == 'USB':
                self.__upsusbpower = True

    def __voltage(self, source):
        return float(self.__queryups(source, "Voltage"))

    def __current(self):
        return float(self.__queryups("CUR", "UPiS Current"))

    @property
    def is_powered(self):
        self.__powersource()
        return self.__pipower or self.__upsexternalpower or self.__upsusbpower

    @property
    def is_on_battery(self):
        self.__powersource()
        return self.__batterypower

    @property
    def battery_voltage(self):
        return self.__voltage("BAT")

    @property
    def pi_voltage(self):
        return self.__voltage("RPI")

    @property
    def supply_voltage(self):
        epr = self.__voltage("EPR")
        usb = self.__voltage("USB")
        return max(epr, usb)

    @property
    def is_battery_ok(self):
        response = True

        if self.is_on_battery and self.__voltage("BAT") < self.__batterylowerlimit:
            response = False

        return response

    @property
    def is_charging(self):
        self.__powersource()
        return self.__pipower or self.__upsexternalpower or self.__upsusbpower

    @property
    def battery_current(self):
        return self.__current()

    @property
    def power_source(self):
        self.__powersource()

        powersource = "Unknown"

        if self.__pipower:
            powersource = "Pi"
        elif self.__upsexternalpower:
            powersource = "External"
        elif self.__batterypower:
            powersource = "Battery"
        elif self.__upsusbpower:
            powersource = "HAT"

        return powersource
