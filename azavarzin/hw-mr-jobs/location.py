import requests
from retry import retry


@retry()
def get_location_by_ip(ip: str) -> str:
    url = "https://ip2c.org/"
    location = requests.get(f"{url}{ip}").text.split(";")[-1]
    return location