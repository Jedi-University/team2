import time
from configparser import ConfigParser

from orchestrator import Orchestrator
from settings import get_workers
from show import show

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    orchestrator = Orchestrator()
    modes = ["default", "thread", "process", "async"]

    performance = {}
    for mode in modes:
        config["Build"]["mode"] = mode
        workers = get_workers(config)
        start = time.time()
        orchestrator.run(workers)
        performance[mode] = time.time() - start
        print()

    show()

    print(f"\n{performance}")
