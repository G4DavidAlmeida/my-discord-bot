import aiohttp, os, json

class GiphyAPI:    
    def __init__(self):
        self._key = os.getenv('GIPHY_API_KEY')
        self._base = 'https://api.giphy.com/v1'

    async def _make_request (self, req_type, url, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = f'{self._base}/{req_type}/{url}?api_key={self._key}'

            for name, value in kwargs.items():
                if value is None: continue
                url = f'{url}&{name}={value}'

            async with session.get(url) as response:
                json_response = json.loads(await response.read())

        return json_response

    async def rand_gif (self, tag=None):
        response = await self._make_request('gifs', 'random', tag=tag)

        return response['data']['images']['original']['url']