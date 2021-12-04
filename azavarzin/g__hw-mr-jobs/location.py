import requests
from retry import retry


@retry()
def get_location_by_ip(ip: str) -> str:
    location = requests.get(f"https://ip2c.org/{ip}").text.split(";")[-1]
    return location