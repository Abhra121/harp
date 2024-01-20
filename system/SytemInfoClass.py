import socket
import subprocess
import json
from pyModbusTCP.client import ModbusClient

class DeviceInformation:
    def __init__(self):
        self.device_info = {
            "device_info": {
                "License_info": {
                    "serial_id": self.get_serial_id(),
                    "hardware_id": self.get_hw_id()
                },
                "Hardware_info": {
                    "CPU": {},
                    "Memory": {},
                    "Storage": {},
                    "Network_interface": {}
                },
                "Software_info": {
                    "OS": {},
                    "system_run_time": {},
                    "service_status": {
                        "harp_service": ""
                    }
                }
            }
        }

    def get_serial_id(self):
        try:
            with open('/home/pi/serialid.txt', 'r') as f:
                SerialNumber = f.read()
            return SerialNumber
        except FileNotFoundError:
            return None
        except Exception as e:
            return None

    def get_hw_id(self):
        try:
            with open('/home/pi/hardwareid.txt', 'r') as f:
                HwId = f.read()
            return int(HwId)
        except FileNotFoundError:
            return None
        except Exception as e:
            return None

    def get_service_status(self):
        try:
            service_status = subprocess.check_output("systemctl is-active harp.service", shell=True, text=True)
            #self.device_info["device_info"]["Software_info"]["service_status"]["harp_service"] = service_status.strip()
            self.device_info[""] = service_status.strip()
        except subprocess.CalledProcessError:
            print("Error retrieving harp.service status.")

    def get_cpu_info(self):
        try:
            cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            hardware = self.extract_cpu_info(cpu_info, "Hardware")
            revision = self.extract_cpu_info(cpu_info, "Revision")
            serial = self.extract_cpu_info(cpu_info, "Serial")
            model = self.extract_cpu_info(cpu_info, "Model")

            lscpu_info = subprocess.check_output("lscpu", shell=True, text=True)
            architecture = self.extract_lscpu_info(lscpu_info, "Architecture")
            cpus = self.extract_lscpu_info(lscpu_info, "CPU(s)")
            model_name = self.extract_lscpu_info(lscpu_info, "Model name")

            #self.device_info["device_info"]["Hardware_info"]["CPU"] = {
            self.device_info[""] = {
                "Hardware": hardware,
                "Revision": revision,
                "Serial": serial,
                "Model": model,
                "Architecture": architecture,
                "CPUs": cpus,
                "ModelName": model_name
            }

        except subprocess.CalledProcessError:
            print("Error retrieving CPU information.")

    def get_memory_info(self):
        try:

            mem_info = subprocess.check_output("cat /proc/meminfo", shell=True, text=True)
            mem_total = self.extract_mem_info(mem_info, "MemTotal")
            mem_free = self.extract_mem_info(mem_info, "MemFree")
            mem_available = self.extract_mem_info(mem_info, "MemAvailable")

            mem_total = self.convert_to_gb(mem_total)
            mem_free = self.convert_to_gb(mem_free)
            mem_available = self.convert_to_gb(mem_available)

            #self.device_info["device_info"]["Hardware_info"]["Memory"] = {
            self.device_info[""] = {    
                "MemTotal": mem_total,
                "MemFree": mem_free,
                "MemAvailable": mem_available
            }

        except subprocess.CalledProcessError:
            print("Error retrieving memory information.")

    def get_storage_info(self):
        try:
            df_info = subprocess.check_output("df -h /", shell=True, text=True)
            total_storage = self.extract_df_info(df_info, "/dev/root", "Size")
            used_storage = self.extract_df_info(df_info, "/dev/root", "Used")
            free_storage = self.extract_df_info(df_info, "/dev/root", "Avail")

            total_storage = self.convert_to_gb(total_storage)
            used_storage = self.convert_to_gb(used_storage)
            free_storage = self.convert_to_gb(free_storage)

            #self.device_info["device_info"]["Hardware_info"]["Storage"] = {
            self.device_info[""] = {    
                "TotalStorage": total_storage,
                "UsedStorage": used_storage,
                "FreeStorage": free_storage
            }

        except subprocess.CalledProcessError:
            print("Error retrieving storage information.")

    def get_network_interface_info(self):
        try:
            netstat_info = subprocess.check_output("netstat -i", shell=True, text=True)
            interfaces = [line.split()[0] for line in netstat_info.split("\n")[2:] if line]
            #self.device_info["device_info"]["Hardware_info"]["Network_interface"] = {}
            self.device_info[""] = {}

            for interface in interfaces:
                ip_address = self.get_ip_address(interface)
                #self.device_info["device_info"]["Hardware_info"]["Network_interface"][interface] = {
                self.device_info[""] = {
                    "IPAddress": ip_address
                }

        except subprocess.CalledProcessError:
            print("Error retrieving network interface information.")

    def get_ip_address(self, interface):
        try:
            ip_info = subprocess.check_output(f"ifconfig {interface} | awk '/inet /{{print $2}}'", shell=True, text=True)
            ip_address = ip_info.strip()
            return ip_address if ip_address else "Not available"
        except subprocess.CalledProcessError:
            return "Not available"

    def extract_df_info(self, df_info, filesystem, key):
        lines = df_info.splitlines()
        for line in lines:
            if filesystem in line:
                return line.split()[1] if key == "Size" else line.split()[2] if key == "Used" else line.split()[3]
        return "Not available"

    def extract_cpu_info(self, cpu_info, key):
        lines = cpu_info.splitlines()
        for line in lines:
            if key in line:
                return line.split(":")[1].strip()
        return "Not available"

    def extract_lscpu_info(self, lscpu_info, key):
        lines = lscpu_info.splitlines()
        for line in lines:
            if key in line:
                return line.split(":")[1].strip()
        return "Not available"

    def extract_mem_info(self, mem_info, key):
        lines = mem_info.splitlines()
        for line in lines:
            if key in line:
                return line.split(":")[1].strip()
        return "Not available"

    def convert_to_gb(self, value):
        try:
            value_in_kb = int(value.split()[0])
            value_in_gb = value_in_kb / (1024 ** 2)
            return f"{value_in_gb:.2f} GB"
        except ValueError:
            return value

    def extract_os_info(self, os_info, key):
        lines = os_info.splitlines()
        for line in lines:
            if key in line:
                return line.split("=")[1].strip('"')
        return "Not available"

    def get_os_info(self):
        try:
            os_info = subprocess.check_output("cat /etc/os-release", shell=True, text=True)
            os_name = self.extract_os_info(os_info, "NAME")
            os_pretty_name = self.extract_os_info(os_info, "PRETTY_NAME")

            #self.device_info["device_info"]["Software_info"]["OS"] = {
            self.device_info[""] = {
                "Name": os_name,
                "PrettyName": os_pretty_name
            }
        except subprocess.CalledProcessError:
            print("Error retrieving OS information.")

    def get_system_run_time(self):
        try:
            uptime_info = subprocess.check_output("uptime -p", shell=True, text=True)
            #self.device_info["device_info"]["Software_info"]["system_run_time"] = {
            self.device_info[""] = {
                "uptime": uptime_info.strip()
            }
        except subprocess.CalledProcessError:
            print("Error retrieving system run time information.")

    def get_device_info(self):
        self.get_cpu_info()
        self.get_memory_info()
        self.get_storage_info()
        self.get_network_interface_info()
        self.get_os_info()
        self.get_system_run_time()
        self.get_service_status()
    def to_json(self):
        return json.dumps(self.device_info, indent=4)
