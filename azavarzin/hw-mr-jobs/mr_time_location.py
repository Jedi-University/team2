from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
from location import get_location_by_ip


class MRTimeLocation(MRJob):

    FILES = ["location.py"]
    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_id_with_hour,
                combiner=self.reducer,
                reducer=self.reducer
            ),
            MRStep(
                mapper=self.mapper_location_with_hour,
                combiner=self.reducer,
                reducer=self.reducer
            ),
            MRStep(
                mapper=self.mapper_for_hour,
                reducer=self.reducer_for_hour
            ),
            MRStep(
                mapper=self.mapper_data,
                reducer=self.reducer_data
            )
        ]

    def mapper_id_with_hour(self, _, line):
        data = line.split()
        ip = data[-1]
        hour = data[1][:2]
        if 8 <= int(hour) <= 18:
            yield (ip, hour), 1
    
    def mapper_location_with_hour(self, ip_with_hour, count):
        ip, hour = ip_with_hour
        location = get_location_by_ip(ip)
        yield (location, hour), count        
        
    def reducer(self, key, values):
        yield key, sum(values)
    
    def mapper_for_hour(self, location_with_hour, count):
        location, hour = location_with_hour
        yield hour, {location: count}

    def reducer_for_hour(self, hour, data):
        yield hour, list(data)

    def mapper_data(self, hour, data):
        time = f"{hour}:00-{int(hour) + 1}:00"
        yield None, (time, data)

    def reducer_data(self, _, hour_data):
        yield None, dict(hour_data)


if __name__ == "__main__":
    MRTimeLocation.run()
