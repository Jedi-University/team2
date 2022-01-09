from app_config import *
import sys
import time

class App():
    def __init__(self, orch, db):
        self.orch = orch
        self.db = db

    def fetch(self):
        top_repos = self.orch.run()
        db.create_db(top_repos=top_repos)

    def show(self):
        show = db.get()
        show.sort(key=lambda x:x.stars_count, reverse=True)
        for item in show:
            print(f'{item.id}\t{item.org_name}\t{item.repo_name}\t{item.stars_count}\n')

if __name__ == '__main__':
    app = App(orch=orchestrators[sys.argv[1]], db=db)
    t0 = time.time()
    app.fetch()
    app.show()
    t1 = time.time()
    print("Time elapsed: ", t1 - t0) # CPU seconds elapsed (floating point)