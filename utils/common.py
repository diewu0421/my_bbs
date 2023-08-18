import aiohttp

import nest_asyncio
nest_asyncio.apply()

async def get_html(url):
    print("url111111111111=i ", url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.text()




