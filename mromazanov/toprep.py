import requests
import json
import time
import heapq

def get_names(orgs):
    names = []
    for entry in orgs:
        names.append(entry['login'])
    return names


def get_orgs(pages):
    global last_id
    text = ''
    iteration = 0
    while iteration < pages:
        response_API = requests.get(f'https://api.github.com/organizations?since={last_id}&per_page=100').json()
        last_id = response_API[-1]['id']
        iteration += 1
        yield response_API
    

def get_repos(name):
    global repoStars
    response_API = requests.get(f'https://api.github.com/orgs/{name}/repos').json()
    for repo in response_API:
        id = repo['id']
        #print(id)
        stars = repo['stargazers_count']
        #print(stars)
        repoStars[id] = stars
    return response_API


last_id = 0
orgs = []
repoStars = {}
repos = []

for i in get_orgs(2):
    orgs.extend(i)
names = get_names(orgs)
#print(names)
repos.extend(get_repos("Jedi-University"))
for i in range(20):
    repos.extend(get_repos(names[i]))
#for name in names:
#    repos.extend(get_repos(name))
repoStars = heapq.nlargest(20, repoStars.items(), key=lambda i: i[1])
for repo in repos:
    print(repo['full_name'])
print(repoStars)
#to_file = text
#filepath = './1'
#with open(filepath, "w") as f:
#    f.write(to_file)
