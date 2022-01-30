"""
    api interface para requisições ao
    giphy API
"""
import json
import aiohttp

from DiscordBot.Bot import Bot

bot = Bot()


class GiphyAPI:
    """ bridge interface ao giphy API """

    def __init__(self):
        self._base = 'https://api.giphy.com/v1'
        self.key = bot.settings.GIPHY_API_KEY

    async def _make_request(self, req_type, url, *_, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = f'{self._base}/{req_type}/{url}?api_key={self.key}'

            for name, value in kwargs.items():
                if value is None:
                    continue
                url = f'{url}&{name}={value}'

            async with session.get(url) as response:
                json_response = json.loads(await response.read())

        return json_response

    async def rand_gif(self, tag=None):
        """ gerá uma gif aleatória """
        response = await self._make_request('gifs', 'random', tag=tag)

        return response['data']['images']['original']['url']
