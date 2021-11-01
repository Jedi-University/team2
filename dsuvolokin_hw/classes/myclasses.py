
from random import random as rand

def says(f,*args,**kwargs):
  def wrapper(*args,**kwargs):
    print('He/she says: ',f.__name__, f(*args,**kwargs))
  return wrapper

def thinks(f,*args,**kwargs):
  def wrapper(*args,**kwargs):
    print('He/she thinks: ',f.__name__,f(*args,**kwargs))
  return wrapper

class Scientist:
    def __init__(self,name=None,age=None,sex=None,spec=None):
      self.name = name
      self.age  = age
      self.sex  = sex
      self.spec = spec
    
    @thinks
    def think(self,*args,**kwargs):
        return rand()

    @says
    def speak(self,*args,**kwargs):
        return kwargs['t']*10


class Student(Scientist):
    def __init__(self,classroom=None,name=None,age=None,sex=None,spec=None):
        self.classroom=classroom
        super().__init__(name,age,sex,spec)
    
    @thinks
    def sum(self,a,b):
      return a+b
        
class Tutor(Scientist):
    def __init__(self,expirience=None,name=None,age=None,sex=None,spec=None):
      self.expirience=expirience
      super().__init__(name,age,sex,spec)

    def speak(self,*args,**kwargs):
      # return super().speak(**kwargs)+self.expirience
      return kwargs['t']*10+self.expirience

    @says
    def answer(self,v,*args,**kwargs):
      return pow(v,10)
