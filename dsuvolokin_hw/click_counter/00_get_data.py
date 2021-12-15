# py 00_get_data.py clicks1.txt > denormalized_data.txt

from mrjob.job import MRJob
from mrjob.step import MRStep
import aiohttp
import asyncio
import re
import json

async def get_location(ip):
    async with aiohttp.ClientSession() as session:
        url = f'https://ip2c.org/?ip={ip}'
        try:
            async with session.get(url) as resp:
                response = await resp.text()
                my_re = re.compile('(?<=;)\\s{0,1}[\\w\\s\\(\\)\\.\\,\\?\\!\\@\\#\\%\\^\\&\\*\\-\\=\\+]+$')
                location = my_re.findall(response)[0]
        except Exception as e:
            location = f'error {e}'
        return location

class MRWordFrequencyCount(MRJob):
    def mapper(self, key, record):        yield  (record.split()[1][:2], record.split()[2]), 1

    def reducer(self, key, values):
        yield key, sum(values)
    
    def map_locations(self,key,values):
        if values>1:
          try:
            response = asyncio.run(get_location(key[1]))
          except:
            response = f"error"
          yield (key[0],key[1], response), values

    def steps(self):
        return [MRStep( mapper = self.mapper
                       ,reducer = self.reducer) 
               ,MRStep( mapper=self.map_locations)
              ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()
