import asyncio
from aioconsole import ainput

async def busy(n):
	print("Busy"+str(n)+" waiting")
	await asyncio.sleep(n)
	print("Busy"+str(n)+" ending")

async def creator():
	while True:
		n = await ainput("How long should I get busy for? ('s' to stop)\n> ")
		if n == "s":
		    break
		print("Creating task for 'busy("+n+")'")
		n = int(n)
		co = busy(n)
		task = loop.create_task(co)

loop = asyncio.get_event_loop()
loop.run_until_complete(creator())
loop.close()