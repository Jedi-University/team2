import random
from enum import Enum


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    ANOTHER = 3


class HomoSapiens:

    LIMIT_OF_HUMAN_LIFE = 125

    def __init__(self, name: str, age: int, gender: Gender):
        self.__name = name
        self.__age = age
        self.__gender = gender

    # методы think и speak спокойно можно сделать методыми класса (@classmethod),
    # т.к. они не используют атрибуты инстанса, но пусть будет так
    def think(self):
        """Returns a random number between 0 and 1."""
        return random.random()

    def think(self, a, b):
        """Returns a random floating point number from a range [a, b]."""
        return random.uniform(a, b)

    def speak(self, t):
        return t + 10

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @age.setter()
    def age(self, age):
        if 0 < age < HomoSapiens.LIMIT_OF_HUMAN_LIFE:
            self.__age = age
        else:
            raise ValueError('Impossible age value.')

    @property
    def gender(self):
        return self.__gender
