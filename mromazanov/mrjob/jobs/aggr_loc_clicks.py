from mrjob.job import MRJob, MRStep
import requests
import retry


@retry.retry()
def get_location(ip):
    return requests.get(f'https://ip2c.org/{ip}').text.split(';')[3]


class MRClickCount(MRJob):

    def location_mapper(self, _, line):
        line = line.strip('[]').split(',')
        ip = line[0].strip('"')
        count = int(line[1])
        temp = ip.split('.')
        ip = int(temp[0])*16777216+int(temp[1])*65536+int(temp[2])*256+int(temp[3])
        location = get_location(ip)
        yield location, count

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

    def steps(self):
        return [
            MRStep(mapper=self.location_mapper,
                    combiner=self.combiner,
                    reducer=self.reducer)
        ]



if __name__ == '__main__':
    MRClickCount.run()