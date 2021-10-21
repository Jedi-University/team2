import random


class Human():
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    

    def think(self):
        return(int(random.random() * 1000))
    

    def speak(self, t):
        return(t+10)

    
    def info(self):
        return(self.name, self.age, self.gender)


class Student(Human):
    def __init__(self, name, age, gender, classnum, spec):
        self.name, self.age, self.gender, self.classnum, self.spec = name, age, gender, classnum, spec
    

    def sum(self, a, b):
        return(a+b)
    

class Teacher(Human):
    def __init__(self, name, age, gender, subject_name, work_experience):
        self.name, self.age, self.gender, self.subject_name, self.work_experience = name, age, gender, subject_name, work_experience


    def speak(self, t):
        return(t + self.work_experience + 10)


    def answer(self, v):
        return(v**10)



Petr = Student("Petr", 19, 'm', 234, 'Computer science')
Galina = Teacher("Galina", 38, 'f', 'OOP', 13)
print(Petr.info(), Galina.info())
print(Petr.think(), Galina.think())
print(Petr.speak(54), Galina.speak(54))
print(Galina.answer(Petr.sum(5, 10)))