import asyncio
import json

import aiohttp


async def fetch_url(session, url):
    res = await session.get(url)
    return res


async def get_ip():
    url = "http://ip-api.com/json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            ip = json.loads(await res.text())['query']
            print("ip = ", ip)
            return ip


async def main():
    tasks = []
    tasks.append(asyncio.create_task(get_ip()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print('start')
    print("get_ip")
    asyncio.run(main())
