import logging
from datetime import datetime
from os import system
from sys import exit
from time import sleep

from systemd.journal import JournalHandler

import upscode.undervoltage as undervoltage
import upsconfig

log = logging.getLogger("UPS")
log.addHandler(JournalHandler())

if upsconfig.upstype == "UPiS":
    import upscode.upis as ups

    log.setLevel(logging.INFO)
    log.info("UPiS Advanced UPS")
elif upsconfig.upstype == "SBComponents":
    import upscode.sbcomponents as ups

    log.setLevel(logging.INFO)
    log.info("SB Components")
elif upsconfig.upstype == "PiUpTime":
    import upscode.piuptime as ups

    log.setLevel(logging.INFO)
    log.info("PiUpTime UPS")
else:
    log.setLevel(logging.ERROR)
    log.info("Define the UPS Type in upsconfig.py")
    exit(0)

attachedups = ups.UPS(log)
vgcmd = undervoltage.Undervoltage(log)


def logBatteryPower():
    batterypercent = attachedups.batteryPercent
    if batterypercent is not None:
        log.setLevel(logging.INFO)
        log.info(f"Battery Remaining: {batterypercent:.1%}")


def upsCheckStatus():
    onbattery = False
    vgcmd.undervoltage()
    attachedups.updateDisplay()

    while True:
        if attachedups.isPowered is not None:
            if attachedups.isPowered:
                if onbattery:
                    onbattery = False
                    log.setLevel(logging.INFO)
                    log.info(f"Power returned at {datetime.today()}.")
                    logBatteryPower()
            else:
                if not onbattery:
                    log.setLevel(logging.INFO)
                    log.info(f"UPS Battery is being used at {datetime.today()}.")
                onbattery = True
                logBatteryPower()

        if not attachedups.isBatteryOk:
            log.setLevel(logging.INFO)
            log.info(f"UPS Battery is running out. Shutting down the Pi at {datetime.today()}.")
            logBatteryPower()
            system("sudo shutdown -h now")  # Shutdown the Pi

        attachedups.updateDisplay()
        vgcmd.undervoltage()
        sleep(upsconfig.refreshtime)


if __name__ == "__main__":
    upsCheckStatus()
