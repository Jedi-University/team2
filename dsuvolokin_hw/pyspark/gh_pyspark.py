import requests
import json
import concurrent.futures
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from os import path
from shutil import rmtree 


sc = SparkContext('local')
spark = SparkSession(sc)

token = ""
base_uri = " https://api.github.com"
headers = {'Accept':"application/vnd.github+json", "authorization": f"Bearer {token}"}
filepath = 'Top.csv'

def get_orgs(batches = 2):
  org_uri = "/organizations"
  max_id = 0
  orgs_list =[]

  for i in range(batches):
    org_params = {"per_page":100, "since":max_id}
    r = requests.get(f"{base_uri}{org_uri}",params = org_params,headers = headers)
    for org in json.loads(r.text):
      orgs_list.append(org['login'])
    max_id= max([org['id'] for org in json.loads(r.text)])+1
  orgs_list=orgs_list[:3] # restrict for test
  return orgs_list

def get_repo(org):
  repo_list=[]
  r = requests.get(base_uri+f"/orgs/{org}/repos", headers = headers)
  for repo in json.loads(r.text):
    repo_list.append({"org": org, "repo_id": repo['id'], "name": repo['name'],"stars_count": repo['watchers_count']}) if repo.get('watchers_count',0)>0 else None
  return repo_list



if __name__ == '__main__':

  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      l = sum(map(get_repo,get_orgs()),[]) #flatten appended lists
   
  df = spark.createDataFrame(l)
  top = df.orderBy(col('stars_count').desc()).limit(20)

  if path.isdir(filepath):
    try:
      rmtree(f"{filepath}", ignore_errors=True)
    except Exception as e:
      print(e)

  top.repartition(1).write.csv(filepath,header='true')
