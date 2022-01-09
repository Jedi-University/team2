from sqlalchemy.sql.expression import table
from WORKER import *
from ORCH import *
from DB.db import *
from API import *
from githubcred import cred


db = Db()

config_orgs_top = {'orgs_count':200,
'top_count':20}

requests = Requests_Sync(**cred)

async_requests = RequestsAsync(**cred)

config = {**config_orgs_top, 'requests':requests}

config_async = {**config_orgs_top, 'requests':async_requests}

workers = {'org': OrgWorker(**config),
           'repo': RepoWorker(**config),
           'filter': FilterWorker(**config)}

async_workers = {'org': OrgWorker(**config),
           'repo': AsyncRepoWorker(**config_async),
           'filter': FilterWorker(**config)}

orchestrators = {'seq':SeqOrch(workers=workers),
'thread': ThreadOrch(workers=workers),
'proc': ProcessOrch(workers=workers),
'async': AsyncOrch(workers=async_workers)}