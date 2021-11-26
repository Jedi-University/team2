class Orchestrator():
    def __init__(self):
        pass

    def tune(self,mode,classes_dict):
        return classes_dict[mode]()
		