from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class MRClickCount(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        line = line.strip(' [').split('] ')
        ip = line[1].strip('\ "')
        yield ip, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield None, (key, sum(values))


if __name__ == '__main__':
    MRClickCount.run()
