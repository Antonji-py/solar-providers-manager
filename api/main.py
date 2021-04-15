from flask import Flask, request
from flask_cors import CORS
import json

from utils import get_credentials, update_plants_json, update_devices_json, get_dates_between, get_plant_by_id
from files_maker import GrowattFileMaker, SolarEdgeFileMaker
from growatt.api import GrowattApi
from solaredge.api import SolarEdgeApi

app = Flask(__name__)
CORS(app)

credentials = get_credentials()
growatt = GrowattApi(credentials["growatt"]["username"], credentials["growatt"]["password"])
solaredge = SolarEdgeApi(credentials["solaredge"]["api_token"],
                         credentials["solaredge"]["username"],
                         credentials["solaredge"]["password"])

g_maker = GrowattFileMaker()
se_maker = SolarEdgeFileMaker()


@app.route("/refresh-plants")
def refresh_plants():
    growatt_plants = growatt.get_plants()
    update_plants_json("growatt", growatt_plants)
    solaredge_plants = solaredge.get_plants()
    update_plants_json("solaredge", solaredge_plants)

    growatt_devices = growatt.get_all_devices()
    update_devices_json("growatt", growatt_devices)
    solaredge_devices = solaredge.get_all_devices()
    update_devices_json("solaredge", solaredge_devices)

    return {"result": "File updated successfully"}


@app.route("/get-plants")
def get_plants():
    with open("plants.json") as plants_file:
        plants = json.load(plants_file)

    return {"plants": plants}


@app.route("/get-devices")
def get_devices():
    with open("devices.json") as devices_file:
        devices = json.load(devices_file)

    return {"devices": devices}


@app.route("/get-devices-by-ids", methods=["POST"])
def get_devices_by_ids():
    filtered_devices = []

    if request.json["plants"] is not []:
        plants = request.json["plants"]
        plants_ids = [plant["id"] for plant in plants]

        with open("devices.json") as devices_file:
            devices = json.load(devices_file)

            for provider in devices:
                for plant in devices[provider]:
                    for device in plant:
                        if device["plant_id"] in plants_ids:
                            filtered_devices.append(device)

    return {"devices": filtered_devices}


@app.route("/get-logs-file", methods=["POST"])
def get_logs_file():
    devices = request.json["devices"]
    start_date = request.json["startDate"]
    end_date = request.json["endDate"]

    for device in devices:
        dates_between = get_dates_between(start_date, end_date)
        device_plant = get_plant_by_id(device["plant_id"])
        logs = []

        for date in dates_between:
            if device_plant["provider"] == "growatt":
                daily_logs = growatt.get_daily_logs(device["serial_number"], date)
            else:
                daily_logs = solaredge.get_daily_logs(device_plant["id"], device["serial_number"], date)["data"]["telemetries"]
            logs += daily_logs

        plant_name = device_plant["plant_name"]
        if device_plant["provider"] == "growatt":
            g_maker.write_logs_file(logs, plant_name, [start_date, end_date])
        else:
            se_maker.write_logs_file(logs, plant_name, [start_date, end_date])

    return {"result": "File created successfully"}


@app.route("/get-fault-logs-file", methods=["POST"])
def get_fault_logs_file():
    plants = request.json["plants"]
    date = request.json["date"]

    for plant in plants:
        plant_id = plant["id"]
        provider = get_plant_by_id(plant_id)["provider"]
        plant_name = get_plant_by_id(plant_id)["plant_name"]

        if provider == "growatt":
            fault_logs = growatt.get_fault_logs(plant_id, date)
            g_maker.write_fault_logs_file(fault_logs, plant_name, date)
        else:
            pass

    return {"result": "File created successfully"}


@app.route("/get-monthly-report-file", methods=["POST"])
def get_monthly_report_file():
    plants = request.json["plants"]
    date = request.json["date"]

    for plant in plants:
        plant_id = plant["id"]
        provider = get_plant_by_id(plant_id)["provider"]
        plant_name = get_plant_by_id(plant_id)["plant_name"]

        if provider == "growatt":
            monthly_energy = growatt.get_monthly_energy_data(plant_id, date)
            g_maker.write_monthly_report_file(monthly_energy, plant_name, date)
        else:
            monthly_energy = solaredge.get_monthly_energy_data(plant_id, date)
            se_maker.write_monthly_report_file(monthly_energy, plant_name, date)

    return {"result": "File created successfully"}


app.run(debug=True)
