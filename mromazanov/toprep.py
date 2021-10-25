import requests
import json
import time
import heapq

def get_names(text):
    names = []
    text = text.strip('[]/{/}')
    entries = text.split("},{")
    for entry in entries:
        names.append(entry[9:entry.find(',')-1])
    return names


def get_last_id(text):
    start = text.rfind('"id":')
    end = text.find(",",start)
    return text[start+5:end]


def get_orgs(pages):
    global last_id
    text = ''
    iteration = 0
    while iteration < pages:
        response_API = requests.get(f'https://api.github.com/organizations?since={last_id}&per_page=100')
        text = response_API.text
        last_id = get_last_id(text)
        iteration += 1
        yield text
    

def get_repos(name):
    pass


last_id = 0
text = ''





for i in get_orgs(2):
    text += str(i)
names = get_names(text)
print(names)
#to_file = text
#filepath = './1'
#with open(filepath, "w") as f:
#    f.write(to_file)
