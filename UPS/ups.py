#!/usr/bin/python3

import logging
from datetime import datetime
from os import system
from sys import exit
from time import sleep

from systemd.journal import JournalHandler

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
elif upsconfig.upstype == "PiJuice":
    import upscode.pspijuice as ups

    log.setLevel(logging.INFO)
    log.info("PiJuice UPS")
else:
    log.setLevel(logging.ERROR)
    log.info("Define the UPS Type in upsconfig.py")
    exit(0)

attachedups = ups.UPS(log)


def logbatterypower():
    batterypercent = attachedups.battery_percent
    if batterypercent is not None:
        logmessage(f"Battery Remaining: {batterypercent:.1%}")


def logmessage(message):
    log.setLevel(logging.INFO)
    log.info(message)
    print(message)


def startup_status():
    if attachedups.is_powered is not None:
        logmessage(f'Is Powered: {attachedups.is_powered}')
    if attachedups.is_on_battery is not None:
        logmessage(f'Is on battery: {attachedups.is_on_battery}')
    if attachedups.battery_voltage is not None:
        logmessage(f'Battery Voltage: {attachedups.battery_voltage} v')
    if attachedups.pi_voltage is not None:
        logmessage(f'Pi Voltage: {attachedups.pi_voltage} v')
    if attachedups.supply_voltage is not None:
        logmessage(f'Supply Voltage: {attachedups.supply_voltage} v')
    if attachedups.is_battery_ok is not None:
        logmessage(f'Is Battery OK: {attachedups.is_battery_ok}')
    if attachedups.is_charging is not None:
        logmessage(f'Is Charging: {attachedups.is_charging}')
    if attachedups.battery_current is not None:
        logmessage(f'Current: {attachedups.battery_current} A')
    if attachedups.battery_percent is not None:
        logmessage(f'Battery %: {attachedups.battery_percent:.1%}')
    if attachedups.power_source is not None:
        logmessage(f'Power Source: {attachedups.power_source}')


def ups_check_status():
    onbattery = False
    attachedups.update_display()
    startup_status()

    while True:
        ispowered = attachedups.is_powered
        isonbattery = attachedups.is_on_battery
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        if ispowered is not None and isonbattery is not None:
            if ispowered:
                if onbattery:
                    onbattery = False
                    logmessage(f"Power returned at {now}.")
            elif not onbattery:
                onbattery = True
                logmessage(f"UPS Battery is being used at {now}.")
                logbatterypower()
            else:
                logbatterypower()

        if not attachedups.is_battery_ok:
            logmessage(f"UPS Battery is running out. Shutting down the Pi at {now}.")
            logbatterypower()
            system("sudo shutdown -h now")  # Shutdown the Pi

        # TODO: Add hourly log of battery status

        attachedups.update_display()
        sleep(upsconfig.refreshtime)


if __name__ == "__main__":
    ups_check_status()
