from ..API.API_request import org_request


def get_orgs(pages):
    iteration = 0
    last_id = 0
    while iteration < pages:
        response_API = org_request(last_id).json()
        last_id = response_API[-1]['id']
        iteration += 1
        yield response_API


def get_names(orgs):
    names = []
    for entry in orgs:
        names.append(entry['login'])
    return names