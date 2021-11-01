
'''
Используя GitHub API для организаций (https://docs.github.com/en/rest/reference/orgs) для первых 200 организаций 
нужно подсчитать ТОП-20 самых "звездных" репозиториев(т.е. те репозитории у которых больше всего звездочек среди всех организаций). 
Полученный ТОП нужно сохранить в базу используя SQLAlchemy в следующем формате Top(id, org_name, repo_name, stars_count). 
В приложении должно быть 2 команды 1 команда: fetch, которая забирает данные с github, находит ТОП и сохраняет его в базу; 
2 команда: show достает из базы ТОП и выводит на экран. В качестве базы нужно использовать sqllite.
'''


import requests
import json
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine,Table,Column,Integer,String

print("start fetching...")

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///github_stars.db')

Base = declarative_base()

base_uri = " https://api.github.com"
org_uri = "/organizations"
max_id = 0
orgs_list =[]
repo_list = []
rating_set = set()
token = "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"
headers = {'Accept':"application/vnd.github+json", "authorization": f"Bearer {token}"}

for i in range(2):
  org_params = {"per_page":100, "since":max_id}
  r = requests.get(base_uri+org_uri,params = org_params,headers = headers)
  for org in json.loads(r.text):
    orgs_list.append(org['login'])
  max_id= max([org['id'] for org in json.loads(r.text)])+1

# for org in orgs_list[:5]:
for org in orgs_list:
  r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
  for repo in json.loads(r.text):
    repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None

repo_list_sorted_by_stars = sorted(repo_list, key=lambda l: l['stars_count'])[:-21:-1]

repo_table = Table(
    'repo',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('org', String(50)),
    Column('repo_id', Integer),
    Column('name', String(50)),
    Column('stars_count', Integer)
)

class Repo(Base):
  __table__ = repo_table

  def __init__(self,org=None,repo_id=None,repo_name=None,name=None,stars_count=None):
    self.org=org
    self.repo_id=repo_id
    self.repo_name=repo_name
    self.name=name
    self.stars_count=stars_count
    

Base.metadata.create_all(engine)

engine.execute(Repo.__table__.insert(),repo_list_sorted_by_stars)


print("fetching complete")

