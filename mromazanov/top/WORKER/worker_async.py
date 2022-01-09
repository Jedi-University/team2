from WORKER.worker import Worker

class WorkerAsync(Worker):
    async def get_json(self, response):
        json = await response.json()
        return json

    async def response_mapper(self, response):
        result = {'json': await self.get_json(response)}
        if 'next' in response.links:
            result['url'] = response.links['next']['url']
        return result

    async def get_api_response(self, url, **kwargs):
        response = await self.requests.get(
            url, mapper=self.response_mapper, **kwargs)
        return response