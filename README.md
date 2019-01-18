# asyncio Examples
A series of examples of asynchronous programming using asyncio

# Requirements
```
asyncio
aiofiles
aiohttp
ainput
asyncssh
```

# Useful resources
A historical perspective of Python asynchronicity:

http://cheat.readthedocs.io/en/latest/python/asyncio.html

A good explanation of how asyncio works:

https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e

More in-depth on callbacks:

https://hackernoon.com/controlling-python-async-creep-ec0a0f4b79ba

Look at this code sample and the image below until they both make sense:
```
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```
![async calls](https://docs.python.org/3/_images/tulip_coro.png)
