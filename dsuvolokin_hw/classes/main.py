from myclasses import *

#testing Student class
print('-'*11,'Student methods','-'*11)
p=Student(classroom = "11",name = 'tom', age =22)
p.think()
p.speak(t=3)
p.sum(1,11)

#testing Tutor class
print('\n','-'*11,'Tutor methods','-'*11)
p=Tutor(expirience = 11,name = 'tom', age =22)
p.think()
p.speak(t=3)
p.answer(2)
