import asyncio
import aiohttp
import aiofiles
from aioconsole import ainput
import os
import inspect

def callback(future):
	# First check if any exceptions arose, like a file not found
	e = future.exception()
	if e:
		print(e)
	else:
		result = future.result()
		if result[0] == read:
			print("Read from "+result[1]+":\n\t"+result[2])
		else:
			print("Wrote to "+result[1]+":\n\t"+result[2])
	# Important! Notice how release() isn't a coroutine, so it doesn't have to be awaited
	lock.release()

async def read(filename):
	async with aiofiles.open(filename, "r") as file:
		text = await file.read()
	return (read, filename, text)

async def write(filename, text):
	async with aiofiles.open(filename, "w") as file:
		await file.write(text)
	return (write, filename, text)

async def main():
	while True:
		await lock.acquire()
		action = await ainput("Would you like to read ('r') or write ('w') to a file? ('s' to stop)\n> ")
		if action in ["read", "r"]:
			filename = await ainput("Which file would you like to read from?\n> ")
			co = read(filename)
		elif action in ["write", "w"]:
			filename = await ainput("Which file would you like to write to?\n> ")
			text = await ainput("What would you like to write to "+filename+"?\n> ")
			co = write(filename, text)
		elif action in ["s", "stop"]:
			break
		else:
			continue
		task = loop.create_task(co)
		task.add_done_callback(callback)

if __name__ == "__main__":
	lock = asyncio.Lock()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()
