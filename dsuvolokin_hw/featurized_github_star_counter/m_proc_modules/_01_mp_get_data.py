import requests
import json


def get_org(*args):
  orgs_list=args[0][0]
  base_uri=args[0][1]
  org_uri=args[0][2]
  headers=args[0][3]
  max_id = 0
  for i in range(2):
    org_params = {"per_page":100, "since":max_id}
    r = requests.get(f"{base_uri}{org_uri}",params = org_params,headers = headers)
    for org in json.loads(r.text):
      orgs_list.append(org['login'])
    max_id= max([org['id'] for org in json.loads(r.text)])+1
  return orgs_list

def get_repo(*args):
  org=args[0][0]
  headers = args[0][1]
  base_uri=args[0][2]
  repo_list = args[0][3]
  r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
  for repo in json.loads(r.text):
    repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None
  return repo_list




