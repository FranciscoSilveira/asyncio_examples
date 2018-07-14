import asyncio
from aioconsole import ainput

tasks = []

async def busy(n):
	print("Busy"+str(n)+" waiting")
	await asyncio.sleep(n)
	print("Busy"+str(n)+" ending")

async def quick(n):
	print("Quick "+str(n)+" (not) waiting")
	asyncio.sleep(n)
	print("Quick ending")

async def main():
	tasks = [busy(2), quick(2), busy(3)]
	print("Gathering initial tasks")
	await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()