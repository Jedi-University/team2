# py 02_count_over_locations.py denormalized_data.txt > location.txt

import json
import re
from mrjob.job import MRJob
from mrjob.step import MRStep

class Group_by_locations(MRJob):

    def mapper(self, key, record):
        s=re.findall('.+(?=\t)',record)[0]
        l = json.loads(s)
        location = l[2]
        value = int(re.findall('(?<=\t).*',record)[0])
        yield  location, value

    
    def reducer(self,key,values):
        yield key,sum(values)

    def steps(self):
        return [MRStep( mapper = self.mapper
                       ,reducer = self.reducer)
              ]

if __name__ == '__main__':

    Group_by_locations.run()
    # print(time.time() - ts)