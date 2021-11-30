from mrjob.job import MRJob


class MRClickCount(MRJob):

    def mapper(self, _, line):
        line = line.strip(' [').split('] ')
        yield line[1], 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        s = sum(values)
        if s > 1:
            yield key, s


if __name__ == '__main__':
    MRClickCount.run()
