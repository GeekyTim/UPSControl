from datetime import datetime
from os import system
from sys import exit
from time import sleep

import upsconfig

if upsconfig.upstype == "UPiS":
    import upscode.upis as ups
elif upsconfig.upstype == "SBComponents":
    import upscode.sbcomponents as ups
elif upsconfig.upstype == "PiUpTime":
    import upscode.piuptime as ups
else:
    print("Define the UPS Type in upsconfig.py.")
    exit(0)

attachedups = ups.UPS()

sleep(5)


def upsCheckStatus():
    onbattery = False
    attachedups.updatedisplay()

    while True:
        if attachedups.isonbattery:
            if not onbattery:
                print("UPS Battery is being used at {0}.".format(datetime.now()))
            onbattery = True
        else:
            if onbattery:
                onbattery = False
                print("Power returned at {0}.".format(datetime.now()))

        if not attachedups.isbatteryok:
            print("UPS Battery is running out. Shutting down the Pi at {0}.".format(datetime.now()))
            system("sudo shutdown -h now")  # Shutdown the Pi

        attachedups.updatedisplay()
        sleep(upsconfig.refreshtime)


if __name__ == "__main__":
    upsCheckStatus()
