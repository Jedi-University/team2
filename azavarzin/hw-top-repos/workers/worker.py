class Worker:
    def exec(self, *args, **kwargs):
        print(f"{self.__class__.__name__} is working")
