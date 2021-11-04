import heapq


def filter(repos):
    top_repos = heapq.nlargest(20, repos, key=lambda x:int(x['stars']))
    return top_repos