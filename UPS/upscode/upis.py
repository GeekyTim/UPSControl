from sys import exit
from os import path
import serial


class UPS(object):
    """
    UPS Driver for the UPiS Advanced
    """
    __baudrate = 38400
    __timeout = 1
    __rtscts = 0
    __xonxoff = 0

    __port = "/dev/ttyAMA0"
    __batterylowerlimit = 3.4

    __verbose = False

    def __init__(self):
        self.__serial = serial

        # Check if serial port device exists
        if not path.exists(self.__port):
            print("ERROR: Serial port '{0}' cannot be found!".format(str(self.__port)))
            exit(1)

        self.__pipower = False
        self.__upsusbpower = False
        self.__upsexternalpower = False
        self.__batterypower = False

        self.__get_powersource()

    def __queryUPIS(self, query, resultstring):
        # Set up the connection to the UPS
        upis = self.__serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout,
                                    rtscts=self.__rtscts, xonxoff=self.__xonxoff)

        upis.write("@{0}\r".format(query).encode())
        upis.flush()
        results = upis.readlines()

        upis.close()

        response = None
        for line in results:
            # get rid of the newline characters
            line = line.decode().strip()

            print("INFO: Reading line {0}".format(line))
            # is it the answer we are looking for? (yep, should be regexp...)
            if resultstring in line:
                response = line.split(":", 1)[1].split(" ")[0]

                if self.__verbose:
                    print("INFO: Query '{0}' returned {1}".format(query, response))

        return response

    def __get_powersource(self):
        if self.__verbose:
            print('INFO: Detecting power setup')

        powersource = self.__queryUPIS("PM", "Powering Source")

        # is it the answer we are looking for? (yep, should be regexp...)
        if powersource is not None:
            self.__pipower = False
            self.__upsusbpower = False
            self.__upsexternalpower = False
            self.__batterypower = False

            if self.__verbose:
                print("INFO: System is powered via {0}".format(powersource))

            if powersource == 'RPI':
                self.__pipower = True
            elif powersource == 'EPR':
                self.__upsexternalpower = True
            elif powersource == 'BAT':
                self.__batterypower = True
            elif powersource == 'USB':
                self.__upsusbpower = True

    def __get_voltage(self, source):
        voltage = self.__queryUPIS(source, "Voltage")

        if self.__verbose:
            print("INFO: Battery voltage {0}".format(voltage))

        return float(voltage)

    def __get_current(self):
        current = self.__queryUPIS("CUR", "UPS Current")

        if self.__verbose:
            print("INFO: Battery voltage {0}".format(current))

        return float(current)

    @property
    def ispowered(self):
        self.__get_powersource()
        return self.__pipower or self.__upsexternalpower or self.__upsusbpower

    @property
    def isonbattery(self):
        self.__get_powersource()
        return self.__batterypower

    @property
    def getbatteryvoltage(self):
        return self.__get_voltage("BAT")

    @property
    def getpivoltage(self):
        return self.__get_voltage("RPI")

    @property
    def getsupplyvoltage(self):
        epr = self.__get_voltage("EPR")
        usb = self.__get_voltage("USB")
        return max(epr, usb)

    @property
    def isbatteryok(self):
        return self.__get_voltage("BAT") >= self.__batterylowerlimit

    @property
    def ischarging(self):
        self.__get_powersource()
        return self.__pipower or self.__upsexternalpower or self.__upsusbpower

    @property
    def getcurrent(self):
        return self.__get_current()

    @property
    def getpowersource(self):
        self.__get_powersource()

        powersource = "Unknown"

        if self.__pipower:
            powersource = "Pi"
        elif self.__upsexternalpower:
            powersource = "External"
        elif self.__batterypower:
            powersource = "Battery"
        elif powersource == "USB":
            powersource = "UPS USB"

        return powersource

    def updatedisplay(self):
        """
        If the UPS is able to display its condition, do so
        """
        pass
