from homo_sapiens import HomoSapiens, Gender


class Student(HomoSapiens):
    
    def __init__(self, name: str, age: int, gender: Gender,
                 class_number: int, speciality: str):
        super().__init__(self, name, age, gender)
        self.__class_number = class_number
        self.__speciality = speciality
        
    def sum(self, a: float, b: float) -> float:
        """The student knows how to add not only prime numbers, but also float, intelligent student."""
        return a + b

    @property
    def class_number(self):
        return self.__class_number

    @class_number.setter()
    def class_number(self, class_number):
        if class_number > 0:
            self.__class_number = class_number
        else:
            raise ValueError('Invalid class number value.')

    @property
    def speciality(self):
        return self.__speciality


    