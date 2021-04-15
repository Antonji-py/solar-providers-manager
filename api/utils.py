import json
from datetime import date, timedelta


def get_credentials():
    with open("credentials.json") as credentials_file:
        credentials = json.load(credentials_file)

    return credentials


def update_plants_json(provider, plants):
    with open("plants.json", "r") as plants_read_file:
        plants_json = json.load(plants_read_file)
        plants_json[provider] = plants

    with open("plants.json", "w") as plants_write_file:
        json.dump(plants_json, plants_write_file)


def update_devices_json(provider, devices):
    with open("devices.json", "r") as devices_read_file:
        devices_json = json.load(devices_read_file)
        devices_json[provider] = devices

    with open("devices.json", "w") as devices_write_file:
        json.dump(devices_json, devices_write_file)


def get_dates_between(start_date, end_date):
    days_between = []

    start_date_list = start_date.split("-")
    end_date_list = end_date.split("-")

    start_date = date(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2]))
    end_date = date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))

    delta = end_date - start_date

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        days_between.append(str(day))

    return days_between


def get_plant_by_id(plant_id):
    plant_data = {}
    
    with open("plants.json") as plants_file:
        plants_json = json.load(plants_file)

        for provider in plants_json:
            for plant in plants_json[provider]:
                if plant["id"] == plant_id:
                    plant_data = plant
                    plant_data.update({"provider": provider})

        return plant_data
