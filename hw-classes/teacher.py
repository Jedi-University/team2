from homo_sapiens import HomoSapiens, Gender


class Teacher(HomoSapiens):
    def __init__(
        self, name: str, age: int, gender: Gender, discipline_name: str, experience: int
    ):
        super().__init__(self, name, age, gender)
        self.__discipline_name = discipline_name
        self.__experience = experience

    def speak(self, t) -> float:
        return super().speak(t) + self.__experience

    def answer(self, v):
        return v ** 10

    @property
    def discipline_name(self):
        return self.__discipline_name

    @property
    def experience(self):
        return self.__experience

    @experience.setter()
    def experience(self, experience):
        if experience >= 0:
            self.__experience = experience
        else:
            raise ValueError("Invalid experience value.")
