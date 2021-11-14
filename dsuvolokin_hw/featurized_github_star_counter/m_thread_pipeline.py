from threading import Thread
from  m_thread_modules._01_mt_get_data import *
from  m_thread_modules._02_mt_save_data import *
from  m_thread_modules._03_mt_read_and_drop_data import *
import constants as const

# orgs_list, base_uri, org_uri, headers,repo_list \
# = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list

# if __name__ == "__main__":
#   print('fetching organizations')
#   thread1 = Thread(target = get_org, args = ([orgs_list, base_uri, org_uri, headers],))
#   thread1.start()
#   thread1.join()

#   orgs_list=orgs_list[:3] #restricted for test

#   print('fetching repositories')
#   orgs_and_args = [[org,headers,base_uri,repo_list] for org in orgs_list]
#   for a in orgs_and_args:
#     thread2 =  Thread(target = get_repo, args = (a,))
#     thread2.start()
#     thread2.join()

#   top_repos = sorted(repo_list, key=lambda l: l['stars_count'])[:-21:-1]

#   print('saving data')
#   save_data(top_repos)

#   read_data()

def main():
  orgs_list, base_uri, org_uri, headers,repo_list \
  = const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list
  print('fetching organizations')
  thread1 = Thread(target = get_org, args = ([orgs_list, base_uri, org_uri, headers],))
  thread1.start()
  thread1.join()

  orgs_list=orgs_list[:3] #restricted for test

  print('fetching repositories')
  orgs_and_args = [[org,headers,base_uri,repo_list] for org in orgs_list]
  for a in orgs_and_args:
    thread2 =  Thread(target = get_repo, args = (a,))
    thread2.start()
    thread2.join()

  top_repos = sorted(repo_list, key=lambda l: l['stars_count'])[:-21:-1]

  print('saving data')
  save_data(top_repos)

  read_data()