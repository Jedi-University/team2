from .worker import Worker
from ..API.API_request import APIRequest


class OrgWorker(Worker):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Org', self.type])
        self.API = APIRequest()

    def get_orgs(self, pages):
        iteration = 0
        last_id = 0
        while iteration < pages:
            response_API = self.API.org_request(last_id).json()
            try:
                last_id = response_API[-1]['id']
                iteration += 1
                yield response_API
            except KeyError:
                print(response_API)
                exit()

    def get_names(self, orgs):
        names = []
        for entry in orgs:
            names.append(entry['login'])
        return names