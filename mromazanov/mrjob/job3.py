from mrjob.job import MRJob, MRStep
from mrjob.protocol import JSONValueProtocol
import requests
import retry


@retry.retry()
def get_location(ip):
    return requests.get(f'https://ip2c.org/{ip}').text.split(';')[3]


class MRClickCount(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def time_ip_mapper(self, _, line):
        line = line.strip(' [').split('] ')
        ip = line[1]
        time = line[0].split()[1].split(':')[0]
        yield (time, ip), 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values): 
        yield key, sum(values)

    def time_loc_mapper(self, timeip, values):
        time = timeip[0]
        ip = timeip[1]
        # temp = line[1].split('.')
        # ip = int(temp[0])*16777216+int(temp[1])*65536+int(temp[2])*256+int(temp[3])
        location = get_location(ip)
        yield (time, location), values

    def reducer2(self, key, values):
        yield key[0], {key[1]:sum(values)}

    def reducer3(self, key, values):
        if int(key) >= 8 and int(key) <= 19:
            key = f'{key}:00'
            yield None, (key, list(values))
            # yield key, list(values)
    
    def reducer4(self, _, values):
        yield None, dict(values)

    def steps(self):
        return [
            MRStep(mapper=self.time_ip_mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(mapper=self.time_loc_mapper,
                    combiner=self.combiner,
                    reducer=self.reducer2),
            MRStep(reducer=self.reducer3),
            MRStep(reducer=self.reducer4)
        ]


if __name__ == '__main__':
    MRClickCount.run()
