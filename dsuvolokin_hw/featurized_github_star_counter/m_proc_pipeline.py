from multiprocessing import Pool
from functools import reduce
from  m_proc_modules._01_mp_get_data import *
from  m_proc_modules._02_mp_save_data import *
from  m_proc_modules._03_mp_read_and_drop_data import *
import constants as const

# orgs_list, base_uri, org_uri, headers,repo_list \
# = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list

# if __name__=='__main__':
#   with Pool(5) as p:

#     print('fetching organizations')
#     l=p.map(get_org,[[ orgs_list, base_uri, org_uri, headers]])[0][:3] #restricted for test

#     print('fetching repositories')
#     orgs_and_args = [[org,headers,base_uri,repo_list] for org in l]
#     r = p.map(get_repo,orgs_and_args)
#     rl=reduce(lambda l,m:l+m,r)
#     top_repos = sorted(rl, key=lambda l: l['stars_count'])[:-21:-1]

#     print('saving data')
#     save_data(top_repos)

#     read_data()


def main():
  orgs_list, base_uri, org_uri, headers,repo_list \
  = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list
  
  with Pool(5) as p:

    print('fetching organizations')
    l=p.map(get_org,[[ orgs_list, base_uri, org_uri, headers]])[0][:3] #restricted for test

    print('fetching repositories')
    orgs_and_args = [[org,headers,base_uri,repo_list] for org in l]
    r = p.map(get_repo,orgs_and_args)
    rl=reduce(lambda l,m:l+m,r)
    top_repos = sorted(rl, key=lambda l: l['stars_count'])[:-21:-1]

    print('saving data')
    save_data(top_repos)

    read_data()