# Для файла clicks.txt, в котором каждая запись содержит информацию о клике на нашем сайте. 
# Нужно рассчитать с агрегированные клики по IP адресам, т.е. заходил ли к нам на сайт пользователь больше чем 1 раз и если да то сколько таких раз. 

# Так же пользуясь https://about.ip2c.org/#inputs, который возвращает информацию о геолокации клика, нужно посчитать сколько к нам людей заходило и с какой локации.
# Так же нужно посмотреть сколько людей по локациям нам заходило в рабочее время с 8:00 - 19:00
# Результат:
# 1 - файл grouped.txt должен содержать только IP адреса с которых был заход больше одного раза в лед формате:
# <IP> <click_count>
# 2 - файл location.txt должен содержать локации с количеством заходов с этих локаций
# <location> - <click_count>
# 3 - файла time_location.txt должен содержать разбивку по часам и локациям с количеством кликов в формате json, пример
# {
# ""8:00"" :[
# {""<location>"": <click_count>}
# ],
# ""9:00"": [
# {""<location>"": <click_count>}
# ]
# }

# py 01_count_over_clicks.py denormalized_data.txt > grouped.txt

import json
import re
from mrjob.job import MRJob

class Count_groupby_ip(MRJob):

    def mapper(self, key, record):
        s=re.findall('.+(?=\t)',record)[0]
        l = json.loads(s)
        ip = l[1]
        value = int(re.findall('(?<=\t).*',record)[0])
        yield  ip, value

if __name__ == '__main__':
    Count_groupby_ip.run()

