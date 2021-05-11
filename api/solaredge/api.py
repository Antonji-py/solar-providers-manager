import requests
import calendar


class SolarEdgeApi:
    def __init__(self, api_token, username, password):
        self.api_token = api_token
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.base_url = "https://monitoringapi.solaredge.com"
        self.params = {
            "api_key": api_token
        }

    def get_plants(self):
        url = f"{self.base_url}/sites/list"

        response = requests.get(url, params=self.params)
        response_json = response.json()

        plants_list = []

        for plant in response_json["sites"]["site"]:
            plant_data = {}
            plant_data.update({"id": str(plant["id"])})
            plant_data.update({"plant_name": plant["name"]})
            try:
                plant_data.update({"plant_image": "https://monitoringapi.solaredge.com/" + plant["uris"]["SITE_IMAGE"]})
            except KeyError:
                plant_data.update({"plant_image": "null"})

            plants_list.append(plant_data)

        return plants_list
    
    def get_plant_devices(self, plant_id):
        url = f"{self.base_url}/equipment/{plant_id}/list"

        devices = []
        
        response = requests.get(url, params=self.params)
        response_json = response.json()

        for device in response_json["reporters"]["list"]:
            device_data = {}
            device_data.update({"plant_id": plant_id})
            device_data.update({"serial_number": device["serialNumber"]})
            device_data.update({"device_model": device["model"]})

            devices.append(device_data)

        return devices

    def get_all_devices(self):
        plants = self.get_plants()
        plants_ids = [plant["id"] for plant in plants]

        all_devices = []

        for plant_id in plants_ids:
            devices = self.get_plant_devices(plant_id)
            plant_devices = []

            for device in devices:
                plant_devices.append(device)

            all_devices.append(plant_devices)

        return all_devices

    def get_daily_logs(self, plant_id, device_id, date):
        url = f"{self.base_url}/equipment/{plant_id}/{device_id}/data"
        params = {
            "startTime": date + " 00:00:00",
            "endTime": date + " 23:59:59",
            "api_key": self.api_token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        return response_json

    def get_fault_logs(self, plant_id):
        url = f"https://monitoring.solaredge.com/solaredge-apigw/api/rna/v1.0/site/1916310/alerts?count=20&page=1"
        # url = "https://monitoringapi.solaredge.com/sites/list?api_key="
        response = self.session.get(url)

        print(response.text)
        print(response.status_code)

    def get_monthly_energy_data(self, plant_id, date):
        year = date.split("-")[0]
        month = date.split("-")[1]
        last_day = calendar.monthrange(int(year), int(month))[1]

        url = f"{self.base_url}/site/{plant_id}/energy"
        params = {
            "timeUnit": "DAY",
            "startDate": f"2021-{month}-01",
            "endDate": f"2021-{month}-{last_day}",
            "api_key": self.api_token
        }
        
        response = requests.get(url, params=params)
        response_json = response.json()

        daily_energy = response_json["energy"]["values"]

        return daily_energy

#
# s = SolarEdgeApi("NBIADFNFNCQCURNB0SI3YCA029XDK308", "biuro@fastenergy.pl", "cWO5Cw5&2")
# a = s.get_fault_logs("@")


