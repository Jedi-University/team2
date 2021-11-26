from sqlalchemy import create_engine 
from os import remove,path
import requests
import json
from threading import Thread
from multiprocessing import Pool
from functools import reduce
import asyncio
import aiohttp
import settings.constants as const

class Worker():
    def __init__(self):
        pass

    mode = 'must be overrided'

    def get_org(self,*args):
        raise NotImplementedError

    def get_repo(self,*args):
        raise NotImplementedError

    def save_data(self,repo_list):
        engine = create_engine('sqlite:///github_stars.db')
        conn = engine.connect()
        conn.execute("create table if not exists repo (id integer,org string(50), repo_id integer, name string(50),stars_count integer) ")
        for repo in repo_list:
            conn.execute(f"insert into repo (org,repo_id,name,stars_count) values (\'{repo['org']}\',{repo['repo_id']},\'{repo['name']}\',{repo['stars_count']})")

    def read_data(self,*args):
        if path.isfile('github_stars.db'):
            engine = create_engine('sqlite:///github_stars.db')
            print("most famous repos and its' owners:")
            with engine.connect() as connection:
                result = connection.execute("select * from repo")
                for row in result:
                    print("organization: ",row['org'],"|", "repo_id: ", row["repo_id"],"|","repo_name: ",row['name'],"|","stars_count: ", row['stars_count'])
            try:
                remove('github_stars.db')
            except Exception as e:
                print("database not dropped")
                print(e)
            else:
                msg = "data dropped successfully"
                print("-"*len(msg), msg, "-"*len(msg),sep='\n')
        else:
            print('database is missing')

    def work(self):
        raise NotImplementedError


class Mt_worker(Worker):
    def __init__(self):
        pass

    mode = 'multithreading'

    def get_org(self,*args):
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

    def get_repo(self,*args):
      org=args[0][0]
      headers = args[0][1]
      base_uri=args[0][2]
      repo_list = args[0][3]
      r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
      for repo in json.loads(r.text):
        repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None
      return repo_list

    def work(self):
          orgs_list, base_uri, org_uri, headers,repo_list \
          = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list
          print('fetching organizations')
          thread1 = Thread(target = self.get_org, args = ([orgs_list, base_uri, org_uri, headers],))
          thread1.start()
          thread1.join()
          orgs_list=orgs_list[:3] #restricted for test
          print('fetching repositories')
          orgs_and_args = [[org,headers,base_uri,repo_list] for org in orgs_list]
          for a in orgs_and_args:
            thread2 =  Thread(target = self.get_repo, args = (a,))
            thread2.start()
            thread2.join()
          top_repos = sorted(repo_list, key=lambda l: l['stars_count'])[:-21:-1]
          print('saving data')
          self.save_data(top_repos)
          self.read_data()

class Mp_worker(Worker):
    def __init__(self):
        pass

    mode = 'multiprocessing'

    def get_org(self,*args):
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

    def get_repo(self,*args):
      org=args[0][0]
      headers = args[0][1]
      base_uri=args[0][2]
      repo_list = args[0][3]
      r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
      for repo in json.loads(r.text):
        repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None
      return repo_list

    def work(self):
      orgs_list, base_uri, org_uri, headers,repo_list \
      = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list
      with Pool(5) as p:
        print('fetching organizations')
        l=p.map(self.get_org,[[ orgs_list, base_uri, org_uri, headers]])[0][:3] #restricted for test
        print('fetching repositories')
        orgs_and_args = [[org,headers,base_uri,repo_list] for org in l]
        r = p.map(self.get_repo,orgs_and_args)
        rl=reduce(lambda l,m:l+m,r)
        top_repos = sorted(rl, key=lambda l: l['stars_count'])[:-21:-1]
        print('saving data')
        self.save_data(top_repos)
        self.read_data()


class Async_worker(Worker):
    def __init__(self):
        pass

    mode = 'async'

    def get_org(self,*args): #здесь асинк невозможен, т.к.при каждом следующем запросе используем id из предыдущего
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

    async def get_repo(self,session,org,headers,base_uri):
      async with session.get(base_uri+f"/orgs/{org}/repos", headers = headers) as response:
        return await response.text()

    async def async_main(self,*args):
        orgs_list, base_uri, org_uri, headers = args[0],args[1],args[2],args[3]
        tasks = []
        async with aiohttp.ClientSession() as session:
            print('fetching orgs')
            l = self.get_org(orgs_list, base_uri, org_uri, headers)[:3] #restricted for test
            orgs_and_args = [[org,headers,base_uri] for org in l]
            print('fetching repos')
            for o in orgs_and_args:
                tasks.append(self.get_repo(session,*o))
            r = await asyncio.gather(*tasks)
            repo_list = []
            for txt in r:
                rep = json.loads(txt)
                for repo in rep:
                  repo_list.append({"org": repo['owner']['login'], "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None        
            return repo_list

    def work(self):
        orgs_list, base_uri, org_uri, headers, repo_list = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.async_main(orgs_list, base_uri, org_uri, headers))
        top_repos = sorted(result, key=lambda l: l['stars_count'])[:-21:-1]
        print('saving data')
        self.save_data(top_repos) #no async
        self.read_data() #no async

