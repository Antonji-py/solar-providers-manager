import requests

from growatt.utils import check_device_type


class GrowattApi:
    def __init__(self, username, password):
        session = requests.Session()
        session.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.login(session, username, password)

        self.session = session

    def login(self, session, username, password):
        url = "http://server.growatt.com/login"
        data = {
            "account": username,
            "password": password,
            "validateCode": ""
        }

        response = session.post(url, data=data)
        if response.json()["result"] != 1:
            print("[Growatt]  Error while logging in")

    def get_plants(self):
        url = "http://server.growatt.com/selectPlant/getPlantList"
        current_page = 0
        pages = -1

        plants_list = []

        while current_page != pages:
            current_page += 1
            data = {
                "currPage": current_page,
                "plantType": "-1",
                "orderType": 0,
                "plantName": ""
            }

            response = self.session.post(url, data=data)
            response_json = response.json()

            pages = response_json["pages"]

            for plant in response_json["datas"]:
                plant_data = {}
                plant_data.update({"id": plant["id"]})
                plant_data.update({"plant_name": plant["plantName"]})
                plant_data.update({"plant_img": plant["plantImg"]})

                plants_list.append(plant_data)

        return plants_list

    def get_plant_devices(self, plant_id):
        url = "http://server.growatt.com/panel/getDevicesByPlantList"
        current_page = 0
        pages = -1

        devices = []

        while current_page != pages:
            current_page += 1
            data = {
                "currPage": current_page,
                "plantId": plant_id
            }

            response = self.session.post(url, data=data)
            response_json = response.json()

            if response_json["result"] != 1:
                return response_json

            pages = response_json["obj"]["pages"]

            for device in response_json["obj"]["datas"]:
                devices.append(device)

        return devices

    def get_all_devices(self):
        plants = self.get_plants()
        plants_ids = [plant["id"] for plant in plants]

        all_devices = []

        for plant_id in plants_ids:
            devices = self.get_plant_devices(plant_id)
            plant_devices = []

            for device in devices:
                device_data = {}
                try:
                    device_data.update({"plant_id": device["plantId"]})
                    device_data.update({"serial_number": device["sn"]})
                    device_data.update({"device_model": device["deviceModel"]})
                    device_data.update({"device_type": device["deviceTypeName"]})
                except TypeError:
                    device_data.update({"plant_id": plant_id})
                    device_data.update({"serial_number": "null"})
                    device_data.update({"device_model": "null"})
                    device_data.update({"device_type": "null"})

                plant_devices.append(device_data)

            all_devices.append(plant_devices)

        return all_devices

    def get_daily_logs(self, device_id, date):
        device_type = check_device_type(device_id)
        if device_type == "inv":
            device_key = "invSn"
            url = "http://server.growatt.com/device/getInverterHistory"
        elif device_type == "tlx":
            device_key = "tlxSn"
            url = "http://server.growatt.com/device/getTLXHistory"

        start_index = 0
        have_next = True

        logs = []

        while have_next is True:
            data = {
                device_key: device_id,
                "startDate": date,
                "endDate": date,
                "start": start_index
            }

            response = self.session.post(url, data=data)
            response_json = response.json()

            for log in response_json["obj"]["datas"]:
                logs.append(log)

            start_index = response_json["obj"]["start"]
            have_next = response_json["obj"]["haveNext"]

        logs.reverse()

        return logs

    def get_fault_logs(self, plant_id, date):
        url = "http://server.growatt.com/log/getNewPlantFaultLog"
        start_index = 1
        have_next = True

        logs = []

        while have_next is True:
            data = {
                "deviceSn": "",
                "date": date,
                "plantId": plant_id,
                "toPageNum": start_index,
                "type": "2"
            }

            response = self.session.post(url, data=data)
            print(response.text)
            response_json = response.json()

            logs += response_json["obj"]["datas"]

            if response_json["obj"]["currPage"] == response_json["obj"]["pages"]:
                have_next = False

            start_index += 1

        return logs

    def get_monthly_energy_data(self, plant_id, date):
        url = "http://server.growatt.com/energy/compare/getDevicesMonthChart"
        data = {
            "plantId": plant_id,
            "jsonData": '[{"type":"plant","sn":"225953","params":"energy,autoEnergy"}]',
            "date": date
        }

        response = self.session.post(url, data=data)
        response_json = response.json()

        daily_energy = response_json["obj"][0]["datas"]["energy"]

        return daily_energy
