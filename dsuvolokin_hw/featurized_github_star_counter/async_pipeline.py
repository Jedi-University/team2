from  async_modules._01_async_get_data import *
from  async_modules._02_async_save_data import *
from  async_modules._03_async_read_and_drop_data import *
# from async_modules import *
import constants as const

orgs_list, base_uri, org_uri, headers,repo_list \
= const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(main(orgs_list, base_uri, org_uri, headers))
    
#     top_repos = sorted(result, key=lambda l: l['stars_count'])[:-21:-1]

#     print('saving data')
#     save_data(top_repos) #no async

#     read_data() #no async

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_main(orgs_list, base_uri, org_uri, headers))
    
    top_repos = sorted(result, key=lambda l: l['stars_count'])[:-21:-1]

    print('saving data')
    save_data(top_repos) #no async

    read_data() #no async