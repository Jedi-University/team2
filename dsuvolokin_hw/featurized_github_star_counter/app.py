from modules.workers import Mt_worker,Async_worker,Mp_worker
from modules.orchestrator import Orchestrator
from settings._settings import mode


if __name__ == '__main__':
    d = { Mt_worker.mode : Mt_worker, Async_worker.mode : Async_worker, Mp_worker.mode : Mp_worker}
    o = Orchestrator()
    w = o.tune(mode,d)
    print(f'using {w.mode} mode')
    w.work()
