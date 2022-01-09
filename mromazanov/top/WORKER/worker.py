import heapq
from API.requests import Requests
from heapq import nlargest

class Worker():
    def __init__(self, top_count:int, requests:Requests, orgs_count:int=200, per_page:int=100, *args, **kwargs):
        self.top_count = top_count
        self.orgs_count = orgs_count
        self.requests = requests
        self.per_page = per_page

    def get_info(self, url:str, *args, **kwargs):
        response = self.request_info(url, per_page=self.per_page)
        if 'next' in response.links:
            result = {'json':response.json(),'next':response.links['next']['url']}
        else:
            result = {'json':response.json()}
        return result

    def request_info(self, url:str, **kwargs):
        response = self.requests.request(url, **kwargs)
        return response

    def top_by_stars(self, repos_list:list):
        top_repos = heapq.nlargest(self.top_count, repos_list, key=lambda x:int(x['stars']))
        #top_repos.sort(key=lambda x:int(x['stars']),reverse=True)
        return top_repos

    def run(self):
        pass