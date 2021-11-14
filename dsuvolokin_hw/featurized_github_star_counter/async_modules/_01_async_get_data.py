import asyncio
import aiohttp
import json
import requests

def get_org(*args): #здесь асинк невозможен, т.к.при каждом следующем запросе используем id из предыдущего
  orgs_list=args[0]
  base_uri=args[1]
  org_uri=args[2]
  headers=args[3]
  max_id = 0
  for i in range(2):
    org_params = {"per_page":100, "since":max_id}
    r = requests.get(f"{base_uri}{org_uri}",params = org_params,headers = headers)
    for org in json.loads(r.text):
      orgs_list.append(org['login'])
    max_id= max([org['id'] for org in json.loads(r.text)])+1
  return orgs_list

async def get_repo(session,org,headers,base_uri):
  async with session.get(base_uri+f"/orgs/{org}/repos", headers = headers) as response:
    return await response.text()

async def async_main(*args):
    orgs_list, base_uri, org_uri, headers = args[0],args[1],args[2],args[3]
    tasks = []
    async with aiohttp.ClientSession() as session:
        l = get_org(orgs_list, base_uri, org_uri, headers)[:3] #restricted for test
        orgs_and_args = [[org,headers,base_uri] for org in l]
        for o in orgs_and_args:
            tasks.append(get_repo(session,*o))
        r = await asyncio.gather(*tasks)
        repo_list = []
        for txt in r:
            rep = json.loads(txt)
            for repo in rep:
              repo_list.append({"org": repo['owner']['login'], "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None        
        return repo_list