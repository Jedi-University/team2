import simple_modules._01_get_data           as get_data
import simple_modules._02_save_data          as save_data
import simple_modules._03_read_and_drop_data as read_data
import constants as const

orgs_list, base_uri, org_uri, headers,repo_list \
= const.orgs_list, const.base_uri, const.org_uri,const.headers, const.repo_list

repos = get_data.get_data()
# repos = get_data.get_data(test=False)

save_data.save_data(repos)

read_data.read_data()

