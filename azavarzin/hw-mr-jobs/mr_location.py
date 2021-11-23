from mrjob.job import MRJob
import requests


class MRLocation(MRJob):

    URL = "https://ip2c.org/"

    def mapper(self, _, line):
        ip = line.split()[2]
        location = requests.get(f"{MRLocation.URL}{ip}").text.split(";")[-1]
        yield location, 1

    def combiner(self, key, values):
        yield key, sum(values)


    def reducer(self, key, values):
        count = sum(values)
        if count > 1:    
            yield key, count


if __name__ == '__main__':
    MRLocation.run()
