import asyncio
import time
import aiohttp


async def nested(i = None):

    await asyncio.sleep(1)
    async with aiohttp.ClientSession() as session:
        async with session.get("http://39.106.72.90/") as response:
            print("response code ", response.status)
            text = await response.text()
            print("result= " , text)
            return text


async def main():
    tasks = []

    for i in range(1, 10):
        tasks.append(nested(i))


    start = time.time()
    ret = await asyncio.gather(*tasks)
    print("cost time ", time.time() - start)
    return ret



# asyncio.run(main())


# event = main()
loop = asyncio.get_event_loop()

main_task = loop.create_task(main())
loop.run_until_complete(main_task)

print("main_task result", main_task.result())

loop.close()
print("over")
