# py 03_count_time_locations.py denormalized_data.txt > pre_location.txt

import json
import re
from mrjob.job import MRJob
from mrjob.step import MRStep

class Group_by_locations(MRJob):

    def mapper(self, key, record):
        s=re.findall('.+(?=\t)',record)[0]
        l = json.loads(s)
        hour = l[0]
        location = l[2]
        value = int(re.findall('(?<=\t).*',record)[0])
        yield  (hour,location), value

    
    def reducer(self,key,values):
        yield key[0],{key[1]: sum(values)}

    def steps(self):
        return [MRStep( mapper = self.mapper
                       ,reducer = self.reducer)
              ]

if __name__ == '__main__':

    Group_by_locations.run()
    
