from mrjob.job import MRJob
from mrjob.step import MRStep


class MRLocation(MRJob):

    FILES = ["location.py"]

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_id,
                combiner=self.reducer,
                reducer=self.reducer,
            ),
            MRStep(
                mapper=self.mapper_location,
                combiner=self.reducer,
                reducer=self.reducer,
            ),
        ]

    def mapper_id(self, _, line):
        yield line.split()[-1], 1

    def mapper_location(self, ip, count):
        from location import get_location_by_ip
        location = get_location_by_ip(ip)
        yield location, count

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == "__main__":
    MRLocation.run()
