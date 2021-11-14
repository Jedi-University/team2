import requests
import json
from gh_token import gh_token as token

def get_data(test=True):

  print("start fetching...")

  base_uri = " https://api.github.com"
  org_uri = "/organizations"
  max_id = 0
  orgs_list =[]
  repo_list = []
  headers = {'Accept':"application/vnd.github+json", "authorization": f"Bearer {token}"}

  for i in range(2):
    org_params = {"per_page":100, "since":max_id}
    r = requests.get(f"{base_uri}{org_uri}",params = org_params,headers = headers)
    for org in json.loads(r.text):
      orgs_list.append(org['login'])
    max_id= max([org['id'] for org in json.loads(r.text)])+1

  orgs_list=orgs_list[:3] if test else None

  for org in orgs_list:
    r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
    for repo in json.loads(r.text):
      repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None

  print("fetching complete")
  
  return sorted(repo_list, key=lambda l: l['stars_count'])[:-21:-1]