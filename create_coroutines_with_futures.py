import asyncio
from aioconsole import ainput

async def busy(n):
	await asyncio.sleep(n)
	return n

def callback(future):
	n = future.result()
	if n == 0:
		print("Didn't wait at all")
	else:
		print("Waited "+str(n)+"s")

async def creator():
	while True:
		n = await ainput("How long should I get busy for? ('s' to stop)\n> ")
		if n == "s":
		    break
		print("Creating task for 'busy("+n+")'")
		n = int(n)
		co = busy(n)
		task = loop.create_task(co)
		task.add_done_callback(callback)

loop = asyncio.get_event_loop()
loop.run_until_complete(creator())
loop.close()