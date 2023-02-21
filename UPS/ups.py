from datetime import datetime
from os import system
from sys import exit
from time import sleep

import upsconfig

if upsconfig.upstype == "UPiS":
    import upscode.upis as ups
elif upsconfig.upstype == "SBComponents":
    import upscode.sbcomponents as ups
else:
    print("Define the UPS Type in upsconfig.py.")
    exit(0)

attachedups = ups.UPS()

sleep(5)


def upsCheckStatus():
    onbattery = False
    while True:
        if attachedups.isonbattery:
            if not onbattery:
                print("UPS Battery is being used at {0}.".format(datetime.now()))
            onbattery = True

            if not attachedups.isbatteryok:
                print("UPS Battery is running out at {0}. Shutting down the Pi.".format(datetime.now()))
                system("sudo shutdown -h now")  # Shutdown the Pi
        else:
            if onbattery:
                onbattery = False
                print("Power returned at {0}.".format(datetime.now()))

        attachedups.updatedisplay()
        sleep(upsconfig.refreshtime)


if __name__ == "__main__":
    upsCheckStatus()
