"""NI System Configuration - Get Installed Devices.

This examples demonstrates how to get the devices installed in a chassis.
"""
import nisyscfg


def get_chassis(session):
    "Filter and find chassis in the system."
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_chassis = True
    for chassis in session.find_hardware(filter):
        print("Chassis: ", chassis.name)
    get_modules(session)


def get_modules(session):
    "Filter and find modules installed in the system."
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_device = True
    filter.number_of_slots = 9
    for slot in range(filter.number_of_slots + 1):
        filter.slot_number = slot
        for module in session.find_hardware(filter):
            print("Slot " + str(slot) + ": ", module.name)


def get_installed_devices():
    "Open NI System Configuration session."
    with nisyscfg.Session() as session:
        get_chassis(session)


if __name__ == "__main__":
    get_installed_devices()
