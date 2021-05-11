import csv
from datetime import datetime

from growatt.utils import check_device_type


class GrowattFileMaker:
    def write_logs_file(self, data, plant_name, device_type, dates):
        filename = f"../output/growatt/logs/{plant_name} - {dates[0]}_{dates[1]}.csv"
        headers = list(data[0].keys())

        if device_type == "inv":
            time_key = "time"
        elif device_type == "tlx":
            time_key = "calendar"

        with open(filename, "w", newline="", encoding='utf-8') as logs_file:
            file_writer = csv.writer(logs_file)
            file_writer.writerow(headers)

            for data_row in data:
                values = [str(x).replace("，", ", ") for x in list(data_row.values())]
                values[2] = str(datetime(data_row[time_key]["year"], data_row[time_key]["month"] + 1, data_row[time_key]["dayOfMonth"],
                                         data_row[time_key]["hourOfDay"], data_row[time_key]["minute"], data_row[time_key]["second"]))

                file_writer.writerow(values)

    def write_fault_logs_file(self, data, plant_name, date):
        filename = f"../output/growatt/fault_logs/{plant_name} - {date}.csv"
        headers = ["Date", "Serial Number", "Event ID", "Device Alias", "Device Type", "Desctription", "Solution"]

        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            file = csv.writer(csv_file)

            file.writerow(headers)
            for log in data:
                logs_row = []
                for key in log:
                    logs_row.append(log[key])

                file.writerow(logs_row)

    def write_monthly_report_file(self, data, plant_name, date):
        filename = f"../output/growatt/monthly_reports/{plant_name} - {date}.csv"
        headers = ["plantName", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                   "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
                   "Total(kWh)"]

        total_power = 0
        for power in data:
            total_power += power

        for _ in range(31 - len(data)):
            data.append("")
        data.append(total_power)

        data_to_write = [plant_name] + data

        with open(filename, "w", newline="") as csv_file:
            file = csv.writer(csv_file)

            file.writerow(headers)
            file.writerow(data_to_write)


class SolarEdgeFileMaker:
    def write_logs_file(self, data, plant_name, dates):
        filename = f"../output/solaredge/logs/{plant_name.replace('/', ' ')} - {dates[0]}_{dates[1]}.csv"
        headers = ["date", "totalActivePower", "dcVoltage", "groundFaultResistance", "powerLimit", "totalEnergy",
                   "temperature", "inverterMode", "operationMode", "vL1To2", "vL2To3", "vL3To1", "L1Data", "acCurrent",
                   "acVoltage", "acFrequency", "apparentPower", "activePower", "reactivePower", "cosPhi", "L2Data",
                   "acCurrent", "acVoltage", "acFrequency", "apparentPower", "activePower", "reactivePower", "cosPhi",
                   "L3Data", "acCurrent", "acVoltage", "acFrequency", "apparentPower", "activePower", "reactivePower", "cosPhi"]

        with open(filename, "w", newline="") as logs_file:
            file_writer = csv.writer(logs_file)
            file_writer.writerow(headers)

            for i, data_row in enumerate(data):
                values = list(data_row.values())

                if "groundFaultResistance" not in data_row:
                    values.insert(3, "")

                for i, data in enumerate(values[12]):
                    values.insert(13+i, values[12][data])
                values[12] = ""

                for i, data in enumerate(values[20]):
                    values.insert(21+i, values[20][data])
                values[20] = ""

                for i, data in enumerate(values[28]):
                    values.insert(29+i, values[28][data])
                values[28] = ""

                file_writer.writerow(values)

    def write_monthly_report_file(self, data, plant_name, date):
        filename = f"../output/solaredge/monthly_reports/{plant_name} - {date}.csv"
        headers = ["plantName", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                   "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
                   "Total(kWh)"]

        total_power = 0
        for power in data:
            if power["value"] != "None":
                total_power += power["value"]

        data_parsed = [day_date["value"]/1000 for day_date in data]

        for _ in range(31 - len(data)):
            data_parsed.append("")

        data_parsed.append(total_power/1000)

        data_to_write = [plant_name] + data_parsed

        with open(filename, "w", newline="") as csv_file:
            file = csv.writer(csv_file)

            file.writerow(headers)
            file.writerow(data_to_write)
