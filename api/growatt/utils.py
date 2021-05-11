import json


def check_device_type(device_id):
    with open("devices.json") as devices_file:
        devices = json.load(devices_file)

        for devices in devices["growatt"]:
            for device in devices:
                if device["serial_number"] == device_id:
                    device_type = device["device_type"]

    return device_type
