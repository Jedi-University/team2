import requests
from . import auth


def org_request(last_id):
    return requests.get(f'https://api.github.com/organizations'
        f'?since={last_id}&per_page=100', auth=auth.auth())


def repos_request(org_name, page):
    return requests.get(f'https://api.github.com/orgs/{org_name}'
        f'/repos?per_page=100&page={page}', auth=auth.auth())