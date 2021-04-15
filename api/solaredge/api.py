import requests
import time
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

        self.login()

    def login(self):
        session = requests.Session()

        site_key = "6LeWb6cUAAAAAF-6EUPgS0d-OF0KcvGq-zT1w_Al"
        captcha_key = ""
        domain = "https://monitoring.solaredge.com"

        captcha_id = self.session.post(f"http://2captcha.com/in.php?key={captcha_key}&method=userrecaptcha&googlekey={site_key}&pageurl={domain}").text.split("|")[1]
        recaptcha_answer = self.session.get(f"http://2captcha.com/res.php?key={captcha_key}&action=get&id={captcha_id}").text

        while recaptcha_answer == "CAPCHA_NOT_READY":
            time.sleep(10)
            recaptcha_answer = self.session.get(f"http://2captcha.com/res.php?key={captcha_key}&action=get&id={captcha_id}").text

        recaptcha_answer = recaptcha_answer.split('|')[1]

        url = "https://monitoring.solaredge.com/solaredge-web/p/submitLogin"
        data = {
            "cmd": "login",
            "demo": "false",
            "g-recaptcha-response": recaptcha_answer,
            "username": self.username,
            "password": self.password
        }

        response = session.post(url, data=data)
        response = session.get("https://monitoring.solaredge.com/solaredge-web/p/sites/sitesTable?sort=maxImpact&dir=DESC&start=0&limit=20&status=0&category=0&filter=&showMap=false&alertImpact=ALL")
        print(response.text)
        print(response.status_code)

        # url = "https://monitoring.solaredge.com/solaredge-web/p/home"
        # cookies = {'SolarEdge_SSO-1.4': '9366e830acb384e0d72c4d591b79e5f3c0fa4a9349340798aef88f28e579584b', 'CSRF-TOKEN': 'E1753052DAC9AF4F5B20B0162B5CA7E252A7DA16479A3D857F853A28E0F3F18DF01E10163F8A0C664A5CA48415A03619D8F0', 'SolarEdge_Locale': 'pl_PL', 'JSESSIONID': '0775D869BCE7000A9F89A4FAF49E2175F990009CBDEA80C154FF4DB0B341DEDC5F582D547EEB4E8400D857DA97ED9A7919D652E9BDC5E07315ECF07A90DA7832868903B674C4E6D2FC9F91540B0794FCDABF04F57D6FD9AE7DAA7AF0F30A4F78D3C9C21217116D4EFFE8FEBEE01BF97D34B99AF8C5AB0FCB66B669A6C5C8AE48'}
        #
        # headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        #            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        #            "x-csrf-token": session.cookies.get_dict()["CSRF-TOKEN"]}
        # session.headers = headers
        #
        # # session.cookies.update(cookies)
        # data = (
        #         {"fieldFilterOperator": "IN",
        #          "fieldName": "status",
        #          "fieldValue": ["CLOSED"]}
        # )
        # response = session.post("https://monitoring.solaredge.com/solaredge-apigw/api/rna/v1.0/site/1916310/alerts?count=20&page=1", data=data)
        # print(session.cookies.get_dict())
        # print(response.status_code)
        # print(response.text)

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
s = SolarEdgeApi("NBIADFNFNCQCURNB0SI3YCA029XDK308", "biuro@fastenergy.pl", "cWO5Cw5&2")
# a = s.get_fault_logs("@")


