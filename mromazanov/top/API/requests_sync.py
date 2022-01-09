import requests
from API.requests import Requests

class Requests_Sync(Requests):
    def __init__(self, Authorization:str, *args, **kwargs):
        self.headers = {"Authorization":f"token {Authorization}"}

    def request(self, url, *args, **kwargs):
        return requests.get(url, params=kwargs, headers=self.headers)